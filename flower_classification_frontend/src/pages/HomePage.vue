<template>
  <div class="home-page">
    <!-- 英雄 Header -->
    <div class="hero-section">
      <div class="hero-content d-flex flex-column align-items-center">
        <h1 v-reveal class="hero-title text-center hero-fade-in anim-delay-2">🌸 花卉识别系统</h1>
        <p v-reveal class="hero-subtitle text-center hero-fade-in anim-delay-3">上传图片，AI 帮您快速识别花卉类别</p>
        <p v-reveal class="hero-description text-center hero-fade-in anim-delay-4">支持雏菊、蒲公英、玫瑰、向日葵和郁金香五类花卉</p>
        <div v-reveal class="hero-fade-in">
          <CommonButton
            @click="handleStart"
            theme="success"
            size="lg"
          >
            <i class="bi bi-play-circle me-2"></i>
            {{ isLoggedIn ? '立即开始识别' : '登录开始使用' }}
          </CommonButton>
        </div>
      </div>
    </div>

    <!-- 主内容 -->
    <div class="home-content-wrapper">

      <!-- 功能模块区 - 3 列并排 -->
      <div class="feature-scroll-section">
        <h1 v-reveal class="section-title hero-fade-in anim-delay-1">探索更多功能</h1>
        
        <div class="feature-scroll-container">
          <div class="feature-item">
            <div class="card feature-card card-bg-1"> <div class="card-overlay"></div>
              <div class="card-body d-flex flex-column justify-content-center align-items-center p-5">
                <div class="icon-box mb-4">
                  <i class="bi bi-clock-history feature-icon text-info"></i>
                </div>
                <h3 class="feature-description">
                  每一次识别都会被自动保存，<br>
                  清晰呈现您的识花足迹，<br>
                  让改变看得见。
                </h3>
                <common-button
                  @click="handleHistory"
                  theme="info"
                  size="md"
                >
                  {{ isLoggedIn ? '立即进入历史' : '登录查看历史' }}
                </common-button>
              </div>
            </div>
          </div>

          <div class="feature-item">
            <div class="card feature-card card-bg-2"> <div class="card-overlay"></div>
              <div class="card-body d-flex flex-column justify-content-center align-items-center p-5">
                <div class="icon-box mb-4">
                  <i class="bi bi-book feature-icon text-success"></i>
                </div>
                <h3 class="feature-description">
                  了解模型支持的花卉，<br>
                  查看五种花卉的中英文名称，<br>
                  从熟悉身边的花开始。
                </h3>
                <common-button
                  :href="'#classification-guide'"
                  theme="success"
                  size="md"
                  @click="handleHashClick"
                >
                  查看支持花卉
                </common-button>
              </div>
            </div>
          </div>

          <div class="feature-item">
            <div class="card feature-card card-bg-3"> <div class="card-overlay"></div>
              <div class="card-body d-flex flex-column justify-content-center align-items-center p-5">
                <div class="icon-box mb-4">
                  <i class="bi bi-person feature-icon text-primary"></i>
                </div>
                <h3 class="feature-description">
                  根据您的习惯进行个性化设置，<br>
                  统一管理账户信息与安全，<br>
                  一切井然有序。
                </h3>
                <common-button 
                  @click="handleProfile"
                  theme="primary"
                  size="md"
                >
                  {{ isLoggedIn ? '前往个人管理' : '登录管理资料' }}
                </common-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h1 v-reveal id="classification-guide" class="section-title">五类花卉百科</h1>
      <div class="classification-guide">
        <div class="row g-4">
          <div v-for="flower in flowers" :key="flower.id" class="col-lg-6">
            <article class="guide-card flower-encyclopedia-card p-4">
              <div class="d-flex justify-content-between align-items-start gap-3">
                <div>
                  <h5 class="mb-1">🌸 {{ flower.name }}</h5>
                  <p class="flower-name-en mb-2">{{ flower.name_en }}</p>
                </div>
                <span class="flower-season">{{ flower.season }}</span>
              </div>
              <p class="flower-summary">{{ flower.summary }}</p>
              <button class="flower-info-button" type="button" @click="openEncyclopedia(flower)">
                查看百科详情 <i class="bi bi-arrow-right"></i>
              </button>
            </article>
          </div>
        </div>
        <p class="text-center mt-4">请让一朵主要花卉清晰地出现在画面中。识别结果是候选判断，模型不具备可靠的非花图片拒识能力。</p>
      </div>

      <div v-if="selectedFlower" class="flower-modal-backdrop" role="presentation" @click.self="closeEncyclopedia">
        <section class="flower-modal" role="dialog" aria-modal="true" :aria-label="`${selectedFlower.name}百科`">
          <button class="flower-modal-close" type="button" aria-label="关闭百科" @click="closeEncyclopedia">×</button>
          <div class="flower-modal-icon">🌸</div>
          <p class="flower-modal-kicker">FLOWER ENCYCLOPEDIA</p>
          <h2>{{ selectedFlower.name }}</h2>
          <p class="flower-modal-name">{{ selectedFlower.name_en }}</p>
          <p class="flower-modal-description">{{ selectedFlower.summary }}</p>
          <div class="flower-modal-facts">
            <div><span>常见花期</span><strong>{{ selectedFlower.season }}</strong></div>
            <div><span>养护提示</span><strong>{{ selectedFlower.care }}</strong></div>
          </div>
          <p class="flower-modal-note">百科内容用于辅助了解识别结果，模型输出仍属于候选判断。</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import flowers from '../config/flowerLabels.json'
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useAuthModal } from '@/composables/useAuthModal' // Import useAuthModal
import CommonButton from '@/components/CommonButton.vue';
import '../styles/pages/home.css';

const router = useRouter()
const { isLoggedIn } = useAuth()
// Destructure openLogin and openProfile from useAuthModal
const { openLogin, openProfile } = useAuthModal() 
const selectedFlower = ref(null)

const openEncyclopedia = (flower) => {
  selectedFlower.value = flower
}

const closeEncyclopedia = () => {
  selectedFlower.value = null
}

const handleStart = () => {
  if (isLoggedIn.value) {
    router.push('/user/detect')
  } else {
    // Open login modal instead of redirecting
    openLogin() 
  }
}

const handleHistory = () => {
  if (isLoggedIn.value) {
    router.push('/user/history')
  } else {
    // Open login modal instead of redirecting
    openLogin()
  }
}

const handleProfile = () => {
  if (isLoggedIn.value) {
    // Open profile modal instead of redirecting
    openProfile()
  } else {
    // Open login modal instead of redirecting
    openLogin()
  }
}

const handleHashClick = () => {
  // Logic for hash link if needed, or keep as is in template
}
</script>
