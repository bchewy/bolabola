<template>
  <div>
    <NavBar />
    <div class="streaming-view">
      <!-- {{ streamUrl }} -->
      <div v-if="streamUrl" class="flex-container">
        <h3> {{ match.name }} </h3>
        <p class><span class="teamName">{{ match.home_team }}</span> {{ score[match.home_team] }}:{{
        score[match.away_team] }} <span>{{ match.away_team }}</span></p>
        <div class="container">
          <!-- <transition-group name="list"> -->
          <div class="videoPlayer">
            <VueBasicPlayer :match="match" :src="streamUrl" :play="playNow" @video-timestamp="handleTimeUpdate" />
          </div>
          <div class="ticker">
            <p v-for="(highlight, key) in matchInfo" :key="key">
            <div :style="{ float: match.home_team == highlight.team ? 'left' : 'right', clear: 'both', width: '50%' }">
              <div class="event"
                :class="{ 'home-team': highlight.team === match.home_team, 'away-team': highlight.team === match.away_team }">
                <div class="eventDetails">
                  <h6 class="eventTeam">{{ highlight.team }}</h6>
                  <h6 class="eventPlayer">{{ highlight.player }}</h6>
                  <p class="eventInfo">{{ highlight.description }}</p>
                </div>
              </div>
            </div>
            </p>
          </div>
        </div>
        <p> {{ match.description }}</p>
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
      matchInfo: [],
      score: {}
    };
  },
  mounted() {

      this.socket = io('http://localhost:8000', {
        transports: ['websocket'],
        path: '/api/v1/livestats/socket.io',
      });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from streaming server');
    })

    this.socket.on('connect', () => {
      console.log('Connected to streaming server');
    });

    this.socket.on('stream', (data) => {
      this.matchInfo.unshift(data.data);
      console.log('Stream data:', data.data);
      console.log(data.data.event)
      if (data.data.event == 'GOAL') {
        console.log(this.score[data.data.team.toUpperCase()])
        this.score[data.data.team.toUpperCase()] += 1;
      }

      this.$nextTick(() => {
        const newEvent = this.$el.querySelector('.event');
        newEvent.classList.add('animate');
        const existingEvents = this.$el.querySelectorAll('.event:not(.animate)');
        existingEvents.forEach((event) => {
          event.classList.add('slide-down');
          setTimeout(() => {
            event.classList.remove('slide-down');
          }, 1000); // The duration of your animation
        });
        setTimeout(() => {
          newEvent.classList.remove('animate');
        }, 1000); // The duration of your animation
      });

    });

    axios
      .get("http://localhost:8000/api/v1/videoasset/video?id=1")
      .then((response) => {
        console.log("response",response.data)
        this.streamUrl = response.data;
      })
      .catch((error) => {
        console.error("Error retrieving streaming details:", error);
      });

    axios
      .post("http://localhost:8000/api/v1/match/", {
        query: FETCH_MATCHES,
        variables: {
          _id: this.matchID
        }
      })
      .then((response) => {
        console.log(response.data.data.match_details)
        this.match = response.data.data.match_details;
        this.score = {
          [this.match.home_team]: 0,
          [this.match.away_team]: 0,
        }
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
.container {
  display: flex;
  align-items: flex-start;
}

.streaming-view {
  text-align: center;
  align-items: center;
  margin-top: 50px;
}

.text-superblue {
  color: #5356ff;
}

.match-details {
  margin-top: 20px;
}

.eventPlayer{
  font-weight: 300;
}

.videoplayer {
  align-items: center;
  /* width: fit-content; */
  width: 50%;
  margin: auto;
  margin-right: 5%;
}

.ticker {
  margin-left: auto;
  /* background-color: grey; */
  overflow-y: scroll;
  height: 400px;
  width: 50%;
}

.eventDetails {
  width: inherit;
  margin-left: 3%;
  margin-right: 3%;
}

.list-move {
  transition: transform 1s;
}

.event {
  margin-top: 3%;
  margin-bottom: 3%;
  padding: 5% 5% 0% 5%;
  border-radius: 15px;
  background-color: #5356FF;
  /* background-color: inherit; */
  color: white;
  /* display: flex; */
  /* justify-content: space-between; */
  transition: transform 1s ease-out;
}

.home-team {
  background-color: #67C6E3;
}

.away-team {
  background-color: #5356ff;
}

.event.animate {
  animation: slideIn 1s ease-out;
}

.event.slide-down {
  animation: slideDown 1s ease-out;
}

@keyframes slideIn {
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }

  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideDown {
  0% {
    transform: translateY(0);
  }

  100% {
    transform: translateY(0%);
  }
}
</style>
