// Add a text layer to a composition
// Parameters: {comp_name}, {layer_name}, {text_content}, {x_position}, {y_position}, {font_size}

var comp = null;

// Find the composition
for (var i = 1; i <= app.project.numItems; i++) {
    if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "{comp_name}") {
        comp = app.project.item(i);
        break;
    }
}

if (comp) {
    var textLayer = comp.layers.addText("{text_content}");
    textLayer.name = "{layer_name}";

    // Set position
    var position = textLayer.property("Transform").property("Position");
    position.setValue([parseFloat("{x_position}"), parseFloat("{y_position}")]);

    // Set font size
    var textProp = textLayer.property("Source Text");
    var textDocument = textProp.value;
    textDocument.fontSize = parseFloat("{font_size}");
    textProp.setValue(textDocument);

    outputLogs("Text layer '" + "{layer_name}" + "' added to " + "{comp_name}");
} else {
    outputLogs("Error: Composition '{comp_name}' not found");
}
