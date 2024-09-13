<template>
  <div>
    <NavBar />
    <div class="events-view container-fluid">
      <h1 class="text-superblue">Matches</h1>
      <p class="lead text-dark">Find the latest games here!</p>
      <div class="input-group mb-3">
        <input type="text" v-model="searchTerm" class="form-control" placeholder="Search by name..."
          aria-label="Search by name">
      </div>
      <div class="container-fluid mt-3">
        <div class="row gx-3 gy-3">
          <div v-for="match in filteredMatches" :key="match._id" class="col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <div class="card" @click="displayMatchDetails(match)">
              <div class="card-body">
                <h5 class="card-title">{{ match.name }}</h5>
                <p class="card-text">Home Team: {{ match.home_team }}</p>
                <p class="card-text">Away Team: {{ match.away_team }}</p>
                <!-- <p class="card-text">Home Score: {{ match.home_score }}</p>
                <p class="card-text">Away Score: {{ match.away_score }}</p> -->
                <p class="card-text">Date: {{ match.date }}</p>
                <p class="card-text">Total Seats: {{ match.seats }}</p>
              </div>
              <div class="card-footer">
                <!-- Match ID: {{ match.id }} -->
                <button class="btn btn-primary gradient-button1" @click="bookMatch(match)">Book Now</button>
                <!-- <button v-else class="btn btn-primary gradient-button1" disabled>Book Now</button> -->
                <button class="btn btn-primary gradient-button2" @click="watchMatch(match)">Watch Live</button>


                
                <!-- <button v-else class="btn btn-primary gradient-button2" @click="watchMatch(match)">Watch Live</button> -->
                <!-- <button v-if="isWithinBookingWindow(match.date)" class="btn btn-primary gradient-button1"
                  @click="bookMatch(match)" disabled>Book Now</button>
                <button v-else class="btn btn-primary gradient-button1">Book Now</button>
                <button v-if="!isDuringLiveWindow(match.date)" class="btn btn-primary gradient-button2"
                  @click="watchMatch(match)" disabled>Watch Live</button>
                <button v-else class="btn btn-primary gradient-button2" @click="watchMatch(match)">Watch Live</button> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import gql from 'graphql-tag';
import NavBar from '../components/Navbar.vue';
import axios from 'axios';

const FETCH_MATCHES = `
  query {
    matches_overview {
      _id,
      name,
      home_team,
      away_team,
      home_score,
      away_score,
      date,
      seats
    }
  }
`;

export default {
  components: {
    NavBar
  },
  data() {
    return {
      matches: [],
      selectedMatch: null,
      searchTerm: ''
    };
  },
  computed: {
    filteredMatches() {
      return this.matches.filter(match =>
        match.name.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
  },
  created() {
    this.fetchMatches();
  },
  methods: {
    // Watch match Handling: Scenario 3
    watchMatch(match) {
      this.$router.push({ name: 'Streaming', params: { id: match.id } });
    },
    bookMatch(match) {
      this.$router.push({ name: 'Queue', params: { id: match.id } });
      // this.$router.push({ name: 'Queue', params: { id: match.id } });
      // this.$router.push('/views/queue');
    },
    fetchMatches() {
      axios.post('http://localhost:8000/api/v1/match/', {
        query: FETCH_MATCHES,
      })
        .then(response => {
          this.matches = response.data.data.matches_overview.map(match => {
            // Assuming your backend returns an array of match details
            // You might need to adjust based on the actual structure
            console.log(match);
            return {
              id: match._id, // Adjust based on your data structure
              name: match.name,
              title: `${match.home_team} vs ${match.away_team}`,
              home_team: match.home_team,
              away_team: match.away_team,
              home_score: match.home_score,
              away_score: match.away_score,
              date: new Date(parseInt(match.date)).toLocaleString(), // Convert timestamp to readable date
              description: match.description,
              venue: match.venue,
              seats: match.seats
            };
          });
        })
        .catch(error => {
          console.error('Error fetching matches:', error);
        });
    },
    displayMatchDetails(match) {
      this.selectedMatch = match;
    },
    isWithinBookingWindow(matchDate) {
      // can book up to 90 minutes before match starts
      // Convert the matchDate string to a Date object
      // Assuming matchDate is in the format "DD/MM/YYYY, HH:MM:SS"
      const [datePart, timePart] = matchDate.split(', ');
      const [day, month, year] = datePart.split('/');
      const [hours, minutes, seconds] = timePart.split(':');
      const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      const matchDateTime = new Date(formattedDate);

      // Calculate the booking window
      const now = new Date();
      const ninetyMinutesBefore = new Date(matchDateTime.getTime() - 90 * 60000);

      // Check if the current time is within the booking window
      console.log('Now:', now, '90 minutes before:', ninetyMinutesBefore, "bool:", now <= ninetyMinutesBefore);
      return now <= ninetyMinutesBefore;
    },
    isDuringLiveWindow(matchDate) {
      // Convert the matchDate string to a Date object
      // Assuming matchDate is in the format "DD/MM/YYYY, HH:MM:SS"
      const [datePart, timePart] = matchDate.split(', ');
      const [day, month, year] = datePart.split('/');
      const [hours, minutes, seconds] = timePart.split(':');
      const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
      const matchDateTime = new Date(formattedDate);

      // Calculate the booking window
      const now = new Date();
      const ninetyMinutesBefore = new Date(matchDateTime.getTime() - 90 * 60000);
      const twoHundredMinutesAfter = new Date(matchDateTime.getTime() + 200 * 60000);

      // Check if the current time is within the live window
      console.log('Now:', now, '90 minutes before:', ninetyMinutesBefore, '200 minutes after:', twoHundredMinutesAfter, "bool:", now >= ninetyMinutesBefore && now <= twoHundredMinutesAfter);
      return now >= ninetyMinutesBefore && now <= twoHundredMinutesAfter;
    },
  }

};
</script>


<style scoped>
.events-view {
  text-align: center;
  margin-top: 50px;
}

.text-superblue {
  color: #5356FF;
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

.gradient-button1 {
  background-image: linear-gradient(to right, #67C6E3, #5356FF);
}

.gradient-button2 {
  background-image: linear-gradient(to right, #DFF5FF, #67C6E3);
  color: black
}
</style>
