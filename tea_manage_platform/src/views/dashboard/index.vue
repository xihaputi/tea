<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6" v-for="i in 4" :key="i">
        <el-card shadow="never" class="modern-card hover-up">
          <div class="stat-item">
            <div class="icon-box">
              <el-icon><DataLine /></el-icon>
            </div>
            <div>
              <div class="text-gray-400 text-xs mb-1">监控指标 {{ i }}</div>
              <div class="text-2xl font-bold">1,20{{ i }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

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