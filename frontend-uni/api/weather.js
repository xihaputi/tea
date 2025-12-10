import { api } from '@/common/http.js';

const CACHE_KEY_PREFIX = 'weather_cache_';
const CACHE_EXPIRY = 30 * 60 * 1000; // 30 minutes validity

/**
 * Get weather with caching strategy.
 * 1. Check valid cache.
 * 2. If valid, return cache immediately.
 * 3. If invalid/missing, fetch from API and update cache.
 * @param {string} location 
 * @param {boolean} forceRefresh 
 */
export function getWeather(location, forceRefresh = false) {
    return new Promise((resolve, reject) => {
        const key = CACHE_KEY_PREFIX + location;

        // 1. Try to read from cache
        if (!forceRefresh) {
            try {
                const cached = uni.getStorageSync(key);
                if (cached) {
                    const now = Date.now();
                    if (now - cached.timestamp < CACHE_EXPIRY) {
                        // Cache hit and valid
                        console.log('Weather cache hit:', location);
                        resolve(cached.data);
                        return; // Early return, don't fetch
                    }
                }
            } catch (e) {
                console.error('Cache read failed', e);
            }
        }

        // 2. Cache miss or expired: Fetch from API
        console.log('Weather fetch:', location);
        api.get('/api/weather', { location }).then(res => {
            if (res) {
                // Update cache
                try {
                    uni.setStorageSync(key, {
                        data: res,
                        timestamp: Date.now()
                    });
                } catch (e) {
                    console.error('Cache write failed', e);
                }
                resolve(res);
            } else {
                reject('No data');
            }
        }).catch(err => {
            // Optional: If fetch fails, try to return stale cache if exists?
            // For now, just reject or return null if strict.
            // User didn't specify stale-while-revalidate, but let's stick to fail if network fails first time.
            // But if we had expired cache, maybe we could return that? 
            // Let's implement simple cache: expired = gone.
            reject(err);
        });
    });
}
