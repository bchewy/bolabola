<template>
  <NavBar />
  <div class="events-view">
    <h1>Events</h1>
    <p class="lead text-dark">Find the latest matches here!</p>
    <div class="card-container">
      <div class="card">
        <h2>xxxx</h2>
        <p>2 Mar 2024 - 9 Mar 2024</p>
      </div>
      <div class="card">
        <h2>yyyy</h2>
        <p>3 Apr 2024 - 6 Apr 2024</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/Navbar.vue';
export default {
  name: "EventsView",
  // Add your component's logic here
  components: {
    NavBar,
    // LearnMore,
    // Footer,
  }
}
</script>

<style scoped>
.events-view {
  text-align: center;
  margin-top: 50px;
}

.card-container {
  display: flex;
  justify-content: center;
}

.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 300px; /* Adjust width as needed */
}

.card h2 {
  margin-top: 0;
}

.card p {
  margin-bottom: 0;
}
</style>

