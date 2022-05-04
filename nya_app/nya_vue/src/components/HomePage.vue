<template>
  <NyaLogo/>
  <div class="container">
    <div class="p-2">
      <div class="container-fluid py-5">
        <h1 class="display-5 nya-text">Эмоциональный анализ</h1>
        <p class="col-md-8 fs-4">Анализируйте тональность, эмоциональность и токсичность текстов. Импортируйте данные
          из социальных сетей. Просматривайте характеристики моделей и историю обучения.</p>
        <router-link to="/predict" class="nya-a-2" type="button">
          провести анализ
        </router-link>
      </div>
    </div>

    <div class="row align-items-md-stretch">
      <div class="col-md-6">
        <div class="h-100 p-2">
          <h2 class="nya-text">Отчеты</h2>
          <p>Просматривайте отчеты по моделям, <br> препроцессорам и датасетам</p>
          <router-link to="/reports" class="nya-a-2" type="button">
            просмотреть отчеты
          </router-link>
        </div>
      </div>

      <div class="col-md-6">
        <div class="h-100 p-2">
          <h2 class="nya-text">Рейтинг</h2>
          <p>Результаты тестирования, на основе которых формируется рейтинг моделей.</p>
          <router-link to="/rating" class="nya-a-2" type="button">
            просмотреть рейтинг
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <div class="container" style="margin: 10%">
  </div>
  <router-view/>
</template>

<script>
import NyaLogo from "@/components/NyaLogo";

export default {
  name: "HomePage",
  components: {
    NyaLogo
  }
}
</script>
