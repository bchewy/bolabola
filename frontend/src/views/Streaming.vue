<template>
  <div>
    <NavBar />
    <div class="streaming-view">
      <div v-if="streamUrl">
        <p> {{ match.name }} </p>
        <VueBasicPlayer :src="streamUrl" :play="playNow" @video-timestamp="handleTimeUpdate" />
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
  import { io } from 'socket.io-client';

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
        socket: null,
      };
    },
    mounted() {

      this.socket = io('http://localhost:8000', {
        transports: ['websocket'],
        path: '/api/v1/streaming/socket.io',
      });

  
      // this.socket.on('connect_error', (error) => {
      //   console.error('Connection error:', error);
      // });

      this.socket.on('disconnect', () => {
        console.log('Disconnected from streaming server');
      })

      this.socket.on('connect', () => {
        console.log('Connected to streaming server');
      });

      this.socket.on('stream', (data) => {
        console.log('Stream data:', data.data);
      });

      axios
        .get("http://localhost:8000/api/v1/videoasset/video?id=1")
        .then((response) => {
          this.streamUrl = response.data;
          // Process the streaming details as needed
          // console.log("Streaming details:", streamingDetails);
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
            this.match = response.data.data.match_details;
          })
          .catch((error) => {
            console.error("Error fetching matches:", error);
          });
    },
    methods: {
      handleTimeUpdate(timestamp) {
        console.log("Timestamp:", timestamp);
        this.socket.emit('stream', timestamp);
      }
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
