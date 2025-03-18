//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//
// {'{comp_name}': 'scene-1-intro-comp-gradient-51', '{layer_name}': 'CONTROLS', '{property_name}': 'Effects.Color_01.Color', '{value}': '#DD2993'}
var compMap = [];
function duplicate_comp(compName,parentFolder){

    comp = FindItemByName(compName);
    
    duplicate_name = slugify(parentFolder+"-"+comp.name);

    _i=FindItemIdByName(duplicate_name);

    // if _i is not null, then the comp already exists
    if(_i==null){
        try{
            var duplicateComp = comp.duplicate();

            duplicateComp.parentFolder = FindItemByName(parentFolder);
            
            duplicateComp.name = duplicate_name;

            for(var i = 1; i <= duplicateComp.layers.length; i++) {
                layer = duplicateComp.layers[i];
                if(layer.nullLayer != true && layer.enabled == true){
                    if(layer.constructor.name == "AVLayer"){
                        if(layer.source.constructor.name == "CompItem") {
                            _comp={
                                'fromCompName': duplicateComp.name,
                                'toLayerIndex': layer.index,
                                'ItemName': slugify(parentFolder+"-"+layer.name),
                            }
                            compMap.push(_comp);
                            duplicate_comp(layer.name,parentFolder);
                        }
                    }
                }
        
            }
        }
        catch(err){
            print(err);
        }
    }
    else{
        duplicateComp = FindItemByName(duplicate_name);
    }
    
    return duplicateComp;
}

function copyCompAndAddToTimeline(CompTemplateName,CopyCompName,FolderName,startTime,inPoint,stretch,outPoint) {
    // Duplicate Comp
    var duplicateComp = duplicate_comp(CopyCompName,FolderName);

    saveFile("comp_map.json",JSON.stringify(compMap));

    duplicateComp.duration = outPoint;

    _comp = FindItemByName(CompTemplateName);
    
    _comp.layers.add(duplicateComp);

    _comp.layers[1].startTime = startTime;
    _comp.layers[1].inPoint   = inPoint;
    _comp.layers[1].stretch   = stretch;
    _comp.layers[1].outPoint  = outPoint;
}

copyCompAndAddToTimeline("{CompTemplateName}","{CopyCompName}","{FolderName}",{startTime},{inPoint},{stretch},{outPoint});