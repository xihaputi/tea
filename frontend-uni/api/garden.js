import { api } from '@/common/http.js';

export function getGardenList(params) {
    return api.get('/tea-gardens', params);
}

export function getGardenDetail(id) {
    return api.get(`/tea-gardens/${id}`);
}

export function getGardenPlots(gardenId) {
    return api.get(`/tea-gardens/${gardenId}/plots`);
}

export function getGardenDevices(gardenId) {
    return api.get(`/tea-gardens/${gardenId}/devices`);
}

export function updateGarden(id, data) {
    return api.put(`/tea-gardens/${id}`, data);
}
