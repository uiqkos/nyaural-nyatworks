<template>
  <div class="container">
    <div class="container justify-content-center mt-100 mb-100">
      <h1 class="nya-text" style="margin-top: 5%">Результаты анализа</h1>
        <span class="rounded-pill badge" :style="this.statsStyles.toxic.style">
          {{ this.statsStyles.toxic.label }}
          {{ this.statsStyles.toxic.value }}
        </span>
        <span class="rounded-pill badge" :style="this.statsStyles.sentiment.style">
          {{ this.statsStyles.sentiment.label }}
          {{ this.statsStyles.sentiment.value }}
        </span>
        <span class="rounded-pill badge" :style="this.statsStyles.sarcasm.style">
          {{ this.statsStyles.sarcasm.label }}
          {{ this.statsStyles.sarcasm.value }}
        </span>
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="comment-widgets m-b-20">
              <div v-for="(comment, idx) in this.comments" :key="idx">
                <div v-if="comment.text !== '' || comment.level === 0">
                  <div class="d-flex flex-row comment-row" :style="'margin-left:' + comment.level * 4 + '%'">
                    <div class="p-2">
                      <span class="round"><img :src="comment.author.photo" alt="user" width="50"></span>
                    </div>
                    <div class="comment-text w-100">
                      <h5>{{ comment.author.name }}</h5>
                      <div class="comment-footer" :id="'pills-' + idx">
                        <span class="date">{{ comment.date }}</span>

                        <span class="rounded-pill badge" :style="comment.styles.toxic.style">
                          {{ comment.styles.toxic.label }}
                          {{ comment.styles.toxic.value }}
                        </span>

                        <span class="rounded-pill badge" :style="comment.styles.sentiment.style">
                          {{ comment.styles.sentiment.label }}
                          {{ comment.styles.sentiment.value }}
                        </span>

                        <span class="rounded-pill badge" :style="comment.styles.sarcasm.style">
                          {{ comment.styles.sarcasm.label }}
                          {{ comment.styles.sarcasm.value }}
                        </span>
                      </div>
                      <p class="m-b-5 m-t-10 text-block">
                        {{ comment.text }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <div class=" justify-content-center align-content-center align-items-center">
      <a class="nya-a-2 " v-on:click="nextPage">Загрузить еще</a></div>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import Api from "@/Api";

export default {
  name: "ResultPage",
  data() {
    return {
      pages: 0,
      params: null,
      statsStyles: {},
      comments: []
    }
  },
  methods: {
    nextPage() {
      this.pages += 1
      Api.predict(
          this.params.input,
          this.params.text,
          this.params.toxic,
          this.params.sentiment,
          this.params.sarcasm,
          this.pages,
          5,
          true,
          true
      ).then(v =>
          this.comments = [this.comments.concat(v.data.items), this.statsStyles = v.data.styles][0]
      )
    }
  },
  created() {
    const route = useRoute()
    this.params = route.params
    this.nextPage()
  }
}
</script>

<style scoped>
.author-img {
  width: 46px;
  height: 46px;
  border-radius: 50%;
}

.card-no-border .card {
  border: 0px;
  border-radius: 4px;
  -webkit-box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05);
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.05)
}

.card-body {
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  padding: 1.25rem
}

.comment-widgets .comment-row {
  border-bottom: 1px solid rgba(120, 130, 140, 0.13);
  padding: 15px
}

.comment-text:hover {
  visibility: hidden
}

.comment-text:hover {
  visibility: visible
}

.label {
  padding: 3px 10px;
  line-height: 13px;
  color: #ffffff;
  font-weight: 400;
  border-radius: 4px;
  font-size: 75%
}

.round img {
  border-radius: 100%
}

.label-info {
  background-color: #1976d2
}

.label-success {
  background-color: green
}

.label-danger {
  background-color: #ef5350
}

.action-icons a {
  padding-left: 7px;
  vertical-align: middle;
  color: #99abb4
}

.action-icons a:hover {
  color: #1976d2
}

.mt-100 {
  margin-top: 100px
}

.mb-100 {
  margin-bottom: 100px
}
</style>