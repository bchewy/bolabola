<template>
  <NavBar />
  <div class="events-view">
    <h1>Matches</h1>
    <p class="lead text-dark">Find the latest games here!</p>

    <div class="container-fluid mt-3">
      <div class="row gx-3 gy-3">
        <div class="col col-xs-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <div class="card"  @click="$router.push('/views/eventItem')">
              <div class="card-body">
                <!-- Your card content goes here -->
                <h5 class="card-title">Manchester United vs Liverpool</h5>
                <p class="card-text">October 23, 2023, 8:00 PM</p>
              </div>
            </div>
          <!-- <EventsCard class="EventsCard" /> -->
        </div>
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
  width: 300px;
  /* Adjust width as needed */
}

.card h2 {
  margin-top: 0;
}

.card p {
  margin-bottom: 0;
}
</style>

