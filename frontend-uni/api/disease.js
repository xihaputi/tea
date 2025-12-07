import { api } from '@/common/http.js';

export function detectDisease(filePath, plotId) {
    // api.upload(url, filePath, name, formData)
    return api.upload('/disease/detect', filePath, 'file', {
        'plot_id': plotId || ''
    });
}
