// document.addEventListener('DOMContentLoaded', () => {
//     const chatForm = document.getElementById('chat-form');
//     const input = document.getElementById('prompt-input');
//     const chatHistory = document.getElementById('chat-history');

//     chatForm.addEventListener('submit', async (e) => {
//         e.preventDefault();

//         const prompt = input.value.trim();
//         if (!prompt) return;

//         const userMsg = document.createElement('div');
//         userMsg.className = 'message user';
//         userMsg.innerHTML = `<strong>User:</strong> ${prompt}`;
//         chatHistory.insertBefore(userMsg, document.getElementById('loading-spinner'));
//         input.value = '';
//         chatHistory.scrollTop = chatHistory.scrollHeight;

//         try {
//             const res = await fetch('/chat', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ prompt })
//             });

//             if (!res.ok) throw new Error('Request failed');
//             const data = await res.json();

//             if (!data.response) throw new Error('No response in JSON');

//             const assistantMsg = document.createElement('div');
//             assistantMsg.className = 'message assistant';

//             const parsedHTML = marked.parse(data.response);
//             assistantMsg.innerHTML = `<strong>Assistant:</strong><div class="markdown">${parsedHTML}</div>`;

//             assistantMsg.querySelectorAll('pre code').forEach((block) => {
//                 hljs.highlightElement(block);
//             });

//             chatHistory.insertBefore(assistantMsg, document.getElementById('loading-spinner'));
//             chatHistory.scrollTop = chatHistory.scrollHeight;
//         } catch (err) {
//             const errorMsg = document.createElement('div');
//             errorMsg.className = 'message error';
//             errorMsg.innerHTML = `<strong>Error:</strong> ${err.message}`;
//             chatHistory.appendChild(errorMsg);
//         }
//     });
// });
