from __future__ import annotations

import subprocess
import time
import os
import json
import uuid
import shutil
from typing import Any
from ae_automation import settings
from ae_automation.logging_config import get_logger
from ae_automation.exceptions import (
    AENotResponsiveError,
    ScriptExecutionError,
    RenderError,
)
from jsmin import jsmin
from mutagen.mp3 import MP3
from moviepy import VideoFileClip

logger = get_logger(__name__)

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import pydirectinput
except ImportError:
    pydirectinput = None

try:
    from pywinauto.keyboard import send_keys
except ImportError:
    send_keys = None

class afterEffectMixin:
    """
    afterEffectMixin
    """
    afterEffectItems: list[dict[str, Any]]
    afterEffectResource: list[dict[str, Any]]
    JS_FRAMEWORK: str

    def sanitize_text_for_ae(self, text: Any) -> Any:
        """
        Sanitize text before sending to After Effects.
        Must be done in Python before JS to avoid string escaping issues.
        """
        if not isinstance(text, str):
            return text

        # Replace HTML line breaks with carriage return (AE uses \r for newlines)
        text = text.replace('<br>', '\r')
        text = text.replace('<br/>', '\r')
        text = text.replace('<BR>', '\r')
        text = text.replace('<BR/>', '\r')
        text = text.replace('<br />', '\r')
        text = text.replace('<BR />', '\r')

        # DON'T convert quotes - keep them as-is to avoid UTF-8 encoding issues
        # After Effects handles straight quotes fine, and converting causes encoding problems
        # The â€™ you're seeing is UTF-8 curly quote being misinterpreted as Latin-1

        return text

    def startAfterEffect(self, data: dict[str, Any]) -> None:
        """
        startAfterEffect
        """
        settings.validate_settings()
        filePath = data["project"]["project_file"]
        logger.info("Start After Effect")
        logger.debug("debug=%s", data["project"]["debug"])
        logger.debug("filePath=%s", filePath)
        
        # Define the new file path
        new_file_path = os.path.join(data["project"]["output_dir"], "ae_automation.aep")
        
        # Check if the file exists, delete if it does
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        
        # Copy the original file to the new location
        shutil.copy(filePath, new_file_path)
        
        # Update filePath variable
        filePath = new_file_path
        logger.info("File copied to %s", filePath)
        
        if not data["project"]["debug"]:
            os.startfile(filePath)
            # Wait for After Effects to be fully loaded and ready
            if not self.wait_for_after_effects_ready(timeout=120):
                raise AENotResponsiveError(timeout=120)

        self.deselectAll()

        # Get Map Project 
        Project_Map=self.getProjectMap()

        # Extract file name from path
        fileName=os.path.basename(filePath)

        logger.info("Project is open and ready")

        logger.info("Checking if project folder exists") 
       
        if self.checkIfItemExists(settings.AFTER_EFFECT_PROJECT_FOLDER):
            self.createFolder(settings.AFTER_EFFECT_PROJECT_FOLDER)
        
        logger.info("Project folder ready")

        logger.info("Checking if comp exists")
        
        if self.checkIfItemExists(data["project"]["comp_name"]):
            logger.info("Creating comp")
            if type(data["project"]["comp_end_time"]) is str:
                if ":" in data["project"]["comp_end_time"]:
                    # convert 00:12:00 to 7200
                    comp_end_time=data["project"]["comp_end_time"].split(":")
                    comp_end_time=int(comp_end_time[0])*3600+int(comp_end_time[1])*60+int(comp_end_time[2])
            else:
                comp_end_time=data["project"]["comp_end_time"]

            self.createComp(data["project"]["comp_name"],folderName=settings.AFTER_EFFECT_PROJECT_FOLDER,compWidth=data["project"]["comp_width"],compHeight=data["project"]["comp_height"],duration=comp_end_time,frameRate=data["project"]["comp_fps"])

        logger.info("Comp ready")

        self.createFolder(settings.AFTER_EFFECT_PROJECT_FOLDER+"-cache",settings.AFTER_EFFECT_PROJECT_FOLDER)
        #Import Resources
        for resource in data["project"]["resources"]:
            self.importFile(resource["path"],resource["name"],settings.AFTER_EFFECT_PROJECT_FOLDER+"-cache")
            resource["duration"]=0
            # if path contains .mp3
            if ".mp3" in resource["path"]:
                # Get mp3 duration and convert it to seconds
                audio = MP3(resource["path"])
                mp3_duration=audio.info.length
                resource["duration"]=mp3_duration

        self.afterEffectResource=data["project"]["resources"]

        Project_Map=self.getProjectMap()

        logger.info("Setting up the project")
        for i, itemTimeline in enumerate(data["timeline"]):
            scene_folder=self.slug("Scene "+str(i+1))

            logger.info("Setting up %s", scene_folder)

            if not self.checkIfItemExists(scene_folder):
                self.deleteFolder(scene_folder)

            self.createFolder(scene_folder,settings.AFTER_EFFECT_PROJECT_FOLDER)
            self.addCompToTimeline(data["project"]["comp_name"],itemTimeline["template_comp"],scene_folder,itemTimeline["startTime"],itemTimeline["duration"])

            for custom_edit in itemTimeline["custom_actions"]:
                self.parseCustomActions(custom_edit,scene_folder,itemTimeline,data)
                
        if not data["project"]["debug"]:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(10)
            os.system('taskkill /F /FI "WINDOWTITLE eq Adobe After Effects*"')
            time.sleep(10)
            output_file=self.renderFile(filePath,data["project"]["comp_name"],data["project"]["output_dir"])

    def getResourceDuration(self, resource_name: str) -> float:
        """
        getResourceDuration
        """
        for resource in self.afterEffectResource:
            if resource["name"] == resource_name:
                return float(resource["duration"])
        return 0        

    def parseCustomActions(self, custom_edit: dict[str, Any], scene_folder: str, itemTimeline: dict[str, Any], data: dict[str, Any]) -> None:
        if "property_type" in custom_edit:
            if custom_edit["property_type"] == "color":
                custom_edit["value"]=self.hexToRGBA(custom_edit["value"])

        if custom_edit["change_type"] == "update_layer_property":
            self.editComp(self.slug(scene_folder+" "+custom_edit["comp_name"]),custom_edit["layer_name"],custom_edit["property_name"],custom_edit["value"])
            
        if custom_edit["change_type"] == "update_layer_property_at_frame":
            self.editLayerAtKey(self.slug(scene_folder+" "+custom_edit["comp_name"]),custom_edit["layer_name"],custom_edit["property_name"],custom_edit["value"],custom_edit["frame"])
            
        if custom_edit["change_type"] == "add_resource":
            if "moveToEnd" not in custom_edit:
                custom_edit["moveToEnd"]="false"

            _comp_duration=float(custom_edit["duration"])
            if _comp_duration == 0.0:
                _comp_duration=self.getResourceDuration(custom_edit["resource_name"])
                
            self.addResourceToTimeline(custom_edit["resource_name"],self.slug(scene_folder+" "+custom_edit["comp_name"]),custom_edit["startTime"],_comp_duration,moveToEnd=str(custom_edit["moveToEnd"]).lower())

        if custom_edit["change_type"] == "edit_resource":
            self.updateLayerProperties(self.slug(scene_folder+" "+custom_edit["comp_name"]),custom_edit["layerIndex"],custom_edit["startTime"],custom_edit["duration"],moveToEnd=str(custom_edit["moveToEnd"]).lower())

        if custom_edit["change_type"] == "swap_items_by_index":
            self.swapItem(self.slug(scene_folder+" "+custom_edit["comp_name"]),custom_edit["layer_index"],custom_edit["layer_name"])
            if custom_edit["fit_to_screen"]:
                pyautogui.hotkey('ctrl', 'alt', 'f')
            if custom_edit["fit_to_screen_width"]:
                pyautogui.hotkey('ctrl', 'alt', 'shift', 'h')
            if custom_edit["fit_to_screen_height"]:
                pyautogui.hotkey('ctrl', 'alt', 'shift', 'g')

        if custom_edit["change_type"] == "add_marker":
            self.addMarker(self.slug(scene_folder+" "+custom_edit["comp_name"]),self.slug(scene_folder+" "+custom_edit["layer_name"]),custom_edit["marker_name"],custom_edit["marker_time"])
            
        if custom_edit["change_type"] == "template":
            if custom_edit["template_name"] in data["templates"]:
                for _template in data["templates"][custom_edit["template_name"]]:
                    template_edit=_template.copy()
                    for key,value in template_edit.items():
                        if "{" in str(value) and "}" in str(value):
                            template_edit[key]=custom_edit["template_values"][value[1:-1]]
                    self.parseCustomActions(template_edit,scene_folder,itemTimeline,data)

        if custom_edit["change_type"] == "add_comp":
            self.addCompToTimeline(self.slug(scene_folder+" "+itemTimeline["template_comp"]),custom_edit["comp_name"],scene_folder,custom_edit["startTime"],custom_edit["duration"])

        if custom_edit["change_type"] == "apply_template_values":
            target = self.slug(scene_folder + " " + custom_edit["comp_name"])
            values_source = custom_edit.get("values_file") or custom_edit.get("values", [])
            if isinstance(values_source, str):
                self.applyTemplateValues(target, values_file=values_source)
            else:
                self.applyTemplateValues(target, values=values_source)

        if custom_edit["change_type"] == "add_transition":
            self.addTransition(
                self.slug(scene_folder + " " + custom_edit["comp_name"]),
                custom_edit["layer_name"],
                custom_edit.get("transition_type", "fade_in"),
                custom_edit.get("start_time", 0.0),
                custom_edit.get("duration", 1.0)
            )

    def checkIfItemExists(self, itemName: str) -> bool:
        """
        check If Item Exists
        """
        for items in self.afterEffectItems:
            if items["name"] == itemName:
                return False
        return True

    def focusOnProjectPanel(self) -> None:
        """
        focusOnProjectPanel
        """
        pyautogui.hotkey('ctrl', '0')
        time.sleep(2)
        pyautogui.hotkey('ctrl', '0')
        time.sleep(2)

    def getProjectMap(self) -> dict[str, Any]:
        """
        getProjectMap
        """
        logger.info("Getting project map")
        
        self.runScript("file_map.jsx")
        time.sleep(2)
        data = json.load(open(settings.CACHE_FOLDER+"/file_map.json", encoding='utf-8'))
        
        self.afterEffectItems=data["files"]
        logger.debug("Finished getting project map")
        return data

    def getFolderItems(self, folder_name: str) -> list[dict[str, Any]]:
        """Return items from cached afterEffectItems whose parentFolder matches folder_name."""
        return [item for item in self.afterEffectItems if item.get("parentFolder") == folder_name]

    def searchFolderItems(self, folder_name: str) -> list[dict[str, Any]]:
        """Execute JSX to get fresh folder contents from AE project, return as list of dicts."""
        _replace = {
            "{folderName}": str(folder_name),
        }
        self.runScript("search_folder_items.jsx", _replace)
        data = json.load(open(settings.CACHE_FOLDER + "/search_folder_items.json", encoding='utf-8'))
        return data

    def createFolder(self, folderName: str, parentFolder: str = "") -> None:
        """
        createFolder
        """
        _replace={
            "{folderName}":str(folderName),
            "{parentFolder}":str(parentFolder),
        }
        logger.info("Creating folder: %s", folderName)
        self.runScript("create_folder.jsx",_replace)
        logger.debug("Finished creating folder: %s", folderName)
        
    def deleteFolder(self, folderName: str) -> None:
        """
        Delete Folder
        """
        logger.info("Deleting folder: %s", folderName)
        self.goToItem(folderName)
        send_keys('{DEL}')
        time.sleep(1)
        send_keys('{ENTER}')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 's')

    def createComp(self, compName: str, compWidth: int = 1980, compHeight: int = 1080, pixelAspect: int = 1, duration: float = 120, frameRate: float = 30, folderName: str = "") -> None:
        """
        Create Comp
        """
        logger.info("Creating comp: %s", compName)
        _replace={
            "{compName}":str(compName),
            "{compWidth}":str(compWidth),
            "{compHeight}":str(compHeight),
            "{pixelAspect}":str(pixelAspect),   
            "{duration}":str(duration),
            "{frameRate}":str(frameRate),
            "{folderName}":str(folderName)
        }
        self.runScript("addComp.jsx",_replace)
        logger.debug("Finished creating comp: %s", compName)

    def goToItem(self, itemName: str) -> None:
        self.deselectAll()
        for item in self.afterEffectItems:
            if item["name"] == itemName:
                self.selectItem(item["id"])
                break
            
    def selectItem(self, index: int | str) -> None:
        """
        selectItem
        """
        _replace={
            "index":str(index)
        }
        self.runScript("selectItem.jsx",_replace)

    def selectItemByName(self, name: str) -> None:
        """
        Select Item By Name
        """
        _replace={
            "{name}":str(name)
        }
        self.runScript("selectItemByName.jsx",_replace)

    def openItemByName(self, name: str) -> None:
        """
        Select Item By Name
        """
        _replace={
            "{name}":str(name)
        }
        self.runScript("openItemName.jsx",_replace)
        
    def editComp(self, comp_name: str, layer_name: str, property_name: str, value: Any) -> None:
        """
        editComp
        """
        # Sanitize text values before sending to After Effects
        if isinstance(value, str):
            value = self.sanitize_text_for_ae(value)

        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{property_name}":str(property_name),
            "{value}":str(value),
        }
        logger.debug("editComp replacements: %s", _replace)
        self.runScript("update_properties.jsx",_replace)
        
    def selectLayerByName(self, comp_name: str, layer_name: str) -> None:
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
        }
        self.runScript("selectLayerByLayer.jsx",_replace)

    def selectLayerByIndex(self, comp_name: str, layer_index: int | str) -> None:
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_index}":str(layer_index),
        }
        self.runScript("selectLayerByIndex.jsx",_replace)

    def editLayerAtKey(self, comp_name: str, layer_name: str, property_name: str, value: Any, frame: int | float | str) -> None:
        """
        editComp
        """
        # Sanitize text values before sending to After Effects
        if isinstance(value, str):
            value = self.sanitize_text_for_ae(value)

        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{property_name}":str(property_name),
            "{value}":str(value),
            "{frame}":str(frame),
        }
        self.runScript("update_properties_frame.jsx",_replace)

    def editComp1(self, comp_name: str, layer_name: str, property_name: str, value: Any) -> None:
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{property_name}":str(property_name),
            "{value}":str(value),
        }
        self.runScript("duplicate_comp_1.jsx",_replace)
            
    def swapItem(self, fromCompName: str, toLayerIndex: int | str, ItemName: str) -> None:
        self.openItemByName(fromCompName)
        self.selectItemByName(ItemName)
        time.sleep(2)
        self.selectLayerByIndex(fromCompName, toLayerIndex)
        pyautogui.hotkey('ctrl', 'alt', '/')

    def addMarker(self, comp_name: str, layer_name: str, marker_name: str, marker_time: float | str) -> None:
        """
        add marker
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{marker_name}":str(marker_name),
            "{marker_time}":str(marker_time),
        }
        self.runScript("add_marker.jsx",_replace)

    def addCompToTimeline(self, CompTemplateName: str, CopyCompName: str, FolderName: str, startTime: float = 0.0, compDuration: float = 0.0, inPoint: float = 0.0, stretch: int = 100, outputName: str = "") -> None:
        """
        add Comp To Timeline
        """
        self.addCompToTimelineB1(CompTemplateName, CopyCompName, FolderName, startTime, compDuration, inPoint, stretch)

    def addCompToTimelineB1(self, CompTemplateName: str, CopyCompName: str, FolderName: str, startTime: float = 0.0, compDuration: float = 0.0, inPoint: float = 0.0, stretch: int = 100) -> None:
        """
        add Comp To Timeline
        """
        _replace={
            "{CompTemplateName}":str(CompTemplateName),
            "{CopyCompName}":str(CopyCompName),
            "{FolderName}":str(FolderName),
            "{startTime}":str(startTime),
            "{inPoint}":str(inPoint),
            "{stretch}":str(stretch),
            "{outPoint}":str(startTime+compDuration)
        }

        self.runScript("duplicate_comp_2.jsx",_replace)
        
        data = json.load(open(settings.CACHE_FOLDER+"/comp_map.json", encoding='utf-8'))

        for comp in data:
            self.swapItem(comp["fromCompName"],comp["toLayerIndex"],comp["ItemName"])

    def duplicateFolderItems(self, source_folder: str, target_folder: str, parent_folder: str = "") -> list[dict[str, Any]]:
        """Duplicate all items from source_folder into target_folder."""
        _replace = {
            "{sourceFolderName}": str(source_folder),
            "{targetFolderName}": str(target_folder),
            "{parentFolder}": str(parent_folder),
        }
        self.runScript("duplicate_folder_items.jsx", _replace)
        data = json.load(open(settings.CACHE_FOLDER + "/duplicate_folder_items.json", encoding='utf-8'))
        return data

    def addResourceToTimeline(self, ResourceName: str, CompName: str, startTime: float = 0.0, compDuration: float = 0.0, inPoint: float = 0.0, stretch: int = 100, moveToEnd: bool | str = False) -> None:
        """
        add Comp To Timeline
        """
        _replace={
            "{ResourceName}":str(ResourceName),
            "{CompName}":str(CompName),
            "{startTime}":str(startTime),
            "{inPoint}":str(inPoint),
            "{stretch}":str(stretch),
            "{outPoint}":str(float(startTime)+float(compDuration)),
            "{moveToEnd}":str(moveToEnd).lower(),
        }
        self.runScript("add_resource.jsx",_replace)

    def updateLayerProperties(self, CompName: str, layerIndex: int = 0, startTime: float = 0.0, compDuration: float = 0.0, inPoint: float = 0.0, stretch: int = 100, moveToEnd: bool | str = False) -> None:
        """
        add Comp To Timeline
        """
        _replace={
            "{CompName}":str(CompName),
            "{layerIndex}":str(layerIndex),
            "{startTime}":str(startTime),
            "{inPoint}":str(inPoint),
            "{stretch}":str(stretch),
            "{outPoint}":str(float(startTime)+float(compDuration)),
            "{moveToEnd}":str(moveToEnd).lower(),
        }
        self.runScript("update_resource.jsx",_replace,debug=True)

    def addCompToTimelineA1(self, CompTemplateID: int | str, compName: str, compStartTime: float = 0, compDuration: float = 0, compInPoint: float = 0, compStretch: int = 100) -> None:
        """
        add Comp To Timeline
        """
        _replace={
            "{CompTemplateID}":str(CompTemplateID),
            "{compName}":str(compName),
            "{start_time}":str(compStartTime),
            "{end_time}":str(compStartTime+compDuration),
            "{inPoint}":str(compInPoint),
            "{stretch}":str(compStretch),
        }
        self.runScript("add_comp_to_templates.jsx",_replace)
    
    def renameItem(self, itemID: int | str, itemName: str) -> None:
        """
        renameItem
        """
        _replace={
            "{index}":str(itemID),
            "{name}":str(itemName),
        }
        self.runScript("renameItem.jsx",_replace)
        _file_map=self.afterEffectItems
        for item in _file_map:
            if item["id"] == itemID:
                item["name"]=itemName
                break
        self.afterEffectItems=_file_map

    def importFile(self, filePath: str, fileName: str, cacheFolder: str) -> None:
        """
        Import File
        """
        _replace={
            "{filePath}":str(filePath),
            "{fileName}":str(fileName),
            "{cacheFolder}":str(cacheFolder),
        }
        self.runScript("importFile.jsx",_replace)

    def renderComp(self, compName: str, outputPath: str) -> str:
        _replace={
            "{outputPath}":str(outputPath),
            "{compName}":str(compName)
        }
        self.runScript("renderComp.jsx",_replace) 
        return outputPath+"/"+compName+".mp4"

    def deselectAll(self) -> None:
        """
        deselectAll
        """
        self.focusOnProjectPanel()
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'shift', 'a')
        time.sleep(2)

    def executeCommand(self, cmdId: int | str) -> None:
        """
        run Command
        """
        _replace={
            "cmdId":str(cmdId)
        }
        self.runScript("run_command.jsx",_replace)

    def _execute_script_in_running_ae(self, script_path: str) -> None:
        """
        Execute a script in an already-running After Effects instance
        Uses file-based command queue system
        """
        # Generate unique filename to avoid conflicts
        queue_file = os.path.join(settings.QUEUE_FOLDER, f"cmd_{uuid.uuid4().hex[:8]}.jsx")

        try:
            # Ensure queue folder exists
            os.makedirs(settings.QUEUE_FOLDER, exist_ok=True)

            # Copy the script to the queue folder
            shutil.copy2(script_path, queue_file)

            # Wait for the script to be processed (deleted by AE)
            # The ae_command_runner.jsx script running in AE will pick it up
            max_wait = 10  # seconds
            wait_interval = 0.1  # seconds
            elapsed = 0

            while os.path.exists(queue_file) and elapsed < max_wait:
                time.sleep(wait_interval)
                elapsed += wait_interval

            if os.path.exists(queue_file):
                # File still exists - might not have been processed
                # Check if it was renamed to .error
                error_file = queue_file.replace('.jsx', '.error')
                if os.path.exists(error_file):
                    logger.warning("Script execution failed - check %s", error_file)
                    os.remove(error_file)
                else:
                    logger.warning("Script may not have been processed by After Effects")
                    logger.warning("Make sure the ae_command_runner.jsx startup script is installed")
                    # Clean up
                    try:
                        os.remove(queue_file)
                    except Exception:
                        pass
        except OSError as e:
            logger.error("Error queueing script: %s", e)
            # Clean up on error
            try:
                if os.path.exists(queue_file):
                    os.remove(queue_file)
            except OSError:
                pass

    def runScript(self, fileName: str, _remplacements: dict[str, str] | None = None, debug: bool = False) -> str:
        """
        run Script
        """
        logger.info("Running script: %s", fileName)
        fileContent=self.file_get_contents(os.path.join(settings.JS_DIR, fileName))
        filePath=os.path.join(settings.CACHE_FOLDER, fileName)

        if _remplacements is not None:
            for key, value in _remplacements.items():
                fileContent=fileContent.replace(key,value)

        fileContent = jsmin(self.JS_FRAMEWORK) + "\n var _error=''; try{" + fileContent + "\n}catch(e){_error= e.lineNumber+' '+e.toString(); }outputLogs(_error);"

        randomName=str(uuid.uuid4())
        fileContent=fileContent.replace("{LOGS_NAME}",randomName)
        fileContent=fileContent.replace("{FILE_NAME}",fileName)

        with open(filePath, "w", encoding='utf-8') as text_file:
            text_file.write(fileContent)

        # Execute script in the already-running After Effects instance using queue system
        self._execute_script_in_running_ae(filePath)

        time.sleep(1)  # Reduced sleep time since we wait in _execute_script_in_running_ae
        logger.debug("Finished script: %s", fileName)
        return randomName

    def applyTemplateValues(self, comp_name: str, values: list[dict[str, Any]] | None = None, values_file: str | None = None) -> None:
        """Apply template values to a composition.

        Args:
            comp_name: Target composition name
            values: List of value dicts with layer_name, property_name, value
            values_file: Path to JSON file with template values (alternative to values param)
        """
        if values_file:
            with open(values_file, encoding='utf-8') as f:
                data = json.load(f)
            comp_name = data.get("comp_name", comp_name)
            values = data.get("values", [])

        if values is None:
            values = []

        for val in values:
            if val.get("property_type") == "color":
                val["value"] = self.hexToRGBA(val["value"])
            self.editComp(comp_name, val["layer_name"], val["property_name"], val["value"])

    def addTransition(self, comp_name: str, layer_name: str, transition_type: str = "fade_in",
                      start_time: float = 0.0, duration: float = 1.0) -> None:
        """Add a transition effect to a layer.

        Args:
            comp_name: Target composition name
            layer_name: Layer to apply transition to
            transition_type: One of: fade_in, fade_out, cross_dissolve, slide_left, slide_right, wipe_left
            start_time: When the transition starts (seconds)
            duration: Transition duration (seconds)
        """
        _replace = {
            "{comp_name}": str(comp_name),
            "{layer_name}": str(layer_name),
            "{transition_type}": str(transition_type),
            "{start_time}": str(start_time),
            "{duration}": str(duration),
        }
        self.runScript("add_transition.jsx", _replace)

    def workAreaComp(self, compName: str, startTime: float, endTime: float) -> None:
        """
        workAreaComp
        """
        duration=endTime-startTime
        _replace={
            "{compName}":str(compName),
            "{startTime}":str(startTime),
            "{durationTime}":str(duration)
        }
        self.runScript("workAreaComp.jsx",_replace)

    def runCommand(self, command: str) -> str:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                logger.info(output.decode('utf-8').strip())
        
        stderr = process.communicate()[1]
        
        if process.returncode != 0:
            raise RenderError(detail=stderr.decode('utf-8'))
        
        return "Command executed successfully."

    def renderFile(self, projectPath: str, compName: str, outputDir: str) -> str:
        """
        Render an Adobe After Effects project file via terminal
        """
        settings.validate_settings()
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        
        outputPath = os.path.join(outputDir, f"{compName}.mp4")
        
        render_command = f'"{settings.AERENDER_PATH}" -project "{projectPath}" -comp "{compName}" -output "{outputPath}" -mem_usage 20 40'
        logger.info("Rendering project...")
        self.runCommand(render_command)
        
        return outputPath
    
    def time_to_seconds(self, time_str: str) -> float:
        h, m, s = map(float, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def convertMovToMp4(self, inputPath: str, outputPath: str) -> None:
        """
        Convert MOV to MP4 using moviepy
        """
        logger.info("Converting MOV to MP4 using moviepy...")
        clip = VideoFileClip(inputPath)
        clip.write_videofile(outputPath, codec="libx264", audio_codec="aac", fps=29.97)
        clip.close()
