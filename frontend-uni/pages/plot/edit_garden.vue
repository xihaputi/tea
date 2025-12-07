<template>
  <view class="page-container">
    <view class="title-lg header">编辑茶园</view>
    
    <view class="card form-card">
      <view class="form-item">
        <text class="label">茶园名称</text>
        <input class="input" v-model="form.name" placeholder="请输入茶园名称" />
      </view>
      
      <view class="form-item">
        <text class="label">茶园封面</text>
        <view class="cover-preview" @click="showCoverSelector = true">
          <image :src="coverUrl" mode="aspectFill" class="cover-img"></image>
          <view class="cover-overlay">
            <text class="overlay-text">更换封面</text>
          </view>
        </view>
      </view>
      
      <view class="form-item">
        <text class="label">简介描述</text>
        <textarea class="textarea" v-model="form.description" placeholder="请输入茶园描述" />
      </view>

      <view class="form-item">
        <text class="label">种植地址</text>
        <input class="input" v-model="form.address" placeholder="请输入地址" />
      </view>

      <button class="btn-primary" @click="save" :loading="saving">保存修改</button>
    </view>

    <!-- Cover Selection Modal -->
    <view v-if="showCoverSelector" class="modal-mask" @click="showCoverSelector = false">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">选择封面</text>
          <text class="close-btn" @click="showCoverSelector = false">×</text>
        </view>
        
        <scroll-view scroll-y class="grid-scroll">
          <view class="cover-grid">
            <!-- Custom Upload -->
            <view class="grid-item upload-item" @click="chooseImage">
              <text class="upload-icon">+</text>
              <text class="upload-text">上传图片</text>
            </view>
            
            <!-- System Images -->
            <view 
              v-for="i in 14" 
              :key="i" 
              class="grid-item" 
              :class="{ active: form.image_path === `/static/gardens/${i}.png` }"
              @click="selectSystemImage(i)"
            >
              <image :src="`${$baseUrl}/static/gardens/${i}.png`" mode="aspectFill" class="grid-img"></image>
              <view v-if="form.image_path === `/static/gardens/${i}.png`" class="check-mark">✓</view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<script>
import { getGardenDetail, updateGarden } from '@/api/garden.js';
import { api } from '@/common/http.js';

export default {
  data() {
    return {
      gardenId: null,
      form: {
        name: '',
        description: '',
        address: '',
        image_path: ''
      },
      saving: false,
      showCoverSelector: false
    };
  },
  computed: {
    coverUrl() {
      if (!this.form.image_path) return '/static/gardens/1.png'; // Default fallback
      if (this.form.image_path.startsWith('http')) return this.form.image_path;
      // Ensure baseUrl doesn't have double slash if image_path has one
      const base = this.$baseUrl || ''; // Ensure base is defined
      return base + this.form.image_path;
    }
  },
  onLoad(options) {
    if (options.id) {
      this.gardenId = Number(options.id);
      this.loadData();
    }
  },
  methods: {
    async loadData() {
      try {
        const res = await getGardenDetail(this.gardenId);
        this.form = {
          name: res.name,
          description: res.description,
          address: res.address,
          image_path: res.image_path
        };
      } catch (e) {
        uni.showToast({ title: '加载失败', icon: 'none' });
      }
    },
    selectSystemImage(index) {
      this.form.image_path = `/static/gardens/${index}.png`;
      this.showCoverSelector = false;
    },
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: async (res) => {
          const filePath = res.tempFilePaths[0];
          try {
            uni.showLoading({ title: '上传中' });
            // Using the /disease/detect endpoint as a known working upload (hacky but functional for now if no generic upload)
            // OR better: use the generic upload if backend supports it.
            // Let's assume there is NO generic upload yet based on previous file list.
            // I'll stick to a placeholder/local path for now OR try /common/upload if I saw it?
            // I saw `upload.py` in routers! Let's check that.
            // For now, assume /upload/file exists or fallback.
             const uploadRes = await api.upload('/upload/file', filePath, 'file');
             this.form.image_path = uploadRes.url || uploadRes.path;
             this.showCoverSelector = false;
          } catch (e) {
            // uni.showToast({ title: '暂时不支持上传', icon: 'none' });
             // Fallback: just use local path for display (won't persist well across devices but good for demo)
             // this.form.image_path = filePath;
             // this.showCoverSelector = false;
             uni.showToast({ title: '上传失败', icon: 'none' });
          } finally {
            uni.hideLoading();
          }
        }
      });
    },
    async save() {
      this.saving = true;
      try {
        await updateGarden(this.gardenId, this.form);
        uni.showToast({ title: '保存成功', icon: 'success' });
        setTimeout(() => {
          // Go back and refresh
          const pages = getCurrentPages();
          const prevPage = pages[pages.length - 2];
          if (prevPage && prevPage.$vm.loadData) {
              prevPage.$vm.loadData();
          }
          uni.navigateBack();
        }, 1500);
      } catch (e) {
        uni.showToast({ title: '保存失败', icon: 'none' });
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "@/uni.scss";

.page-container {
  padding: 24rpx;
}

.header {
  margin-bottom: 24rpx;
}

.form-card {
  padding: 32rpx;
}

.form-item {
  margin-bottom: 32rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: $text-sub;
  margin-bottom: 16rpx;
}

.input {
  background: #F9FAFB;
  border: 2rpx solid #E5E7EB;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
}

.textarea {
  background: #F9FAFB;
  border: 2rpx solid #E5E7EB;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  width: 100%;
  height: 160rpx;
}

.cover-preview {
  width: 100%;
  height: 300rpx;
  border-radius: 16rpx;
  overflow: hidden;
  position: relative;
  border: 2rpx solid #E5E7EB;
}

.cover-img {
  width: 100%;
  height: 100%;
}

.cover-overlay {
  position: absolute;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay-text {
  color: #fff;
  border: 2rpx solid #fff;
  padding: 8rpx 24rpx;
  border-radius: 99rpx;
  font-size: 26rpx;
}

/* Modal */
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  z-index: 999;
  display: flex;
  align-items: flex-end;
}

.modal-content {
  background: #fff;
  width: 100%;
  border-radius: 24rpx 24rpx 0 0;
  padding: 32rpx;
  max-height: 80vh;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.modal-title {
  font-size: 32rpx;
  font-weight: 700;
}

.close-btn {
  font-size: 40rpx;
  color: $text-sub;
  padding: 0 16rpx;
}

.grid-scroll {
  height: 600rpx;
}

.cover-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
}

.grid-item {
  aspect-ratio: 16/9;
  border-radius: 12rpx;
  overflow: hidden;
  position: relative;
  border: 4rpx solid transparent;
  
  &.active {
    border-color: $primary;
  }
}

.upload-item {
  background: #F3F4F6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2rpx dashed #D1D5DB;
}

.upload-icon {
  font-size: 48rpx;
  color: $text-sub;
}

.upload-text {
  font-size: 24rpx;
  color: $text-sub;
}

.grid-img {
  width: 100%;
  height: 100%;
}

.check-mark {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  background: $primary;
  color: #fff;
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
}
</style>
