//
// Update Comp at Key
// ------------------------------------------------------------
// Language: javascript
//

function updateCompPropertiesAtKey(compName, layer_name, property_name, property_value, frame) {
   
    property=propertyParser(FindLayerByComp(compName,layer_name),property_name);
    property.setValueAtTime(frame,valueParser(property_value));

}

updateCompPropertiesAtKey("{comp_name}","{layer_name}","{property_name}","{value}","{frame}")