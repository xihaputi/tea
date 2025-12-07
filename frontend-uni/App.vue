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
