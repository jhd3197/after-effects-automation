// Add a null object layer to a composition
// Parameters: {comp_name}, {layer_name}

var comp = null;

// Find the composition
for (var i = 1; i <= app.project.numItems; i++) {
    if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "{comp_name}") {
        comp = app.project.item(i);
        break;
    }
}

if (comp) {
    var nullLayer = comp.layers.addNull();
    nullLayer.name = "{layer_name}";

    outputLogs("Null layer '" + "{layer_name}" + "' added to " + "{comp_name}");
} else {
    outputLogs("Error: Composition '{comp_name}' not found");
}
