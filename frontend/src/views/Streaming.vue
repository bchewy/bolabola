<template>
  <div>
    <NavBar />
    <div class="streaming-view">
      <div v-if="match">
        <h1 class="text-center text-superblue">{{ match.title }}</h1>
        <p class="lead text-dark text-center">Tune in and experience the thrill of live football!</p>
        <div class="match-details">
          <p>Home Team: {{ match.home_team }}</p>
          <p>Away Team: {{ match.away_team }}</p>
          <p>Date: {{ match.date }}</p>
          <p>Seats Left: {{ match.seats }}</p>
        </div>
      </div>
      <div v-else>
        <p>Loading match details...</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/Navbar.vue';
import axios from 'axios';

export default {
  name: 'Streaming',
  components: {
    NavBar,
  },
  data() {
    return {
      match: null,
    };
  },
  created() {
    const matchId = this.$route.params.id;
    this.fetchMatchDetails(matchId);
  },
  methods: {
    fetchMatchDetails(matchId) {
      axios.get(`http://localhost:8000/api/v1/match/${matchId}`)
        .then(response => {
          const match = response.data;
          this.match = {
            id: match._id,
            title: `${match.home_team} vs ${match.away_team}`,
            home_team: match.home_team,
            away_team: match.away_team,
            date: new Date(parseInt(match.date)).toLocaleString(),
            seats: match.seats,
          };
        })
        .catch(error => {
          console.error('Error fetching match details:', error);
        });
    },
  },
};
</script>

<style scoped>
.streaming-view {
  text-align: center;
  margin-top: 50px;
}

.text-superblue {
  color: #5356FF;
}

.match-details {
  margin-top: 20px;
}
</style>