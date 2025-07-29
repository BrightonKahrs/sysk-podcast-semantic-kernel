// static/js/websocket.js

async function getBackendUrl() {
    try {
        const res = await fetch('/config');
        if (!res.ok) throw new Error('Failed to fetch config');
        const config = await res.json();
        return config.backend_url;
    } catch (err) {
        console.error('Error fetching backend config:', err);
        // Fallback to localhost or other default
        return 'http://localhost:7000';
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const backendUrl = await getBackendUrl();

    const protocol = backendUrl.startsWith('https') ? 'wss:' : 'ws:';
    const backendHost = backendUrl.replace(/^https?:\/\//, '');
    const socket = new WebSocket(`${protocol}//${backendHost}/ws`);

    socket.onopen = () => console.log('WebSocket connection established.');
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received WebSocket message:', data);

        if (data.event === 'tool_call') {
            const { tool_name } = data;
            showSpinner(tool_name);
        }
        else if (data.event =='message_finished'){
            hideSpinner()
        }
    };
    socket.onclose = () => console.log('WebSocket connection closed.');
    socket.onerror = (error) => console.error('WebSocket error:', error);

    function showSpinner(toolName) {
        const spinner = document.getElementById('loading-spinner');
        const label = spinner?.querySelector('.spinner-label');
        if (spinner) {
            spinner.style.display = 'flex'; // so the spinner + label are side-by-side
            if (label) {
                label.textContent = `Running tool: ${toolName}`;
            }
        }
    }

    function hideSpinner() {
        const spinner = document.getElementById('loading-spinner');
        if (spinner) {
            spinner.style.display = 'none';
        }
    }
});
