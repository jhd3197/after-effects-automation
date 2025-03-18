//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//
// {'{comp_name}': 'scene-1-intro-comp-gradient-51', '{layer_name}': 'CONTROLS', '{property_name}': 'Effects.Color_01.Color', '{value}': '#DD2993'}


function duplicate_comp(compName){
    _layers=[];
    comp = FindItemByName(compName);
    for(var i = 1; i <= comp.layers.length; i++) {
        // Get Layer

        layer = comp.layers[i];
        _layers.push(layer);

        if(layer.constructor.name == "AVLayer"){
            try{
                if(layer.source != undefined){
                    if(layer.source.constructor.name == "CompItem") {
                        //print(layer.source.constructor.name,layer.name)

                        arr=duplicate_comp(layer.name);
                        //append arr to _layers
                        for(var j = 0; j < arr.length; j++){
                            _layers.push(arr[j]);
                        }

                    }
                }
            }
            catch(e){
                print(e.toString())
            }
        }

    }
    print("Layer Count:",_layers.length)
}
_layers=[];

function duplicate_comp1(comp,parentFolder,outputName,deph){
    _comps=[]
    
    if(outputName==null || outputName==""){
        outputName = parentFolder+"-"+comp.name;
    }
    
    if(deph==0){
        //Create Folder Here
        //if parentFolder is null or empty
        _folder=app.project.items.addFolder(outputName)
        _folder.parentFolder = FindItemByName(parentFolder);
        parentFolder=_folder.name;
    }

    if(comp.constructor.name == "CompItem") {
        //print(comp.name)

        var duplicate_comp = comp.duplicate();
        //duplicate_comp.name = slugify(comp.name);
        // Set Comp Parent Folder
        duplicate_comp.parentFolder = FindItemByName(parentFolder);
        //var duplicate_comp = comp;
        _comp={
            "comp":duplicate_comp,
            "parent_comp":comp.name,
            "deph":deph
        }
        _comps.push(_comp);
        deph++;

        for(var i = 1; i <= duplicate_comp.layers.length; i++) {
            layer = duplicate_comp.layers[i];
            //layer.name=parentFolder+"-"+comp.layers[i].name;
            //print(comp.constructor.name,comp.name,String(deph));
            try{
                if(layer.source != undefined){
                    if(layer.source.constructor.name == "CompItem") {
                        _folder=duplicate_comp1(layer.source,parentFolder,outputName,deph);
                        // Loop through _folder
                        for(var j = 0; j < _folder.length; j++){
                            //print("-"+_folder[j]["comp"].name,deph,_folder[j]["comp_name"])
                            layer.replaceSource(_folder[j]["comp"], true)
                        }
                       

                        // Print _comps as json string
                        //alert(_folder);

                    }
                }
            }
            catch(e){
                print(e.toString())
            }
            _layers.push(layer);

        }
        print(comp.name,duplicate_comp.name,String(deph));
        print("------------------------------------------------------");

    }
    else{
        print(comp.name); 
    }
    return _comps
}


compName="Quote_Template_1"
comp = FindItemByName(compName);

duplicate_comp1(comp,"Template1","",0);

// Print _comps as json string

//print("Layer Count:",_layers.length)

//var duplicate_comp = duplicateCompCurrent(compName,"Template1","Template-1-"+compName,0);