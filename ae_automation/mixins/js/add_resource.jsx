//
// Duplicate Component
// ------------------------------------------------------------
// Language: javascript
//


function addResource(_Item,_comp,startTime,inPoint,stretch,outPoint,moveToEnd) {

    _comp.layers.add(_Item);

    _comp.layers[1].startTime = startTime;
    _comp.layers[1].inPoint   = inPoint;
    _comp.layers[1].stretch   = stretch;
    _comp.layers[1].outPoint  = outPoint;
    if(moveToEnd=="true"){
        _comp.layers[1].moveToEnd()
    }
}

addResource(FindItemByName("{ResourceName}"),FindItemByName("{CompName}"),{startTime},{inPoint},{stretch},{outPoint},"{moveToEnd}");