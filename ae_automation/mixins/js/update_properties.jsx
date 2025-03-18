//
// Update Comp
// ------------------------------------------------------------
// Language: javascript
//


function updateCompProperties(compName, layer_name, property_name, property_value) {
    
    property=propertyParser(FindLayerByComp(compName,layer_name),property_name);
    property.setValue(valueParser(property_value));

}

updateCompProperties("{comp_name}","{layer_name}","{property_name}","{value}")