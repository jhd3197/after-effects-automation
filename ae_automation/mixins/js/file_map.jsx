//
// File Map
// ------------------------------------------------------------
// Language: javascript
//

var projectItems = app.project.items;

var fileMap = [];
for (var i = 1; i <= projectItems.length; i++) {
    _file={
        id: i,
        name: String(projectItems[i].name),
        type: String(projectItems[i].constructor.name),
        parentFolder: String(projectItems[i].parentFolder.name),
        parentId: String(projectItems[i].parentFolder.id),
    };
    
    fileMap.push(_file);
}

//Save the fileMap to a file
_obj={
    projectName: app.project.file.name,
    files: fileMap
}

saveFile("file_map.json",JSON.stringify(_obj));

