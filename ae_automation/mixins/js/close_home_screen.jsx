// Close the Home screen and ensure we're on a project
// This handles After Effects 2024/2025 which opens with a Home screen

// Check if we're on the Home screen or have no project
if (!app.project || !app.project.file) {
    // Create a new project to get past the Home screen
    app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    app.newProject();
}

outputLogs("Home screen handled, project ready");
