<template>
  <NavBar />
  <div class="about-view d-flex flex-column justify-content-center align-items-center">
    <h1 class="text-center">Score Your Seats, Secure Your Spot!</h1>
    <p class="lead text-dark text-center">TicketBoost is a comprehensive platform designed to streamline the process of ticket sales, distribution, and management for football matches. It provides features such as online ticket purchasing and refund, seat selection, real-time videos, and secure payment processing. This platform offers convenience, efficiency, and security throughout the ticketing process. By automating various tasks and providing a user-friendly interface, TicketBoost enhances the overall experience for fans while optimizing revenue generation and administrative processes for event organizers.</p>
</div>
</template>

<script>
import NavBar from '../components/Navbar.vue';
export default {
  name: "AboutView",
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
