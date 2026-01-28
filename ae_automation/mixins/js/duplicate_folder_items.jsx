//
// Duplicate Folder Items
// ------------------------------------------------------------
// Language: javascript
//
// Duplicates all items from a source folder into a target folder.
// For CompItems, performs recursive duplication of nested comps.

var sourceFolderName = "{sourceFolderName}";
var targetFolderName = "{targetFolderName}";
var parentFolder = "{parentFolder}";

// Find or create the target folder
var targetFolderId = FindItemIdByName(targetFolderName);
if (targetFolderId == null) {
    var targetFolderItem = app.project.items.addFolder(targetFolderName);
    if (parentFolder != "") {
        targetFolderItem.parentFolder = FindItemByName(parentFolder);
    }
} else {
    var targetFolderItem = FindItemByName(targetFolderName);
}

// Collect items from source folder
var projectItems = app.project.items;
var sourceItems = [];
for (var i = 1; i <= projectItems.length; i++) {
    if (String(projectItems[i].parentFolder.name) == sourceFolderName) {
        sourceItems.push(projectItems[i]);
    }
}

var results = [];

// Recursive comp duplication (reuses pattern from duplicate_comp_2.jsx)
function duplicateCompDeep(comp, destFolder) {
    var dupName = slugify(destFolder.name + "-" + comp.name);
    var existingId = FindItemIdByName(dupName);

    if (existingId != null) {
        return FindItemByName(dupName);
    }

    try {
        var dup = comp.duplicate();
        dup.parentFolder = destFolder;
        dup.name = dupName;

        for (var j = 1; j <= dup.layers.length; j++) {
            var layer = dup.layers[j];
            if (layer.nullLayer != true && layer.enabled == true) {
                if (layer.constructor.name == "AVLayer") {
                    if (layer.source.constructor.name == "CompItem") {
                        var newChild = duplicateCompDeep(layer.source, destFolder);
                        layer.replaceSource(newChild, false);
                    }
                }
            }
        }
        return dup;
    } catch (err) {
        print(err);
        return comp;
    }
}

// Duplicate each item
for (var s = 0; s < sourceItems.length; s++) {
    var srcItem = sourceItems[s];
    var newItem;

    if (srcItem.constructor.name == "CompItem") {
        newItem = duplicateCompDeep(srcItem, targetFolderItem);
    } else {
        newItem = srcItem.duplicate();
        newItem.parentFolder = targetFolderItem;
    }

    results.push({
        originalName: String(srcItem.name),
        newName: String(newItem.name),
        type: String(newItem.constructor.name),
        id: newItem.id
    });
}

saveFile("duplicate_folder_items.json", JSON.stringify(results));
