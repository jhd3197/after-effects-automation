// Add a solid layer to a composition
// Parameters: {comp_name}, {layer_name}, {color_r}, {color_g}, {color_b}, {width}, {height}

var comp = null;

// Find the composition
for (var i = 1; i <= app.project.numItems; i++) {
    if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "{comp_name}") {
        comp = app.project.item(i);
        break;
    }
}

if (comp) {
    var color = [
        parseFloat("{color_r}"),
        parseFloat("{color_g}"),
        parseFloat("{color_b}")
    ];

    var solidLayer = comp.layers.addSolid(
        color,
        "{layer_name}",
        parseFloat("{width}"),
        parseFloat("{height}"),
        1.0
    );

    outputLogs("Solid layer '" + "{layer_name}" + "' added to " + "{comp_name}");
} else {
    outputLogs("Error: Composition '{comp_name}' not found");
}
