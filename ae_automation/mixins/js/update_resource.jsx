//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//


function editResource(_comp,layer_index,startTime,inPoint,stretch,outPoint,moveToEnd) {

    _comp.layers[layer_index].startTime = startTime;
    _comp.layers[layer_index].inPoint   = inPoint;
    _comp.layers[layer_index].stretch   = stretch;
    _comp.layers[layer_index].outPoint  = outPoint;
    if(moveToEnd=="true"){
        _comp.layers[layer_index].moveToEnd()
    }
}

editResource(FindItemByName("{CompName}"),{layerIndex},{startTime},{inPoint},{stretch},{outPoint},"{moveToEnd}");