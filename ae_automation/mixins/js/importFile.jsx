//
// Rename Item
// ------------------------------------------------------------
// Language: javascript
//


var _File = File("{filePath}");
var _Item = app.project.importFile(new ImportOptions(_File));
_Item.name = "{fileName}";
_Item.parentFolder=FindItemByName("{cacheFolder}");