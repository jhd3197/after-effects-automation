// Debug save project - outputs diagnostic information

try {
    print("=== Save Project Debug ===");
    print("Project exists: " + (app.project != null));
    print("Project items count: " + app.project.items.length);
    print("Project file path: " + (app.project.file ? app.project.file.fsName : "NONE - Project not saved yet"));

    var projectPath = "{projectPath}";
    print("Target save path: " + projectPath);

    // Check if path is valid
    var projectFile = new File(projectPath);
    print("File object created: " + (projectFile != null));
    print("Parent folder: " + projectFile.parent.fsName);
    print("Parent folder exists: " + projectFile.parent.exists);

    // Try to save
    print("Attempting to save...");
    app.project.save(projectFile);
    print("Save completed!");

    // Verify file exists
    projectFile = new File(projectPath);
    print("File exists after save: " + projectFile.exists);
    print("File size: " + (projectFile.exists ? projectFile.length : 0) + " bytes");

    outputLogs("SUCCESS: Project saved to: " + projectPath);
} catch(e) {
    var errorMsg = "ERROR at line " + e.line + ": " + e.toString();
    print(errorMsg);
    outputLogs(errorMsg);
}
