<template>
  <div class="text-center">
    <div class="logo-box">
      <h1 class="display-1 nya-text-header">
        <span class="nya" id="nya1" ref="nya1"></span><span ref="space1"></span>
        <span class="nya" id="nya2" ref="nya2"></span><span id="cursor" ref="cursor">|</span>
      </h1>
    </div>
  </div>
</template>

<script>
import {typingText} from '@/typingCat'


export default {
  name: "NyaLogo",
  methods: {
    bitCat() {
      typingText(
          ['nya1', 'nya2', 'nya3'],
          ['NYAURAL', 'NYATWORKS'],
          this.$refs.cursor,
          undefined,
          [this.$refs.space1]
      )
    }
  },
  mounted() {
    this.bitCat()
  }
}

</script>
