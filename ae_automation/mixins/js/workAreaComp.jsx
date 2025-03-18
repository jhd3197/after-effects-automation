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
comp=app.project.item(FindItemIdByName("{compName}"))

comp.workAreaStart = {startTime};
comp.workAreaDuration = {durationTime};

