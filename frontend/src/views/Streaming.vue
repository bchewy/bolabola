<template>
  <div>
    <NavBar />
    <div class="streaming-view">
      <!-- <p>{{ matchID }}</p> -->
      <div v-if="streamUrl">
        <p> {{ match.name }} </p>
        <VueBasicPlayer :src="streamUrl" :play="playNow"></VueBasicPlayer>
      <p> {{ match.description }}</p>
      </div>
      <div v-else-if="loading">
        <p>Loading match details...</p>
      </div>
      <div v-else>
        <p>Match not found.</p>
      </div>
    </div>
  </div>
</template>

<script>
  import NavBar from "../components/Navbar.vue";
  import axios from "axios";
  import { defineComponent } from "vue";
  import VueBasicPlayer from "../components/Video.vue";

  const FETCH_MATCHES = `
    query($_id: String!) {
    match_details (_id: $_id) {
        _id,
        name,
        description,
        venue,
        home_team,
        away_team,
        home_score,
        away_score,
        date,
        seats
    }
}
  `;

  export default defineComponent({
    name: "Streaming",
    components: {
      NavBar,
      VueBasicPlayer,
    },
    data() {
      return {
        match: null,
        loading: false,
        matchID: this.$route.params.id,
        streamUrl: "",
        playNow: true,
      };
    },
    mounted() {
      this.fetchMatches(this.matchID);
      // this.getMatchStreamingMatchDetails(matchId);

      axios
        .get("http://localhost:8000/api/v1/videoasset/video?id=1")
        .then((response) => {
          this.streamUrl = response.data;
          // Process the streaming details as needed
          console.log("Streaming details:", streamingDetails);
        })
        .catch((error) => {
          console.error("Error retrieving streaming details:", error);
        });

        axios
          .post("http://localhost:8000/api/v1/match/", {
            query: FETCH_MATCHES,
            variables:{
              _id: this.matchID
            }
          })
          .then((response) => {
           console.log(response.data.data.match_details)
           this.match = response.data.data.match_details
          //   this.matches = response.data.data.matches_overview.map((match) => {
          //     // Assuming your backend returns an array of match details
          //     // You might need to adjust based on the actual structure
          //     console.log(match);
          //     return {
          //       id: match._id, // Adjust based on your data structure
          //       title: `${match.home_team} vs ${match.away_team}`,
          //       home_team: match.home_team,
          //       away_team: match.away_team,
          //       home_score: match.home_score,
          //       away_score: match.away_score,
          //       date: new Date(parseInt(match.date)).toLocaleString(), // Convert timestamp to readable date
          //       description: match.description,
          //       venue: match.venue,
          //       seats: match.seats,
          //     };
          //   });
          })
          .catch((error) => {
            console.error("Error fetching matches:", error);
          });
    },
    methods: {
      // fetchMatchDetails(matchId) {
      //   console.log('Match ID:', matchId);
      //   axios.get(`http://localhost:8000/api/v1/match/${matchId}`)
      //     .then(response => {
      //       const match = response.data;
      //       this.match = {
      //         id: match._id,
      //         title: `${match.home_team} vs ${match.away_team}`,
      //         home_team: match.home_team,
      //         away_team: match.away_team,
      //         date: new Date(parseInt(match.date)).toLocaleString(),
      //         seats: match.seats,
      //       };
      //     })
      //     .catch(error => {
      //       console.error('Error fetching match details:', error);
      //     })
      //     .finally(() => {
      //       this.loading = false;
      //     });
      // },
      fetchMatches() {
      },
      // getMatchStreamingMatchDetails(matchId) {
      //   axios
      //     .get("http://localhost:8000/api/v1/videoasset/video?id=1")
      //     .then((response) => {
      //       const streamingDetails = response.data;
      //       // Process the streaming details as needed
      //       console.log("Streaming details:", streamingDetails);
      //     })
      //     .catch((error) => {
      //       console.error("Error retrieving streaming details:", error);
      //     });
      // },
    },
  });
</script>

<style scoped>
  .streaming-view {
    text-align: center;
    margin-top: 50px;
  }

  .text-superblue {
    color: #5356ff;
  }

  .match-details {
    margin-top: 20px;
  }
</style>
