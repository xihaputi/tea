<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="eyebrow">茶园管理</div>
        <div class="title">茶园总览</div>
        <div class="sub">统一视图管理茶园、地块与设备情况</div>
      </div>
      <el-button type="primary" icon="Plus" @click="handleAdd">新增茶园</el-button>
    </div>

    <div class="filters card">
      <el-form :inline="true" :model="queryParams" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="queryParams.name" placeholder="输入茶园名称" clearable />
        </el-form-item>
        <el-form-item label="所属">
          <el-select v-model="queryParams.company" placeholder="选择合作社" clearable>
            <el-option label="西湖集团" value="xh" />
            <el-option label="安吉白茶合作社" value="aj" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card">
      <el-table :data="tableData" style="width: 100%" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="茶园名称" min-width="180" />
        <el-table-column prop="address" label="位置" show-overflow-tooltip />
        <el-table-column prop="plotCount" label="地块数" width="90" />
        <el-table-column label="在线设备" width="140">
          <template #default="{ row }">
            <span class="tag success">{{ row.onlineCount }}</span> / {{ row.totalCount }}
          </template>
        </el-table-column>
        <el-table-column prop="manager" label="负责人" width="120" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goDetail(row.id)">详情</el-button>
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="success" @click="handleBindDevice(row)">绑定设备</el-button>
            <el-button link type="danger" @click="handleDelete(row)">停用</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination 
          background 
          layout="prev, pager, next" 
          :total="total" 
          v-model:current-page="queryParams.page"
          :page-size="queryParams.size"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑茶园' : '新增茶园'" width="500px">
      <el-form :model="form" label-width="80px" ref="formRef" :rules="rules">
        <el-form-item label="茶园名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入茶园名称" />
        </el-form-item>
        <el-form-item label="所属公司" prop="company">
          <el-select v-model="form.company" placeholder="请选择" style="width: 100%">
            <el-option label="西湖集团" value="xh" />
            <el-option label="安吉白茶合作社" value="aj" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人" prop="manager">
          <el-input v-model="form.manager" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="联系地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item label="占地面积" prop="area">
          <el-input v-model.number="form.area" placeholder="请输入面积">
            <template #append>亩</template>
          </el-input>
        </el-form-item>
        <el-form-item label="地理位置" required>
            <el-row :gutter="10" style="width: 100%">
                <el-col :span="10">
                    <el-input v-model="form.longitude" placeholder="经度" readonly />
                </el-col>
                <el-col :span="10">
                    <el-input v-model="form.latitude" placeholder="纬度" readonly />
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" icon="Location" @click="openMapDialog" style="width: 100%">选点</el-button>
                </el-col>
            </el-row>
        </el-form-item>
        <el-form-item label="摄像头" prop="camera_url">
            <el-input v-model="form.camera_url" placeholder="RTSP/HLS 视频流地址" />
        </el-form-item>
        <el-form-item label="描述信息" prop="desc">
          <el-input v-model="form.desc" type="textarea" rows="3" placeholder="请输入描述信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 绑定设备弹窗 -->
    <el-dialog v-model="bindDialogVisible" title="绑定设备" width="600px">
      <div class="mb-4 text-gray-500">请选择要绑定到该茶园的设备：</div>
      <el-table ref="bindTableRef" :data="unboundDevices" style="width: 100%" height="300" @selection-change="val => selectedDevices = val.map(v => v.id)">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="设备名称" />
        <el-table-column prop="sn" label="序列号" />
        <el-table-column prop="status" label="状态">
             <template #default="{ row }">
                <el-tag size="small" :type="row.status === 'online' ? 'success' : 'info'">{{ row.status }}</el-tag>
             </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="bindDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitBindDevice" :loading="bindLoading">确认绑定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 地图选点弹窗 -->
    <el-dialog v-model="mapDialogVisible" title="地图选点" width="800px" top="5vh" @opened="initSelectMap">
        <div style="position: relative;">
            <div style="margin-bottom: 10px; display: flex; gap: 10px;">
                <el-input v-model="mapSearchKeyword" placeholder="输入关键字搜索地址" id="map-search-input" clearable @keyup.enter="searchMapLocation" />
                <el-button type="primary" @click="searchMapLocation">搜索</el-button>
            </div>
            <div id="select-map-container" style="width: 100%; height: 500px; border-radius: 4px; border: 1px solid #dcdfe6;"></div>
            <div style="margin-top: 10px; font-size: 13px; color: #666;">
                当前选中: 经度 {{ tempLng || '-' }}, 纬度 {{ tempLat || '-' }}
            </div>
        </div>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="mapDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="confirmMapSelection" :disabled="!tempLat">确定使用该位置</el-button>
            </span>
        </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTeaGardenList, createTeaGarden, updateTeaGarden, deleteTeaGarden } from '@/api/tea-garden'
