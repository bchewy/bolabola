<template>
  <div>
    <NavBar />
    <div class="events-view">
      <h1>Matches</h1>
      <p class="lead text-dark">Find the latest games here!</p>

      <div class="container-fluid mt-3">
        <div class="row gx-3 gy-3">
          <div v-for="match in matches" :key="match.id" class="col col-xs-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <div class="card" @click="displayMatchDetails(match)">
              <div class="card-body">
                <h5 class="card-title">{{ match.title }}</h5>
                <p class="card-text">{{ match.date }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavBar from '../components/Navbar.vue'; // Adjust the path as per your project structure

export default {
  components: {
    NavBar
  },
  data() {
    return {
      matches: [], // Initialize matches as an empty array
      selectedMatch: null // Initialize selectedMatch as null
    };
  },
  created() {
    this.fetchMatches(); 
  },
  methods: {
    fetchMatches() {
      axios.get('') // what is this bruh :(((((
        .then(response => {
          this.matches = response.data; 
        })
        .catch(error => {
          console.error('Error fetching matches:', error);
        });
    },
    displayMatchDetails(match) {
      this.selectedMatch = match; 
    }
  }
};
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

