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
            const { tool_description } = data;
            showSpinner(tool_description);
        }
        else if (data.event =='message_finished'){
            hideSpinner()
        }
    };
    socket.onclose = () => console.log('WebSocket connection closed.');
    socket.onerror = (error) => console.error('WebSocket error:', error);

    function showSpinner(tool_description) {
        const container = document.getElementById('loading-spinner-container');
        container.style.display = 'flex';

        // Update all previous entries to show a checkmark
        const previousEntries = container.querySelectorAll('.spinner-entry');
        previousEntries.forEach(entry => {

            const labelEl = entry.querySelector('.spinner-label');
            const labelText = labelEl ? labelEl.textContent : '';

            entry.innerHTML = `
            <div class="completed-spinner">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                    <path fille="currentColor" d="M320 576C461.4 576 576 461.4 576 320C576 178.6 461.4 64 320 64C178.6 64 64 178.6 64 320C64 461.4 178.6 576 320 576zM404.4 276.7L324.4 404.7C320.2 411.4 313 415.6 305.1 416C297.2 416.4 289.6 412.8 284.9 406.4L236.9 342.4C228.9 331.8 231.1 316.8 241.7 308.8C252.3 300.8 267.3 303 275.3 313.6L302.3 349.6L363.7 251.3C370.7 240.1 385.5 236.6 396.8 243.7C408.1 250.8 411.5 265.5 404.4 276.8z"/>
                </svg>
            </div>
            <div class="spinner-label spinner-label-completed">${labelText}</div>
            `;

        });

        // Create a new entry for the current tool
        const entry = document.createElement('div');
        entry.classList.add('spinner-entry');

        entry.innerHTML = `
            <div class="spinner-animation">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                    <path fill="currentColor" d="M286.7 96.1C291.7 113 282.1 130.9 265.2 135.9C185.9 159.5 128.1 233 128.1 320C128.1 426 214.1 512 320.1 512C426.1 512 512.1 426 512.1 320C512.1 233.1 454.3 159.6 375 135.9C358.1 130.9 348.4 113 353.5 96.1C358.6 79.2 376.4 69.5 393.3 74.6C498.9 106.1 576 204 576 320C576 461.4 461.4 576 320 576C178.6 576 64 461.4 64 320C64 204 141.1 106.1 246.9 74.6C263.8 69.6 281.7 79.2 286.7 96.1z"/>
                </svg>
            </div>
            <div class="spinner-label">${tool_description}</div>
        `;

        container.appendChild(entry);
    }


    function hideSpinner() {
        const container = document.getElementById('loading-spinner-container');
        container.style.display = 'flex';

        // Update all previous entries to show a checkmark just for a moment
        const previousEntries = container.querySelectorAll('.spinner-entry');
        previousEntries.forEach(entry => {

            const labelEl = entry.querySelector('.spinner-label');
            const labelText = labelEl ? labelEl.textContent : '';

            entry.innerHTML = `
            <div class="completed-spinner">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
                    <path fille="currentColor" d="M320 576C461.4 576 576 461.4 576 320C576 178.6 461.4 64 320 64C178.6 64 64 178.6 64 320C64 461.4 178.6 576 320 576zM404.4 276.7L324.4 404.7C320.2 411.4 313 415.6 305.1 416C297.2 416.4 289.6 412.8 284.9 406.4L236.9 342.4C228.9 331.8 231.1 316.8 241.7 308.8C252.3 300.8 267.3 303 275.3 313.6L302.3 349.6L363.7 251.3C370.7 240.1 385.5 236.6 396.8 243.7C408.1 250.8 411.5 265.5 404.4 276.8z"/>
                </svg>
            </div>
            <div class="spinner-label">${labelText}</div>
            `;

        });

        container.innerHTML = '';
        container.style.display = 'none';
    }

});
