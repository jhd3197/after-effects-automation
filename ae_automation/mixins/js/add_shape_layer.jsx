// Add a shape layer with a rectangle to a composition
// Parameters: {comp_name}, {layer_name}, {width}, {height}, {color_r}, {color_g}, {color_b}

var comp = null;

// Find the composition
for (var i = 1; i <= app.project.numItems; i++) {
    if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "{comp_name}") {
        comp = app.project.item(i);
        break;
    }
}

if (comp) {
    var shapeLayer = comp.layers.addShape();
    shapeLayer.name = "{layer_name}";

    // Add rectangle shape
    var shapeGroup = shapeLayer.property("Contents").addProperty("ADBE Vector Group");
    shapeGroup.name = "Rectangle";

    var rect = shapeGroup.property("Contents").addProperty("ADBE Vector Shape - Rect");
    rect.property("Size").setValue([parseFloat("{width}"), parseFloat("{height}")]);

    // Add fill
    var fill = shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Fill");
    fill.property("Color").setValue([
        parseFloat("{color_r}"),
        parseFloat("{color_g}"),
        parseFloat("{color_b}")
    ]);

    outputLogs("Shape layer '" + "{layer_name}" + "' added to " + "{comp_name}");
} else {
    outputLogs("Error: Composition '{comp_name}' not found");
}
