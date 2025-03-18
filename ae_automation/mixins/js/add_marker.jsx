//
// Add Marker
// ------------------------------------------------------------
// Language: javascript
//


function addMarker(compName, layer_name, marker_name, marker_time) {
    
    layer=FindLayerByComp(compName,layer_name);
    var mv = new MarkerValue(marker_name);
    layer.property("Marker").setValueAtTime(marker_time, mv);
}

addMarker("{comp_name}","{layer_name}","{marker_name}",{marker_time})