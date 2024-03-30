<template>
  <div class="queue">
    <h1 class="text-superblue" v-if="queue_position > 0">Your queue number is : {{ queue_position }}</h1>
    <h1 class="text-superblue" v-else>Please proceed to booking!</h1>
    <p class="lead text-dark"><b>Please do not reload this page.</b><br>You are important to us and your place in the Queue is currently being processed.
      <br>Thank you for your interest for this match and we seek your patience in this process.</p>
    <img src="/src/assets/background1.png" style="width:50%;" alt="Queue Image" class="queue-image">
    <div class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
    <p>User ID: {{this.$auth0.user.value.sub.split('|')[1]}}</p>
    <p>Match ID: {{ matchID }}</p>
    <p v-show="token"><button class="btn btn-primary gradient-button1" @click="chooseSeats">Choose seats</button></p>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';

export default {
  name: 'Queue',
  setup() {
    const initial_position = ref(null);
    const queue_position = ref(null);
    const token = ref(null);
    const progress = ref(0);
    const { user } = useAuth0();
    const user_id = user.value.sub.split('|')[1];

    const socket = new WebSocket('ws://localhost:8000/api/v1/queue')

    socket.onopen = function() {
      console.log('Connected to the WebSocket server');
      var message = {
        action: "connect",
        user_id: user_id,
        demo: true // generated for presentation
      }
      socket.send(JSON.stringify(message));
    };

    socket.onclose = function() {
      console.log('Disconnected from the WebSocket server');
      var message = {
        action: "disconnect",
        user_id: user_id
      }
      socket.send(JSON.stringify(message));
    };

    socket.onmessage = function(event) {
      try {
        var data = JSON.parse(event.data);

        console.log('Received JSON data:', data);

        if ('queue_position' in data) {
          queue_position.value = data.queue_position;
          initial_position.value = data.queue_position;
        }

        if ('num_disconnects' in data) {
          queue_position.value -= data.num_disconnects;
        }

        if ('token' in data) {
          console.log('Token:', data.token);
          progress.value = 100;
          token.value = data.token;
        }

      } catch (e) {
        return;
      }
    };

    watch(queue_position, (newValue, oldValue) => {
      if (initial_position.value != null) {
        let newProgress = (initial_position.value - newValue) / initial_position.value * 100;
        console.log("New progress", newProgress)
        if (newProgress < 100) {
          progress.value = newProgress;
        } else {
          progress.value = 100;
        }
      }
    });

    watch(progress, (newValue, oldValue) => {
      if (newValue == 100) {
        queue_position.value = 0;
      }
    });

    return {
      token,
      queue_position,
      progress
    };
  },
  data() {
    return {
      matchID: null
    };
  },
  methods: {
    chooseSeats() {
      this.$router.push({ name: 'seats', params: { id: this.matchID } });
    }
  },
  mounted() {
    this.matchID = this.$route.params.id;
  },
};
</script>


<style scoped>
.queue {
  text-align: center;
  margin-top: 50px;
}

.text-superblue{
  color: #5356FF;
}

.progress-container {
  width: 50%;
  margin: 20px auto;
  background-color: #f2f2f2;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 20px;
  background-color: #5356FF; /* Adjust color as needed */
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

.gradient-button1 {
    background-image: linear-gradient(to right, #67C6E3, #5356FF); 
}
</style>

  
  
  
  