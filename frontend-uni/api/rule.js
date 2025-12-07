import { api } from '@/common/http.js';

export function getSensorRules() {
    return api.get('/rules/sensor');
}