import { getDeviceList, updateDevice } from '@/api/device'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const queryParams = reactive({ 
  name: '', 
  company: '',
  page: 1,
  size: 10
})
const tableData = ref([])
const total = ref(0)
const loading = ref(false)

// 新增/编辑相关
const dialogVisible = ref(false)
const submitting = ref(false)
const isEdit = ref(false)
const currentId = ref(null)
const formRef = ref(null)
const form = reactive({
  name: '',
  company: '',
  manager: '',
  address: '',
  area: null,
  latitude: null,
  longitude: null,
  camera_url: '',
  desc: ''
})

const rules = {
  name: [{ required: true, message: '请输入茶园名称', trigger: 'blur' }],
  company: [{ required: true, message: '请选择所属公司', trigger: 'change' }],
  area: [
    { type: 'number', message: '必须为数字值', trigger: 'blur', transform: (value) => Number(value) }
  ]
}

// 绑定设备相关
const bindDialogVisible = ref(false)
const bindLoading = ref(false)
const unboundDevices = ref([])
const selectedDevices = ref([])
const currentBindGardenId = ref(null)
const bindTableRef = ref(null)

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getTeaGardenList(queryParams)
    if (res) {
      tableData.value = res.list || []
      total.value = res.total || 0
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  fetchData()
}

const handleReset = () => {
  queryParams.name = ''
  queryParams.company = ''
  queryParams.page = 1
  fetchData()
}

const handlePageChange = (page) => {
  queryParams.page = page
  fetchData()
}

const goDetail = (id) => {
  router.push(`/tea-garden/detail/${id}`)
}

// 新增/编辑逻辑
const handleAdd = () => {
  isEdit.value = false
  currentId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  currentId.value = row.id
  form.name = row.name
  form.company = row.company
  form.manager = row.manager
  form.address = row.address
  form.area = row.area
  form.latitude = row.latitude
  form.longitude = row.longitude
  form.camera_url = row.camera_url
  form.desc = row.desc
  dialogVisible.value = true
}

const resetForm = () => {
  form.name = ''
  form.company = ''
  form.manager = ''
  form.address = ''
  form.area = null
  form.latitude = null
  form.longitude = null
  form.camera_url = ''
  form.desc = ''
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        if (isEdit.value) {
          await updateTeaGarden(currentId.value, form)
          ElMessage.success('更新成功')
        } else {
          await createTeaGarden(form)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error) {
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 删除逻辑
const handleDelete = (row) => {
  ElMessageBox.confirm('确定要停用该茶园吗？此操作不可恢复', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteTeaGarden(row.id)
      ElMessage.success('已停用')
      fetchData()
    } catch (error) {
      console.error(error)
    }
  })
}

// 绑定设备逻辑
// 绑定设备逻辑
const handleBindDevice = async (row) => {
  currentBindGardenId.value = row.id
  bindDialogVisible.value = true
  selectedDevices.value = []
  // 获取所有设备列表
  try {
    const res = await getDeviceList({ page: 1, size: 1000 })
    unboundDevices.value = res.list || []
    
    // 预选中已绑定的设备
    // 需要等待 DOM 更新后操作表格
    setTimeout(() => {
        if (bindTableRef.value) {
            bindTableRef.value.clearSelection()
            unboundDevices.value.forEach(device => {
                if (device.garden_id === row.id) {
                    bindTableRef.value.toggleRowSelection(device, true)
                }
            })
        }
    }, 100)
  } catch (error) {
    console.error(error)
  }
}

