// Debug version of comp creation with detailed alerts
// Parameters: {compName}, {compWidth}, {compHeight}, {duration}, {frameRate}, {folderName}

try {
    alert("DEBUG: Starting composition creation\nComp Name: {compName}\nWidth: {compWidth}\nHeight: {compHeight}");

    var compName = "{compName}";
    var compWidth = parseInt("{compWidth}");
    var compHeight = parseInt("{compHeight}");
    var pixelAspect = 1;
    var duration = parseFloat("{duration}");
    var frameRate = parseFloat("{frameRate}");
    var folderName = "{folderName}";

    // Find or create folder
    var targetFolder = null;
    if (folderName) {
        for (var i = 1; i <= app.project.numItems; i++) {
            if (app.project.item(i) instanceof FolderItem && app.project.item(i).name === folderName) {
                targetFolder = app.project.item(i);
                break;
            }
        }
    }

    alert("DEBUG: Creating comp...\nTarget folder: " + (targetFolder ? targetFolder.name : "root"));

    // Create composition
    var comp = app.project.items.addComp(compName, compWidth, compHeight, pixelAspect, duration, frameRate);

    // Move to folder if specified
    if (targetFolder) {
        comp.parentFolder = targetFolder;
    }

    alert("DEBUG: Composition created successfully!\nComp Name: " + comp.name + "\nID: " + comp.id);

    outputLogs("Composition created: " + compName);

} catch (e) {
    alert("DEBUG ERROR in comp creation:\n" + e.toString() + "\n\nLine: " + e.line);
    outputLogs("Error creating comp: " + e.toString());
}
