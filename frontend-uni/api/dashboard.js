import { api } from '@/common/http.js';

export function getDashboardStats() {
    return api.get('/dashboard/stats');
}
