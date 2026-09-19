<template>
  <div class="about-page">
    <PageHero title="关于花卉识别" subtitle="认识身边的花，从一张照片开始" />
    <div class="container py-5" id="about-project">
      <div class="guide-card p-4 mb-4">
        <h2>保留熟悉的操作，开始识花</h2>
        <p>支持单张照片、批量上传和摄像头识别。登录后可查看识别历史，管理后台可查看花卉类别分布。</p>
        <p>当前支持风铃草、康乃馨、雏菊、蒲公英、薰衣草、百合、荷花、玫瑰、向日葵和郁金香，共 10 类。</p>
      </div>
      <div class="guide-card p-4 mb-4">
        <h2>怎样获得更好的结果</h2>
        <p>让一朵主要花卉占据画面中心，保持清晰、自然光照，尽量减少遮挡。结果表示最可能的候选类别，不是确定结论。</p>
        <p>模型只能在这 10 类中选择，其他花种、非花图片也可能得到高置信度结果。当前不提供多花定位或未知类别的可靠判断。</p>
      </div>
      <div class="guide-card p-4">
        <h2>模型说明</h2>
        <p>本站使用本地部署的 ResNet18 花卉识别模型，所有推理均在本机完成，不调用任何外部识别接口，图片数据不会离开本机。</p>
        <p>模型针对上述 10 类花卉优化，返回最可能的候选类别和置信度，结果仅供参考。</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import PageHero from '@/components/PageHero.vue'
import '../styles/pages/about.css'
</script>
