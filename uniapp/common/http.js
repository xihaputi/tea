const BASE_URL = process.env.UNI_APP_API_BASE || 'http://localhost:5173';

const request = (method, url, data = {}) =>
  new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data);
        } else {
          reject(res);
        }
      },
      fail: reject,
    });
  });

const upload = (url, filePath, name = 'file', formData = {}) =>
  new Promise((resolve, reject) => {
    uni.uploadFile({
      url: `${BASE_URL}${url}`,
      filePath,
      name,
      formData,
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
  upload,
};

