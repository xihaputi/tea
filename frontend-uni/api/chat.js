import { api } from '@/common/http.js';

export function askChatbot(data) {
    return api.post('/chat/ask', data);
}

export function getLatestChat() {
    return api.get('/chat/latest');
}
