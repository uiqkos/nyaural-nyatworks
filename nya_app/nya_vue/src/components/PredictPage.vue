<template>
  <div class="container">
    <form action="/result">
      <div class="container search" style="position: relative;">
        <div class="row">
          <div class="col-md-3 mb-3">
            <select
                id="input" class="nya-a-2 nya-remove-shadow text-center"
                name="input" v-model="params.input"
            >
              <option>auto</option>
              <option value="manual">ручной ввод текста</option>
              <option>vk</option>
              <option>twitter</option>
              <option>reddit</option>
              <option>youtube</option>
            </select>

          </div>

          <div class="col">
            <div class="input-group mb-3">
              <input type="text" class="form-control nya-remove-shadow" placeholder="" aria-label=""
                     aria-describedby="basic-addon2" style="border-bottom: 1px solid black; border-radius: 0"
                     v-model="params.text" name="text">
            </div>
          </div>
          <div class="col-md-3">
            <router-link :to="{name: 'result', params: this.params}">
              <button class="nya-remove-shadow nya-a-2" type="submit">провести анализ
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                     class="bi bi-arrow-right" viewBox="0 0 16 16">
                  <path fill-rule="evenodd"
                        d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"></path>
                </svg>
              </button>
            </router-link>
          </div>
        </div>
      </div>

      <h4 class="nya-text" style="padding-top: 30px">Настройка анализатора</h4>
      <PredictParams
          v-model="params"
          v-model:toxic="params.toxic"
          v-model:sentiment="params.sentiment"
          v-model:sarcasm="params.sarcasm"
      />
    </form>
  </div>
  <router-view/>
</template>

<script>
import PredictParams from "@/components/PredictParams";

export default {
  name: "PredictPage",
  components: {
    PredictParams
  },
  data() {
    return {
      params: {
        input: 'auto',
        text: '',
        toxic: null,
        sentiment: null,
        sarcasm: null,
      }
    }
  }
}
</script>

<style scoped>

</style>