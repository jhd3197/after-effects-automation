// Socket server that runs inside After Effects
// This allows Python to send commands to a running AE instance

(function() {
    var PORT = 49494;
    var serverSocket = null;
    var isRunning = false;

    function startServer() {
        if (isRunning) {
            return;
        }

        try {
            serverSocket = new Socket();

            if (serverSocket.listen(PORT)) {
                isRunning = true;
                $.writeln("AE Server: Listening on port " + PORT);

                // Start listening loop
                app.scheduleTask("checkForConnections()", 100, true);
            } else {
                $.writeln("AE Server: Failed to listen on port " + PORT);
            }
        } catch (e) {
            $.writeln("AE Server Error: " + e.toString());
        }
    }

    function checkForConnections() {
        if (!serverSocket) return;

        var conn = serverSocket.poll();
        if (conn) {
            $.writeln("AE Server: Client connected");

            // Read the script content
            var scriptContent = "";
            var line;
            while ((line = conn.readln()) != "") {
                scriptContent += line + "\n";
            }

            $.writeln("AE Server: Received script (" + scriptContent.length + " bytes)");

            try {
                // Execute the script
                eval(scriptContent);

                // Send success response
                conn.writeln("OK");
                $.writeln("AE Server: Script executed successfully");
            } catch (e) {
                // Send error response
                conn.writeln("ERROR: " + e.toString());
                $.writeln("AE Server Error: " + e.toString());
            }

            conn.close();
        }
    }

    // Make checkForConnections global so scheduleTask can call it
    checkForConnections = function() {
        if (!serverSocket) return;

        var conn = serverSocket.poll();
        if (conn) {
            $.writeln("AE Server: Client connected");

            var scriptContent = "";
            var line;
            while ((line = conn.readln()) != "") {
                scriptContent += line + "\n";
            }

            $.writeln("AE Server: Received script (" + scriptContent.length + " bytes)");

            try {
                eval(scriptContent);
                conn.writeln("OK");
                $.writeln("AE Server: Script executed successfully");
            } catch (e) {
                conn.writeln("ERROR: " + e.toString());
                $.writeln("AE Server Error: " + e.toString());
            }

            conn.close();
        }
    };

    startServer();
})();
