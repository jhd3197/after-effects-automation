//
// Create Folder
// ------------------------------------------------------------
// Language: javascript
//

function create_folder(folderName,parentFolder){
    _folder=app.project.items.addFolder(folderName);
    //if parentFolder is null or empty, then the folder will be created in the root folder
    if(parentFolder!=""){
        _folder.parentFolder = FindItemByName(parentFolder);
    }
}

create_folder("{folderName}","{parentFolder}");