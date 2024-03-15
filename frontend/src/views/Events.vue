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
      axios.post('http://localhost:8000/api/v1/match/', {
        query: `query { matches_overview { _id name home_team away_team home_score away_score date } }`,
        variables: {
          id: "65f42e711c248818445678d3"
        }
      })
        .then(response => {
          this.matches = response.data.data.match_details.map(match => {
            // Assuming your backend returns an array of match details
            // You might need to adjust based on the actual structure
            return {
              id: match._id, // Adjust based on your data structure
              title: `${match.home_team} vs ${match.away_team}`,
              date: new Date(parseInt(match.date)).toLocaleString(), // Convert timestamp to readable date
              description: match.description,
              venue: match.venue
            };
          });
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
