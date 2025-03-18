//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//

function duplicateComp(compName,parentFolder,outputName,deph) {

    comp_id = FindItemIdByName(compName);
    comp = FindItemByName(compName);

    if(deph==0){
        //Create Folder Here
        //if parentFolder is null or empty
        if(outputName==null || outputName==""){
            outputName = parentFolder+"-"+comp.name;
        }
        _folder=app.project.items.addFolder(outputName)
        _folder.parentFolder = FindItemByName(parentFolder);
        parentFolder=_folder.name;
    }
    deph++;
    

    // Duplicate Comp
    var duplicate_comp = comp.duplicate();
    // Set Comp Name
    duplicate_comp.name = slugify(outputName);
    // Set Comp Parent Folder
    duplicate_comp.parentFolder = FindItemByName(parentFolder);
    // Loop through comp layers
    for(var i = 1; i <= comp.layers.length; i++) {

        // Get Layer
        layer = comp.layers[i];
        
        // if layer is not null
        try{
            
            // Check if Layer Source is a Comp
            if(layer.source.constructor.name == "CompItem") {

                var layer_copy=duplicate_comp.layers[i];
                
                // Keep looping until all the layers are not a comp
                var child_comp = duplicateComp(layer.source.name,parentFolder,outputName,deph)

                // Replace Layer Source with Child Comp
                layer_copy.replaceSource(child_comp, true)
            }
        }
        catch(err){
        }
    }
    return duplicate_comp
}

function copyCompAndAddToTimeline(CompTemplateName,CopyCompName,FolderName,outputName,startTime,inPoint,stretch,outPoint) {
    // Duplicate Comp
    var duplicate_comp = duplicateComp(CopyCompName,FolderName,outputName,0);

    duplicate_comp.duration = outPoint;

    _comp = FindItemByName(CompTemplateName);
    
    _comp.layers.add(duplicate_comp);

    _comp.layers[1].startTime = startTime;
    _comp.layers[1].inPoint   = inPoint;
    _comp.layers[1].stretch   = stretch;
    _comp.layers[1].outPoint  = outPoint;
}

copyCompAndAddToTimeline("{CompTemplateName}","{CopyCompName}","{FolderName}","{outputName}",{startTime},{inPoint},{stretch},{outPoint});