const submitBindDevice = async () => {
  bindLoading.value = true
  try {
    const promises = []
    unboundDevices.value.forEach(device => {
        const isSelected = selectedDevices.value.includes(device.id)
        const isOriginallyBound = device.garden_id === currentBindGardenId.value
        
        if (isSelected && !isOriginallyBound) {
            // 新选中：绑定到当前茶园
            promises.push(updateDevice(device.id, { garden_id: currentBindGardenId.value }))
        } else if (!isSelected && isOriginallyBound) {
            // 取消选中：解绑
            promises.push(updateDevice(device.id, { garden_id: null }))
        }
    })
    
    if (promises.length > 0) {
        await Promise.all(promises)
        ElMessage.success('设备绑定状态已更新')
    } else {
        ElMessage.info('未做任何修改')
    }
    
    bindDialogVisible.value = false
    fetchData() // 刷新列表以更新在线设备数等统计
  } catch (error) {
    console.error(error)
    ElMessage.error('操作失败，请重试')
  } finally {
    bindLoading.value = false
  }
}



// 地图选点相关
const mapDialogVisible = ref(false)
const mapSearchKeyword = ref('')
const tempLat = ref(null)
const tempLng = ref(null)
let selectMap = null
let selectMarker = null
let placeSearch = null

const openMapDialog = () => {
    mapDialogVisible.value = true
    tempLat.value = form.latitude
    tempLng.value = form.longitude
}

const initSelectMap = () => {
    if (!window.AMap) {
        setTimeout(initSelectMap, 500)
        return
    }
    
    // 默认杭州
    const center = (tempLng.value && tempLat.value) ? [tempLng.value, tempLat.value] : [120.15, 30.28]
    
    selectMap = new window.AMap.Map('select-map-container', {
        zoom: 12,
        center: center,
        viewMode: '3D'
    })

    // 点击选点
    selectMap.on('click', (e) => {
        updateMarker(e.lnglat.getLng(), e.lnglat.getLat())
    })

    // 如果已有坐标，显示标记
    if (tempLng.value && tempLat.value) {
        updateMarker(tempLng.value, tempLat.value)
    }

    // 加载搜索插件
    window.AMap.plugin(['AMap.PlaceSearch'], function() {
        placeSearch = new window.AMap.PlaceSearch({
            pageSize: 5,
            pageIndex: 1,
            city: "010", // 默认城市
            citylimit: false,
            map: selectMap,
            panel: "panel"
        });
    });
}

const updateMarker = (lng, lat) => {
    tempLng.value = parseFloat(lng.toFixed(6))
    tempLat.value = parseFloat(lat.toFixed(6))
    
    if (selectMarker) {
        selectMarker.setPosition([lng, lat])
    } else {
        selectMarker = new window.AMap.Marker({
            position: [lng, lat],
            map: selectMap
        })
    }
}

const searchMapLocation = () => {
    if (!placeSearch || !mapSearchKeyword.value) return
    placeSearch.search(mapSearchKeyword.value, (status, result) => {
        if (status === 'complete' && result.info === 'OK') {
            // 搜索成功，PlaceSearch 会自动在地图上标注，我们取第一个结果
            if (result.poiList.pois.length > 0) {
                const poi = result.poiList.pois[0]
                updateMarker(poi.location.lng, poi.location.lat)
                selectMap.setCenter([poi.location.lng, poi.location.lat])
                selectMap.setZoom(15)
            }
        } else {
            ElMessage.warning('未找到相关地址')
        }
    })
}

const confirmMapSelection = () => {
    form.latitude = tempLat.value
    form.longitude = tempLng.value
    mapDialogVisible.value = false
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.page { 
  padding: 24px; 
  background: #f0f2f5; 
  min-height: 100vh; 
}
.page-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 24px; 
  background: #fff;
  padding: 20px 24px;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.eyebrow { font-size: 12px; color: #909399; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
.title { font-size: 24px; font-weight: 600; color: #303133; }
.sub { color: #606266; font-size: 14px; margin-top: 4px; }
.card { 
  background: #fff; 
  border-radius: 8px; 
  box-shadow: 0 1px 2px rgba(0,0,0,0.03); 
  padding: 24px; 
  margin-bottom: 24px; 
}
.filters { margin-bottom: 16px; }
.tag.success { color: #67c23a; font-weight: 600; }
.pagination { margin-top: 24px; text-align: right; }
</style>
