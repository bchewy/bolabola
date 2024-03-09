<template>
    <NavBar />
    <div class="about-view d-flex flex-column justify-content-center align-items-center">
      <h1 class="text-center">John Doe's Profile page</h1>
      <p class="lead text-dark text-center">Shows tickets bought</p>
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
  </style>
  

<!-- should have some way of showing the ticket bought, and a refund button right next to it only if the match is less than 24hours away. THANKS -->