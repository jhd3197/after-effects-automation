//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//
// {'{comp_name}': 'scene-1-intro-comp-gradient-51', '{layer_name}': 'CONTROLS', '{property_name}': 'Effects.Color_01.Color', '{value}': '#DD2993'}
var compMap = [];
function duplicate_comp(compName, parentFolder) {

    var comp = FindItemByName(compName);

    var duplicate_name = slugify(parentFolder + "-" + comp.name);

    var _i = FindItemIdByName(duplicate_name);

    // if _i is not null, then the comp already exists
    if (_i == null) {
        try {
            var duplicateComp = comp.duplicate();

            duplicateComp.parentFolder = FindItemByName(parentFolder);

            duplicateComp.name = duplicate_name;

            for (var i = 1; i <= duplicateComp.layers.length; i++) {
                var layer = duplicateComp.layers[i];
                if (layer.nullLayer != true && layer.enabled == true) {
                    if (layer.constructor.name == "AVLayer") {
                        if (layer.source.constructor.name == "CompItem") {
                            // Recursively duplicate the child comp
                            var newChildComp = duplicate_comp(layer.source.name, parentFolder);

                            // Immediately swap the source of the layer to the new duplicate
                            layer.replaceSource(newChildComp, false);
                        }
                    }
                }

            }
        }
        catch (err) {
            print(err);
        }
    }
    else {
        duplicateComp = FindItemByName(duplicate_name);
    }

    return duplicateComp;
}

function copyCompAndAddToTimeline(CompTemplateName, CopyCompName, FolderName, startTime, inPoint, stretch, outPoint) {
    // Duplicate Comp
    var duplicateComp = duplicate_comp(CopyCompName, FolderName);

    saveFile("comp_map.json", JSON.stringify(compMap));

    duplicateComp.duration = outPoint;

    _comp = FindItemByName(CompTemplateName);

    _comp.layers.add(duplicateComp);

    _comp.layers[1].startTime = startTime;
    _comp.layers[1].inPoint = inPoint;
    _comp.layers[1].stretch = stretch;
    _comp.layers[1].outPoint = outPoint;
}

copyCompAndAddToTimeline("{CompTemplateName}", "{CopyCompName}", "{FolderName}", {startTime}, {inPoint}, {stretch}, {outPoint});