//
// Add Transition
// ------------------------------------------------------------
// Language: javascript
//
// Adds transition keyframes to a layer in a composition.
// Supported types: fade_in, fade_out, cross_dissolve, slide_left, slide_right, wipe_left

var compName = "{comp_name}";
var layerName = "{layer_name}";
var transitionType = "{transition_type}";
var startTime = parseFloat("{start_time}");
var duration = parseFloat("{duration}");

var comp = FindItemByName(compName);
var layer = FindLayerByComp(compName, layerName);

if (layer != null && comp != null) {
    var endTime = startTime + duration;

    if (transitionType == "fade_in") {
        var opacity = layer.property("Transform").property("Opacity");
        opacity.setValueAtTime(startTime, 0);
        opacity.setValueAtTime(endTime, 100);
    }
    else if (transitionType == "fade_out") {
        var opacity = layer.property("Transform").property("Opacity");
        opacity.setValueAtTime(startTime, 100);
        opacity.setValueAtTime(endTime, 0);
    }
    else if (transitionType == "cross_dissolve") {
        // Fade out current layer over the duration
        var opacity = layer.property("Transform").property("Opacity");
        opacity.setValueAtTime(startTime, 100);
        opacity.setValueAtTime(endTime, 0);
    }
    else if (transitionType == "slide_left") {
        var position = layer.property("Transform").property("Position");
        var compWidth = comp.width;
        var centerY = comp.height / 2;
        var centerX = compWidth / 2;
        // Start off-screen right, slide to center
        position.setValueAtTime(startTime, [compWidth + centerX, centerY]);
        position.setValueAtTime(endTime, [centerX, centerY]);
    }
    else if (transitionType == "slide_right") {
        var position = layer.property("Transform").property("Position");
        var compWidth = comp.width;
        var centerY = comp.height / 2;
        var centerX = compWidth / 2;
        // Start off-screen left, slide to center
        position.setValueAtTime(startTime, [-centerX, centerY]);
        position.setValueAtTime(endTime, [centerX, centerY]);
    }
    else if (transitionType == "wipe_left") {
        // Wipe using position: start fully visible, move off-screen left
        var position = layer.property("Transform").property("Position");
        var compWidth = comp.width;
        var centerY = comp.height / 2;
        var centerX = compWidth / 2;
        position.setValueAtTime(startTime, [centerX, centerY]);
        position.setValueAtTime(endTime, [-centerX, centerY]);
    }

    print("Transition " + transitionType + " applied to layer " + layerName);
} else {
    print("Error: Could not find comp or layer for transition");
}
