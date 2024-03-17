<template>
  <NavBar />
  <div class="about-view d-flex flex-column justify-content-center align-items-center">
    <h1 class="text-center text-superblue">Streaming</h1>
    <p class="lead text-dark text-center">Tune in and experience the thrill of live football!</p>
</div>
</template>

<script>
import NavBar from '../components/Navbar.vue';
export default {
  name: "StreamingView",
  // Add your component's logic here
  components: {
    NavBar,
    // LearnMore,
    // Footer,
  }
}
</script>

<style scoped>
.about-view {
  text-align: center;
  margin-top: 50px;
}

.text-superblue{
  color: #5356FF;
}


</style>
