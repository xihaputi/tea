<script setup>
import { ref, onMounted } from 'vue'
import { getStats } from '@/api/dashboard'

const statsData = ref([
  { label: '茶园总数', value: '-' },
  { label: '设备总数', value: '-' },
  { label: '今日告警', value: '-' },
  { label: '设备在线率', value: '-' }
])

const fetchData = async () => {
  try {
    const res = await getStats()
    if (res) {
      statsData.value = [
        { label: '茶园总数', value: res.gardenCount },
        { label: '设备总数', value: res.deviceCount },
        { label: '今日告警', value: res.alertCount },
        { label: '设备在线率', value: res.onlineRate }
      ]
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.modern-card {
  border: none;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  transition: all 0.3s;
}
.hover-up:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}
.stat-item { display: flex; align-items: center; gap: 15px; }
.icon-box { 
  width: 48px; height: 48px; border-radius: 12px; background: #e6fffb; color: #13c2c2;
  display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.text-2xl { font-size: 24px; }
.font-bold { font-weight: bold; }
</style>