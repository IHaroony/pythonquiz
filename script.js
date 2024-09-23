document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://127.0.0.1:5000');

    // Initialize the xterm.js terminal
    const term = new Terminal({
        cursorBlink: true,
        fontFamily: 'JetBrains Mono, monospace',  // Set a readable font
        fontSize: 14,  // Set a reasonable font size
        theme: {
            background: '#000000',  // Black background
            foreground: '#ffffff',  // White text
            cursor: '#ff6347',      // Red cursor
            selection: '#87cefa'    // Blue text selection
        }
    });

    // Open the terminal inside the terminal container
    const terminalElement = document.getElementById('terminal');
    term.open(terminalElement);

    // Initial welcome message
    term.write("Press Enter to start the Quiz...\r\n");

    let started = false;
    let userInput = '';

    // Handle terminal input (when user types)
    term.onData(data => {
        if (!started && data === '\r') {
            started = true;
            term.clear();  // Clear the terminal when quiz starts
            socket.emit('start_code_execution');  // Emit event to start the quiz on the backend
        } else if (started) {
            if (data === '\r') {
                socket.emit('input', userInput);  // Send user input to the backend
                userInput = '';  // Clear input after sending
                term.write('\r\n');  // Move to the next line
            } else {
                userInput += data;  // Collect user input
                term.write(data);  // Echo input to the terminal
            }
        }
    });

    // Receive output from the backend and display it in the terminal
    socket.on('output', data => {
        term.write(data + '\r\n');  // Write output from the backend to the terminal
    });

    // Dynamically resize the terminal to fit the container size
    const resizeTerminal = () => {
        const width = terminalElement.clientWidth;
        const height = terminalElement.clientHeight;

        const cols = Math.floor(width / 9);  // Approximate width per character
        const rows = Math.floor(height / 18);  // Approximate height per line

        term.resize(cols, rows);  // Resize terminal to fit the container
    };

    // Resize terminal on window resize
    window.addEventListener('resize', resizeTerminal);

    // Call resize initially to make sure the terminal fits
    resizeTerminal();
});
