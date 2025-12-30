// Create a new After Effects project
// This closes the current project and creates a new one

app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
app.newProject();

outputLogs("New project created");
