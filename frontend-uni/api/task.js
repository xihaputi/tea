import { api } from '@/common/http.js';

export function getTaskList(params) {
    return api.get('/tasks/', params);
}

export function createTask(data) {
    return api.post('/tasks/', data);
}

export function updateTask(id, data) {
    return api.put(`/tasks/${id}`, data);
}

export function deleteTask(id) {
    return api.delete(`/tasks/${id}`);
}

export function runTask(id) {
    return api.post(`/tasks/${id}/run`);
}
