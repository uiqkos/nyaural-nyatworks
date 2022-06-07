<template>
  <div class="row">
    <div class="col-auto">
      <img class="rounded-circle" style="width: 50px; height: 50px" :src="author.photo" alt="avatar"/>
    </div>
    <div class="col">
      <div class="row">
        <b>{{ author.name }}</b>
      </div>
      <div class="row row-cols-auto g-1">
        <div class="col">
          <span class="badge bg-secondary">{{ date }}</span>
        </div>

        <div class="col" v-for="style of styles" :key="style">
          <span :class="'badge ' +  'bg-' + style.tagType">
            {{ style.label }}
            {{ Math.round(style.value * 100) }}
          </span>
        </div>

      </div>
      <div class="fs-5">
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script>
import Utils from "@/utils";

export default {
  name: "SingleComment",
  props: ['comment', 'grads'],
  data() {
    return {
      text: this.comment.text,
      author: this.comment.author,
      date: this.comment.date,
      styles: []
    }
  },
  created() {
    console.log(this.comment)
    for (let [label, prediction] of Object.entries(this.comment.predictions)) {
      let predictionKeys = Object.keys(prediction)
      let predictionValues = Object.values(prediction)
      let idx = Utils.argmax(predictionValues)

      let grad = this.grads[label][predictionKeys[idx]]
      let tagType

      switch (grad) {
        case 0:
          tagType = 'success';
          break
        case 1:
          tagType = 'info';
          break
        case 2:
          tagType = 'danger';
          break
      }

      this.styles.push({
        'label': predictionKeys[idx],
        'value': predictionValues[idx],
        'tagType': tagType
      })

    }
  }
}
</script>

<style scoped>

</style>