// static/js/websocket.js

document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket('ws://localhost:7000/ws');

    socket.onopen = () => console.log('WebSocket connection established.');
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received WebSocket message:', data);

        if (data.event === 'tool_call') {
            const { tool_name } = data;
            showSpinner(tool_name);
        }
    };
    socket.onclose = () => console.log('WebSocket connection closed.');
    socket.onerror = (error) => console.error('WebSocket error:', error);

    function showSpinner(toolName) {
        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';
        spinner.innerText = `Running tool: ${toolName}`;
    }
});
