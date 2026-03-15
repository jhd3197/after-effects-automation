//
// Search Folder Items
// ------------------------------------------------------------
// Language: javascript
//
// Finds all project items whose parentFolder matches the given folder name
// and saves the result as JSON to the cache folder.

var folderName = "{folderName}";
var projectItems = app.project.items;
var results = [];

for (var i = 1; i <= projectItems.length; i++) {
    if (String(projectItems[i].parentFolder.name) == folderName) {
        var item = {
            id: i,
            name: String(projectItems[i].name),
            type: String(projectItems[i].constructor.name),
            parentFolder: String(projectItems[i].parentFolder.name),
            parentId: String(projectItems[i].parentFolder.id)
        };
        results.push(item);
    }
}

saveFile("search_folder_items.json", JSON.stringify(results));
