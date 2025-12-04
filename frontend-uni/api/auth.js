import { api } from '@/common/http.js';

export function login(data) {
    return api.post('/auth/login', data);
}

export function getUserInfo() {
    return api.get('/auth/user/info');
}

export function logout() {
    return api.post('/auth/logout');
}
