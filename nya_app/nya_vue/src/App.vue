<template>
  <nav class="" style="padding-left: 10%; padding-right: 10%; padding-top: 1%">
    <router-link class="nya-text-header nya-a-1 nya-margin nya-header-md" to="/">Nyaural
      Nyatworks
    </router-link>
    <router-link class="nya-text nya-a-2 nya-margin nya-header-sm" to="/predict">Анализ</router-link>
    <router-link class="nya-text nya-a-2 nya-margin nya-header-sm" to="/reports">Отчеты</router-link>
    <!--    <router-link class="nya-text nya-a-2 nya-margin nya-header-sm" to="/rating">Рейтинг</router-link>-->
  </nav>
  <router-view/>
</template>

<script>

export default {
  name: 'App',
  watch: {
        $route: {
            immediate: true,
            handler(to, from_) {
              from_
                document.title = to.meta.title || 'Nyaural Nyatworks';
            }
        },
    }
}

</script>

<style>
.nya-header-sm {
  font-size: 25px;
  border-radius: 0
}

.nya-header-md {
  font-size: 30px;
  border-radius: 0
}

.nya-border {
  border-left: 1px solid var(--first-color);
}

.list-group {
  margin-bottom: 3%;
}

.nested {
  margin-left: 0.5%;
  margin-top: 0.3%;
}

.empty-search {
  margin-top: 15%;
}

.search {
  margin-top: 10%;
}

.navbar {
  margin-left: 10px;
  margin-right: 10px;
}

@font-face {
  font-family: 'electroharmonix';
  src: url(assets/fonts/electroharmonix.ttf);

}

@font-face {
  font-family: 'LiberationMono';
  src: url(assets/fonts/LiberationMono.ttf);
}

@font-face {
  font-family: 'EmperorOfJapan';
  src: url(assets/fonts/EmperorOfJapan-GW6O.otf);
}

@font-face {
  font-family: 'FujimaruRegular';
  src: url(assets/fonts/FujimaruRegular-WGYY.ttf);
}

@font-face {
  font-family: 'RenjiFreeTrial';
  src: url(assets/fonts/RenjiFreeTrial-d9gRV.otf);
}

@font-face {
  font-family: 'ZenzaiItacha';
  src: url(assets/fonts/ZenzaiItacha-vElZ.ttf);
}

:root {
  --first-color: #dd2d4a;
  /*--first-color: #5A189A;*/
  --second-color: #f26a8d;
  /*--second-color: #FF8500;*/
}

.nya-first-color {
  color: var(--first-color);
}

.nya-second-color {
  color: var(--second-color);
}

.nya-text-header {
  font-family: electroharmonix, serif;
}

.nya-text {
  font-family: LiberationMono, serif;
  text-decoration: underline 3px;
  text-decoration-color: var(--first-color);
}

.nya-complete {
  text-decoration: underline wavy 4px;
  text-decoration-color: var(--first-color);
}

.logo-box {
  padding-top: 9%;
  margin: 50px;
}

.nya-decoration-sm-1 {
  text-decoration: underline wavy 2px;
  font-weight: bold;
  text-decoration-color: var(--second-color);
}

.nya-decoration-sm-2 {
  text-decoration: underline wavy 2px;
  font-weight: bold;
  text-decoration-color: var(--first-color);
}

.nya-decoration-lg-1 {
  text-decoration: underline wavy 4px;
  /*font-weight: bold;*/
  text-decoration-color: var(--second-color);
}

.nya-decoration-lg-2 {
  text-decoration: underline wavy 4px;
  font-weight: bold;
  text-decoration-color: var(--first-color);
}

.nya-decoration-m-1 {
  text-decoration: underline wavy 3px;
  font-weight: bold;
  text-decoration-color: var(--second-color);
}

.nya-decoration-m-2 {
  text-decoration: underline wavy 3px;
  font-weight: bold;
  text-decoration-color: var(--first-color);
}

.nya-margin {
  margin-left: 10px;
  margin-right: 10px;
}

.nya-a-1 {
  /*border: 4px solid transparent;*/
  color: black;
  text-decoration: underline wavy 2px;
  text-decoration-color: transparent;
}

.nya-a-1:hover {
  color: black;
  text-decoration: underline wavy 2px;
  text-decoration-color: var(--second-color);
}

.nya-a-2 {
  color: black;
  font-size: large;
  text-decoration: underline 2px;
  text-decoration-color: transparent;
}

.nya-a-2:hover {
  color: black;
  font-size: large;
  text-decoration: underline 2px;
  text-decoration-color: var(--second-color);
}

.nya-remove-shadow:focus {
  box-shadow: unset;
  border: unset;
  background-color: transparent;
}

.nya-active.active {
  background-color: transparent !important;
  color: var(--second-color) !important;
}

.nya-remove-shadow {
  box-shadow: unset;
  border: unset;
  background-color: transparent;
}


.comment {
  /*border-left: 2px;*/
  border-radius: 0;
  border-bottom: 0;
  border-right: 0;
  border-top: 0;
  padding-left: 1%;
}

.nya-positive {
  background-color: rgba(127, 255, 189, 0.6);
  color: #444444;
}

.nya-negative {
  background-color: rgba(255, 127, 161, 0.56);
  color: #444444;
}


.nya-neutral {
  background-color: rgba(255, 229, 127, 0.56);
  color: #444444;
}

.text-block {
  white-space: pre-line;
}

</style>
