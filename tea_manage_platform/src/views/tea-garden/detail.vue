<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTeaGardenDetail, getPlots, getGardenDevices } from '@/api/tea-garden'

const route = useRoute()
const activeTab = ref('plots')
const gardenId = route.params.id

// 表单数据
const form = reactive({
  name: '',
  address: '',
  area: '',
  desc: ''
})

// 地块数据
const plotsData = ref([])

// 设备数据
const deviceData = ref([])

const fetchDetail = async () => {
  if (!gardenId) return
  try {
    const res = await getTeaGardenDetail(gardenId)
    if (res) {
      Object.assign(form, res)
    }
  } catch (error) {
    console.error(error)
  }
}

const fetchPlots = async () => {
  if (!gardenId) return
  try {
    const res = await getPlots(gardenId)
    if (res) {
      plotsData.value = res
    }
  } catch (error) {
    console.error(error)
  }
}

const fetchDevices = async () => {
  if (!gardenId) return
  try {
    const res = await getGardenDevices(gardenId)
    if (res) {
      deviceData.value = res
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchDetail()
  fetchPlots()
  fetchDevices()
})
</script>

<style scoped>
.mb-20 { margin-bottom: 20px; }
.mb-10 { margin-bottom: 10px; }
.mr-3 { margin-right: 12px; }
.mr-1 { margin-right: 4px; }
.text-large { font-size: 18px; }
.font-600 { font-weight: 600; }
</style>