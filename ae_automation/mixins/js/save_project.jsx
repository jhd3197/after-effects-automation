// Save the current project to a specified path
// Parameters: {projectPath}

var projectFile = new File("{projectPath}");
app.project.save(projectFile);

outputLogs("Project saved to: {projectPath}");
