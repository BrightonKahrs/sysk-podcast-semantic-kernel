document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const input = document.getElementById('prompt-input');
    const chatHistory = document.getElementById('chat-history');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const prompt = input.value.trim();
        if (!prompt) return;

        const userMsg = document.createElement('div');
        userMsg.className = 'message user';
        userMsg.innerHTML = `<strong>User:</strong> ${prompt}`;
        chatHistory.insertBefore(userMsg, document.getElementById('loading-spinner-container'));
        input.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            if (!res.ok) throw new Error('Request failed');
            const data = await res.json();

            if (!data.response) throw new Error('No response in JSON');

            const assistantMsg = document.createElement('div');
            assistantMsg.className = 'message assistant';

            const parsedHTML = marked.parse(data.response);
            assistantMsg.innerHTML = `<strong>Assistant:</strong><div class="markdown">${parsedHTML}</div>`;

            assistantMsg.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });

            chatHistory.insertBefore(assistantMsg, document.getElementById('loading-spinner-container'));
            chatHistory.scrollTop = chatHistory.scrollHeight;

            const messageCount = document.querySelectorAll('.message').length;
            console.log(`Message count: ${messageCount}`);

            if (messageCount < 3) {
                const res_history = await fetch('/history-js', {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });

                const data_history = await res_history.json();
                console.log(data_history.session_ids);

                const container = document.getElementById('chat-history-list');
                container.innerHTML = ''; // optional: clear first

                data_history.session_ids.forEach(history => {
                    const historyDiv = document.createElement('div');
                    historyDiv.className = 'chat-history-id';

                    historyDiv.innerHTML = `
                        <form class="get-history-id-form" method="get" action="/history/${history.session_id}">
                            <button class="get-history-id-button" type="submit">${history.title}</button>
                        </form>
                        <form class="delete-button-form" method="post" action="/delete/${history.session_id}">
                            <button class="delete-button" type="submit">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 640 640">
                                    <path fill="currentColor" d="M262.2 48C248.9 48 236.9 56.3 232.2 68.8L216 112L120 112C106.7 112 96 122.7 96 136C96 149.3 106.7 160 120 160L520 160C533.3 160 544 149.3 544 136C544 122.7 533.3 112 520 112L424 112L407.8 68.8C403.1 56.3 391.2 48 377.8 48L262.2 48zM128 208L128 512C128 547.3 156.7 576 192 576L448 576C483.3 576 512 547.3 512 512L512 208L464 208L464 512C464 520.8 456.8 528 448 528L192 528C183.2 528 176 520.8 176 512L176 208L128 208zM288 280C288 266.7 277.3 256 264 256C250.7 256 240 266.7 240 280L240 456C240 469.3 250.7 480 264 480C277.3 480 288 469.3 288 456L288 280zM400 280C400 266.7 389.3 256 376 256C362.7 256 352 266.7 352 280L352 456C352 469.3 362.7 480 376 480C389.3 480 400 469.3 400 456L400 280z"/>
                                </svg>
                            </button>
                        </form>
                    `;

                    container.appendChild(historyDiv);
                });
            }

        } catch (err) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'message error';
            errorMsg.innerHTML = `<strong>Error:</strong> ${err.message}`;
            chatHistory.appendChild(errorMsg);
        }
    });
});
