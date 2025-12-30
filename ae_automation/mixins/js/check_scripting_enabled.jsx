// Check if scripting is enabled and show the current settings

var result = {};

try {
    // Check if we can access app.project
    result.hasProject = app.project ? true : false;
    result.projectName = app.project ? (app.project.file ? app.project.file.name : "Untitled") : "No project";

    // Check scripting preferences
    result.scriptsCanWriteFiles = app.preferences.getPrefAsLong("Main Pref Section", "Pref_SCRIPTING_FILE_NETWORK_SECURITY") === 1;

    // Get AE version
    result.aeVersion = app.version;

    // Create message
    var msg = "After Effects Scripting Status:\n\n";
    msg += "Version: " + result.aeVersion + "\n";
    msg += "Has Project: " + result.hasProject + "\n";
    msg += "Project: " + result.projectName + "\n";
    msg += "Scripts Can Write Files: " + result.scriptsCanWriteFiles + "\n\n";

    if (!result.scriptsCanWriteFiles) {
        msg += "WARNING WARNING WARNING\n\n";
        msg += "Scripts cannot write files!\n\n";
        msg += "To fix:\n";
        msg += "1. Go to Edit > Preferences > Scripting & Expressions\n";
        msg += "2. Check 'Allow Scripts to Write Files and Access Network'\n";
        msg += "3. Restart After Effects\n";
    } else {
        msg += "Scripts are enabled and ready!";
    }

    alert(msg);
    outputLogs(JSON.stringify(result));

} catch (e) {
    alert("Error checking scripting status:\n" + e.toString());
    outputLogs("Error: " + e.toString());
}
