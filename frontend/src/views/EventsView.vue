<template>
  <div class="events-view">
    <h1>Events</h1>
    <p>Find the latest shows here!</p>
    <div class="card-container">
      <div class="card">
        <h2>Taylor Swift | Eras Tour</h2>
        <p>2 Mar 2024 - 9 Mar 2024</p>
      </div>
      <div class="card">
        <h2>Bruno Mars Live in Singapore</h2>
        <p>3 Apr 2024 - 6 Apr 2024</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EventsView",
  // Add your component's logic here
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

