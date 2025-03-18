//
// Rename Item
// ------------------------------------------------------------
// Language: javascript
//
// Reference: NT Productions || https://www.youtube.com/watch?v=iur2c0MlzzY

/*
var _File = File("{filePath}");
var _Item = app.project.importFile(new ImportOptions(_File));
_Item.name = "{fileName}";
_Item.parentFolder=FindItemByName("{cacheFolder}");*/

//comp=app.project.activeItem;
deselectAll();
comp=app.project.item(FindItemIdByName("{compName}"))

var bt = new BridgeTalk();
var path = "{outputPath}";
if(!BridgeTalk.isRunning("ame")) {
    BridgeTalk.launch("ame", "background");
    //alert("Launching Adobe Media Encoder (required to be open for proper rendering");
}
var rqItem = app.project.renderQueue.items.add(comp);
var module = rqItem.outputModule(1);
module.file = File(path+"/"+comp.name);
app.project.renderQueue.queueInAME(true);
