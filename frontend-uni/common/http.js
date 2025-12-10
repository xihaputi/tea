const BASE_URL = 'http://127.0.0.1:8000';

const request = (method, url, data = {}) =>
  new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token');
    const header = {};
    if (token) {
      header['Authorization'] = token;
    }

    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          uni.removeStorageSync('token');
          uni.showToast({ title: '????', icon: 'none' });
          reject(res);
        } else {
          reject(res);
        }
      },
      fail: reject,
    });
  });

const upload = (url, filePath, name = 'file', formData = {}) =>
  new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token');
    const header = {};
    if (token) {
      header['Authorization'] = token;
    }

    uni.uploadFile({
      url: `${BASE_URL}${url}`,
      filePath,
      name,
      formData,
      header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(res.data));
        } else {
          reject(res);
        }
      },
      fail: reject,
    });
  });

export const api = {
  get: (url, data) => request('GET', url, data),
  post: (url, data) => request('POST', url, data),
  put: (url, data) => request('PUT', url, data),
  delete: (url, data) => request('DELETE', url, data),
  upload,
};
