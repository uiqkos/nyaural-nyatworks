<template>
  <div style="margin: 1%; padding: 1%">
    <SingleComment :comment="this.comment" :grads="this.grads"/>
    <div class="row" :gutter="20">
      <div class="col">
        <div v-for="(comment, idx) in this.comments" :key="idx">
          <div v-if="comment.text !== '' || comment.level === 0" :style="'margin-left:' + 50 + 'px'">
            <CommentEntity :comment="comment"
                           :level="comment.level"
                           :grads="this.grads"
                           :parent-request-params="this.requestParams"/>
          </div>
        </div>
        <a
            class="nya-text nya-a-2 nya-header-sm"
            v-if="this.comments.length < comment.comments"
            v-on:click="expandAction"
            style="
              margin-top: 1%;
              margin-left: 1%;
              color: #f26a8d;
            ">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
               class="bi bi-arrow-return-right" viewBox="0 0 16 16">
            <path fill-rule="evenodd"
                  d="M1.5 1.5A.5.5 0 0 0 1 2v4.8a2.5 2.5 0 0 0 2.5 2.5h9.793l-3.347 3.346a.5.5 0 0 0 .708.708l4.2-4.2a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 8.3H3.5A1.5 1.5 0 0 1 2 6.8V2a.5.5 0 0 0-.5-.5z"/>
          </svg>
          комментарии
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import SingleComment from "@/components/SingleComment";
import Api from "@/Api";

export default {
  name: "CommentEntity",
  components: {SingleComment},
  props: ['comment', 'level', 'grads', 'parentRequestParams'],
  data() {
    return {
      comments: [],
      requestParams: null,
      expandAction: null,
    }
  },
  created() {
    this.requestParams = JSON.parse(JSON.stringify(this.parentRequestParams))
    this.requestParams.expand += this.comment.id + '/'
    this.requestParams.per_page = 3
    this.requestParams.page = 1

    let that = this
    this.expandAction = function () {
      that.expand()
      that.expandAction = that.nextPage
    }
  },
  methods: {
    async expand() {
      const data = await Api.predictParams(this.requestParams)

      for (let item of data.items) {
        this.comments.push(item)
      }

      console.log(this.comments)

    },
    nextPage() {
      this.requestParams.page += 1
      this.expand()
    }
  },
  async nextPage() {
    this.request.page += 1
    await this.expand()
  }
}
</script>

<style scoped>

</style>