import subprocess
from lib2to3.pgen2.pgen import DFAState
import pyautogui
import time
import os
import pandas as pd
from pydantic import FilePath
import pydirectinput
import json
import re
from pywinauto.keyboard import send_keys
import sys
import uuid
import shutil
from ae_automation import settings
from jsmin import jsmin
from mutagen.mp3 import MP3
from moviepy import VideoFileClip

class afterEffectMixin:
    """
    ToolsMixin
    """
    #TODO - Add search for items inside folder
    #FIXME - Create a function to duplicate comp and loop through layers to duplicate all the comps inside the comp
    #TODO - Create a duplicate function for items inside folder

    #TODO - Create function to edit values from comp or create a template.json and add the values there then the script will read the values from there will modify the json
    #TODO - Add transitions layer
    afterEffectItems=[]
    
    def startAfterEffect(self, data):
        """
        startAfterEffect
        """
        filePath = data["project"]["project_file"]
        print("Start After Effect")
        print(data["project"]["debug"])
        print("filePath")
        print(filePath)
        
        # Define the new file path
        new_file_path = os.path.join(data["project"]["output_dir"], "ae_automation.aep")
        
        # Check if the file exists, delete if it does
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        
        # Copy the original file to the new location
        shutil.copy(filePath, new_file_path)
        
        # Update filePath variable
        filePath = new_file_path
        print(f"File copied to {filePath}")
        
        if data["project"]["debug"] == False:
            os.startfile(filePath)
            # Wait for After Effects to be fully loaded and ready
            if not self.wait_for_after_effects_ready(timeout=120):
                raise Exception("After Effects failed to start or become ready")

        self.deselectAll()

        # Get Map Project 
        Project_Map=self.getProjectMap()

        # Extract file name from path
        fileName=os.path.basename(filePath)

        print("Project Is Open and Ready") 

        print("Check if the project folder is created") 
       
        if self.checkIfItemExists(settings.AFTER_EFFECT_PROJECT_FOLDER):
            self.createFolder(settings.AFTER_EFFECT_PROJECT_FOLDER)
        
        print("Project Folder is already created")

        print("Check if the comp is created")
        
        if self.checkIfItemExists(data["project"]["comp_name"]):
            print("Create Comp")
            if type(data["project"]["comp_end_time"]) is str:
                if ":" in data["project"]["comp_end_time"]:
                    # convert 00:12:00 to 7200
                    comp_end_time=data["project"]["comp_end_time"].split(":")
                    comp_end_time=int(comp_end_time[0])*3600+int(comp_end_time[1])*60+int(comp_end_time[2])
            else:
                comp_end_time=data["project"]["comp_end_time"]

            self.createComp(data["project"]["comp_name"],folderName=settings.AFTER_EFFECT_PROJECT_FOLDER,compWidth=data["project"]["comp_width"],compHeight=data["project"]["comp_height"],duration=comp_end_time,frameRate=data["project"]["comp_fps"])

        print("Comp is already created")

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

        print("Setting up the project")
        for i, itemTimeline in enumerate(data["timeline"]):
            scene_folder=self.slug("Scene "+str(i+1))

            print("Setting up",scene_folder)

            if not self.checkIfItemExists(scene_folder):
                self.deleteFolder(scene_folder)

            self.createFolder(scene_folder,settings.AFTER_EFFECT_PROJECT_FOLDER)
            self.addCompToTimeline(data["project"]["comp_name"],itemTimeline["template_comp"],scene_folder,itemTimeline["startTime"],itemTimeline["duration"])

            for custom_edit in itemTimeline["custom_actions"]:
                self.parseCustomActions(custom_edit,scene_folder,itemTimeline,data)
                
        if data["project"]["debug"] == False:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(10)
            os.system('taskkill /F /FI "WINDOWTITLE eq Adobe After Effects*"')
            time.sleep(10)
            output_file=self.renderFile(filePath,data["project"]["comp_name"],data["project"]["output_dir"])

    def getResourceDuration(self,resource_name):
        """
        getResourceDuration
        """
        for resource in self.afterEffectResource:
            if resource["name"] == resource_name:
                return float(resource["duration"])
        return 0        

    def parseCustomActions(self,custom_edit,scene_folder,itemTimeline,data):
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

    def checkIfItemExists(self, itemName):
        """
        check If Item Exists
        """
        for items in self.afterEffectItems:
            if items["name"] == itemName:
                return False
        return True

    def focusOnProjectPanel(self):
        """
        focusOnProjectPanel
        """
        pyautogui.hotkey('ctrl', '0')
        time.sleep(2)
        pyautogui.hotkey('ctrl', '0')
        time.sleep(2)

    def getProjectMap(self):
        """
        getProjectMap
        """
        print("Get Project Map")
        
        self.runScript("file_map.jsx")
        time.sleep(2)
        data = json.load(open(settings.CACHE_FOLDER+"/file_map.json", encoding='utf-8'))
        
        self.afterEffectItems=data["files"]
        print("Finish Get Project Map")
        return data

    def createFolder(self, folderName, parentFolder=""):
        """
        createFolder
        """
        _replace={
            "{folderName}":str(folderName),
            "{parentFolder}":str(parentFolder),
        }
        print("Creating Folder",folderName)
        self.runScript("create_folder.jsx",_replace)
        print("Finish Creating Folder",folderName)
        
    def deleteFolder(self, folderName):
        """
        Delete Folder
        """
        print("Delete Folder")
        self.goToItem(folderName)
        send_keys('{DEL}')
        time.sleep(1)
        send_keys('{ENTER}')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 's')

    def createComp(self, compName,compWidth=1980,compHeight=1080,pixelAspect=1,duration=120,frameRate=30,folderName=""):
        """
        Create Comp
        """
        print("Creating Comp",compName)
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
        print("Finish Creating Comp",compName)

    def goToItem(self,itemName):
        self.deselectAll()
        for item in self.afterEffectItems:
            if item["name"] == itemName:
                self.selectItem(item["id"])
                break
            
    def selectItem(self,index):
        """
        selectItem
        """
        _replace={
            "index":str(index)
        }
        self.runScript("selectItem.jsx",_replace)

    def selectItemByName(self,name):
        """
        Select Item By Name
        """
        _replace={
            "{name}":str(name)
        }
        self.runScript("selectItemByName.jsx",_replace)

    def openItemByName(self,name):
        """
        Select Item By Name
        """
        _replace={
            "{name}":str(name)
        }
        self.runScript("openItemName.jsx",_replace)
        
    def editComp(self, comp_name, layer_name, property_name, value):
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{property_name}":str(property_name),
            "{value}":str(value),
        }
        print(_replace)
        self.runScript("update_properties.jsx",_replace)
        
    def selectLayerByName(self, comp_name, layer_name):
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
        }
        self.runScript("selectLayerByLayer.jsx",_replace)

    def selectLayerByIndex(self, comp_name, layer_index):
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_index}":str(layer_index),
        }
        self.runScript("selectLayerByIndex.jsx",_replace)

    def editLayerAtKey(self, comp_name, layer_name, property_name, value,frame):
        """
        editComp
        """
        _replace={
            "{comp_name}":str(comp_name),
            "{layer_name}":str(layer_name),
            "{property_name}":str(property_name),
            "{value}":str(value),
            "{frame}":str(frame),
        }
        self.runScript("update_properties_frame.jsx",_replace)

    def editComp1(self, comp_name, layer_name, property_name, value):
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
            
    def swapItem(self, fromCompName, toLayerIndex, ItemName):
        self.openItemByName(fromCompName)
        self.selectItemByName(ItemName)
        time.sleep(2)
        self.selectLayerByIndex(fromCompName, toLayerIndex)
        pyautogui.hotkey('ctrl', 'alt', '/')

    def addMarker(self, comp_name, layer_name, marker_name, marker_time):
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

    def addCompToTimeline(self,CompTemplateName, CopyCompName, FolderName, startTime=0.0, compDuration=0.0, inPoint=0.0, stretch=100, outputName=""):
        """
        add Comp To Timeline
        """
        self.addCompToTimelineB1(CompTemplateName, CopyCompName, FolderName, startTime, compDuration, inPoint, stretch)

    def addCompToTimelineB1(self,CompTemplateName, CopyCompName, FolderName, startTime=0.0, compDuration=0.0, inPoint=0.0, stretch=100):
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

    def addResourceToTimeline(self,ResourceName, CompName, startTime=0.0, compDuration=0.0, inPoint=0.0, stretch=100, moveToEnd=False):
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

    def updateLayerProperties(self, CompName, layerIndex=0, startTime=0.0, compDuration=0.0, inPoint=0.0, stretch=100, moveToEnd=False):
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

    def addCompToTimelineA1(self,CompTemplateID, compName, compStartTime=0, compDuration=0, compInPoint=0, compStretch=100):
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
    
    def renameItem(self,itemID,itemName):
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

    def importFile(self,filePath,fileName,cacheFolder):
        """
        Import File
        """
        _replace={
            "{filePath}":str(filePath),
            "{fileName}":str(fileName),
            "{cacheFolder}":str(cacheFolder),
        }
        self.runScript("importFile.jsx",_replace)

    def renderComp(self,compName,outputPath):
        _replace={
            "{outputPath}":str(outputPath),
            "{compName}":str(compName)
        }
        self.runScript("renderComp.jsx",_replace) 
        return outputPath+"/"+compName+".mp4"

    def deselectAll(self):
        """
        deselectAll
        """
        self.focusOnProjectPanel()
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'shift', 'a')
        time.sleep(2)

    def executeCommand(self, cmdId):
        """
        run Command
        """
        _replace={
            "cmdId":str(cmdId)
        }
        self.runScript("run_command.jsx",_replace)

    def runScript(self, fileName, _remplacements=None,debug=False):
        """
        run Script
        """
        print("Start Run Script", fileName)
        fileContent=self.file_get_contents(os.path.join(settings.JS_DIR, fileName))
        filePath=os.path.join(settings.CACHE_FOLDER, fileName)
        
        if _remplacements is not None:
            for key, value in _remplacements.items():
                fileContent=fileContent.replace(key,value)

        fileContent = jsmin(self.JS_FRAMEWORK) + "\n var _error=''; try{" + fileContent + "\n}catch(e){_error= e.lineNumber+' '+e.toString(); }outputLogs(_error);"

        randomName=str(uuid.uuid4())
        fileContent=fileContent.replace("{LOGS_NAME}",randomName)
        fileContent=fileContent.replace("{FILE_NAME}",fileName)

        with open(filePath, "w") as text_file:
            text_file.write(fileContent)

        app = os.path.join(settings.AFTER_EFFECT_FOLDER, 'AfterFX.exe')
        
        subprocess.Popen([app, '-s', f"var a = new File('{filePath}'); a.open(); eval(a.read()); app.exitAfterLaunchAndEval = false;"])

        time.sleep(3)
        print("Finish Run Script", fileName)

    def workAreaComp(self,compName,startTime,endTime):
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

    def runCommand(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                print(output.decode('utf-8').strip())
        
        stderr = process.communicate()[1]
        
        if process.returncode != 0:
            raise Exception(f"Error: {stderr.decode('utf-8')}")
        
        return "Command executed successfully."

    def renderFile(self, projectPath, compName, outputDir):
        """
        Render an Adobe After Effects project file via terminal
        """
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        
        outputPath = os.path.join(outputDir, f"{compName}.mp4")
        
        render_command = f'"{settings.AERENDER_PATH}" -project "{projectPath}" -comp "{compName}" -output "{outputPath}" -mem_usage 20 40'
        print("Rendering project...")
        self.runCommand(render_command)
        
        return outputPath
    
    def time_to_seconds(self, time_str):
        h, m, s = map(float, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def convertMovToMp4(self, inputPath, outputPath):
        """
        Convert MOV to MP4 using moviepy
        """
        print("Converting MOV to MP4 using moviepy...")
        clip = VideoFileClip(inputPath)
        clip.write_videofile(outputPath, codec="libx264", audio_codec="aac", fps=29.97)
        clip.close()
