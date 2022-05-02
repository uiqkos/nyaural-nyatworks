<template>
  <div v-for="group in this.groups" :key="group">
    <a
        class="nya-remove-shadow nya-a-2 nya-text"
        data-bs-toggle="collapse"
        :href="'#' + group.name"
        role="button"
        aria-expanded="false"
        :aria-controls="group.name">
      {{ group.header }}
    </a>

    <div :id="group.name" class="collapse container" style="border-left: 1px solid #FF8500">
      <div class="accordion-body">
        <div class="row" v-if="group.models.length > 0">
          <div class="col container">
            <div class="row">
              <div class="col">
                Модель
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <span class=""> нет данных</span>
          <img src="https://c.tenor.com/lqtU1G4aaqIAAAAi/yom-dance.gif" alt="dancing-cat" height="100"
               width="100">
        </div>
        <div class="row align-items-start" style="margin-top: 10px">
          <div class="col container">
            <div class="form-check" v-for="model in group.models" :key="model">
              <input class="form-check-input" type="radio" :value="model.local_name"
                     @input="$emit('update:' + group.name, $event.target.value)"
                     :name="group.name" :id="'flexRadio-' + model.local_name">
              <label class="row form-check-label" :for="'flexRadio-' + model.local_name">
                <div class="col">
                  {{ model.name }}
                  <span
                      data-bs-toggle="tooltip"
                      data-bs-html="true"
                      data-bs-placement="top"
                      title=""
                  >
                    <a href="#">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                           class="bi bi-info-circle" viewBox="0 0 16 16">
                        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"></path>
                        <path
                            d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"></path>
                      </svg>
                    </a>
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div>
    <a
        class="nya-remove-shadow nya-a-2 nya-text"
        style=""
        data-bs-toggle="collapse"
        href="#interpreter-container"
        role="button"
        aria-expanded="false"
        aria-controls="interpreter-container">
      Дополнительные параметры
    </a>

    <div id="interpreter-container" class="collapse container" style="border-left: 1px solid #FF8500">
      <div class="accordion-body">
        <div class="col">
          <div class="form-check">
            <input class="form-check-input" type="radio" value="emoji"
                   name="interpreter" id="flexRadio-emoji">
            <label class="row form-check-label" for="flexRadio-emoji">
              <div>перевод в эмодзи 🤬😀</div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Api from "@/Api";

export default {
  name: "PredictParams",
  data() {
    return {
      groups: [
        {
          name: 'toxic',
          header: 'Токсичность',
          models: []
        },
        {
          name: 'sentiment',
          header: 'Эмоциональность',
          models: []
        },
        {
          name: 'sarcasm',
          header: 'Саркастичность',
          models: []
        }
      ],
    }
  },
  props: {
    toxic: String,
    sentiment: String,
    sarcasm: String
  },
  created() {
    for (let i = 0; i < this.groups.length; i += 1) {
      Api.allModels().then(
          value => this.groups[i].models =
              value.data.filter(m => m.target === this.groups[i].name)
      )
    }
    console.log(this.groups)
  }
}
</script>

<style scoped>

</style>