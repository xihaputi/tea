<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="eyebrow">茶园管理</div>
        <div class="title">茶园总览</div>
        <div class="sub">统一视图管理茶园、地块与设备情况</div>
      </div>
      <el-button type="primary" icon="Plus">新增茶园</el-button>
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
          <el-button type="primary" icon="Search">搜索</el-button>
          <el-button icon="Refresh">重置</el-button>
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
            <el-button link type="success">绑定设备</el-button>
            <el-button link type="danger">停用</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination background layout="prev, pager, next" :total="100" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const queryParams = reactive({ name: '', company: '' })

const tableData = ref([
  { id: 101, name: '西湖龙井一号基地', address: '杭州市西湖区灵隐路88号', plotCount: 5, onlineCount: 12, totalCount: 15, manager: '张三' },
  { id: 102, name: '安吉白茶示范园', address: '湖州市安吉县递铺街道', plotCount: 8, onlineCount: 20, totalCount: 20, manager: '李四' },
])

const goDetail = (id) => {
  router.push(`/tea-garden/detail/${id}`)
}
</script>

<style scoped>
.page { padding: 20px; background: linear-gradient(180deg, #f7f9fb 0%, #f2f6f9 100%); min-height: 100%; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.eyebrow { font-size: 13px; color: #8c9ba8; letter-spacing: 1px; text-transform: uppercase; }
.title { font-size: 26px; font-weight: 700; color: #1f2a44; }
.sub { color: #6b7785; margin-top: 4px; }
.card { background: #fff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); padding: 16px; margin-bottom: 16px; }
.filters { margin-bottom: 16px; }
.tag.success { color: #16c06e; font-weight: 600; }
.pagination { margin-top: 16px; text-align: right; }
</style>
