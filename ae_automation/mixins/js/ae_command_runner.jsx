/*
 * After Effects Command Runner
 * This script runs on AE startup and watches for commands from Python
 *
 * Installation:
 * Copy this file to:
 * C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\Scripts\Startup\
 *
 * After installation, restart After Effects
 */

(function() {
    // Get the queue folder path from environment or use default
    var queueFolder = Folder.userData.fsName + "\\ae_automation\\queue";

    // Ensure queue folder exists
    var folder = new Folder(queueFolder);
    if (!folder.exists) {
        folder.create();
    }

    $.writeln("AE Command Runner: Watching " + queueFolder);

    // Function to process command files
    function processCommands() {
        try {
            var folder = new Folder(queueFolder);
            if (!folder.exists) {
                return;
            }

            var files = folder.getFiles("*.jsx");

            for (var i = 0; i < files.length; i++) {
                var file = files[i];

                // Skip if file is being written (very small delay)
                if (file.length < 10) {
                    continue;
                }

                $.writeln("AE Command Runner: Executing " + file.name);

                try {
                    // Read and execute the script
                    file.open('r');
                    var scriptContent = file.read();
                    file.close();

                    // Execute the script
                    eval(scriptContent);

                    $.writeln("AE Command Runner: Success - " + file.name);

                    // Delete the file after successful execution
                    file.remove();

                } catch (e) {
                    $.writeln("AE Command Runner: Error in " + file.name + ": " + e.toString());

                    // Rename to .error so it doesn't get processed again
                    var errorFile = new File(file.fsName.replace('.jsx', '.error'));
                    file.rename(errorFile.name);
                }
            }
        } catch (e) {
            $.writeln("AE Command Runner: Error processing commands: " + e.toString());
        }
    }

    // Set up interval to check for new commands every 500ms
    app.scheduleTask("processAECommands()", 500, true);

    // Make processCommands global so scheduleTask can call it
    $.global.processAECommands = processCommands;

    $.writeln("AE Command Runner: Started successfully");
})();
