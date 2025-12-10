<template>
  <el-dialog
    v-model="visible"
    title="选择茶园封面"
    width="600px"
    :before-close="handleClose"
    append-to-body
  >
    <div class="image-grid">
      <div 
        v-for="i in 14" 
        :key="i"
        class="image-item"
        :class="{ active: selectedImage === `/static/gardens/${i}.png` }"
        @click="selectImage(`/static/gardens/${i}.png`)"
      >
        <img :src="`/static/gardens/${i}.png`" loading="lazy" />
        <div class="check-mark" v-if="selectedImage === `/static/gardens/${i}.png`">
          <el-icon><Check /></el-icon>
        </div>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Check } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: Boolean,
  currentImage: String
})

const emit = defineEmits(['update:modelValue', 'select'])

const visible = ref(false)
const selectedImage = ref('')

watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    selectedImage.value = props.currentImage || ''
  }
})

const handleClose = () => {
  visible.value = false
  emit('update:modelValue', false)
}

const selectImage = (path) => {
  selectedImage.value = path
}

const handleConfirm = () => {
  emit('select', selectedImage.value)
  handleClose()
}
</script>

<style scoped>
.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
  padding: 4px;
}

.image-item {
  position: relative;
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.image-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.image-item.active {
  border-color: #409EFF;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.check-mark {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #409EFF;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
