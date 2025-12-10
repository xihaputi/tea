<script>
export default {
    onLaunch() {
    console.log('App Launch');
    // Check login status
    const token = uni.getStorageSync('token');
    if (!token) {
      // Use reLaunch to clear page stack and go to login
      uni.reLaunch({
        url: '/pages/login/index'
      });
    }
  },
  onShow() {
    console.log('App Show');
    // Prefetch default weather on app open (silently caching it)
    // Only if logged in (token exists)
    const token = uni.getStorageSync('token');
    if (token) {
        // Dynamic import to avoid circular dependency issues at top level if any, 
        // though typically fine. But let's just use require or import at top if possible.
        // For simple Vue 2/3 in UniApp, standard import at top is better.
        // But here we are inside the object, let's use the API if imported.
        // We will add import at the top.
        // prefetch 'ÐÅÑô'
        import('@/api/weather.js').then(({ getWeather }) => {
            getWeather('ÐÅÑô').catch(e => console.log('Prefetch failed', e));
        });
    }
  },
  onHide() {
    console.log('App Hide');
  },
};
</script>

<style lang="scss">
@import './uni.scss';
page {
  background: #f6f8fb;
  color: #1f2933;
}
</style>
