<template>
  <div class="queue">
    <h1 class="text-superblue">You are now in the queue...</h1>
    <p class="lead text-dark">You are important to us and your place in the Queue is currently being processed. Please do not reload this page.
      <br>Thank you for your interest for this match and we seek your patience in this process.</p>
    <img src="/src/assets/background1.png" style="width:50%;" alt="Queue Image" class="queue-image">
    <div class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>
    <!-- <p>User ID: {{this.$auth0.user.value.sub.split('|')[1]}}</p> -->
    <p>Match ID: {{ matchID }}</p>
  </div>
</template>

<script>
const socket = new WebSocket('ws://localhost:8000/api/v1/queue')

socket.onopen = function() {
  console.log('Connected to the WebSocket server');
  var message = {
    user_id: 3
  }
  socket.send(JSON.stringify(message));
};

socket.onmessage = function(event) {
  console.log('Received message:', event.data);
  this.token = event.data;
};

export default {
  name: 'Queue',
  data() {
    return {
      progress: 20, // Initial progress percentage
      matchID: null,
      token: null
    };
  },
  mounted() {
    this.matchID = this.$route.params.id; 
    // Simulate progress increase over time
    // const interval = setInterval(() => {
    //   if (this.progress < 100) {
    //     this.progress += 10; // Increase progress by 10% (adjust as needed)
    //   } else {
    //     clearInterval(interval); // Stop the interval when progress reaches 100%
    //     // Navigate to the next page when progress reaches 100%
    //     this.$router.push({ name: 'seats', params: { id: this.matchID} });
    //   }
    // }, 1000); // Adjust interval as needed

    // TODO: Verify JWT before routing to checkout page

    this.$router.push({ name: 'Checkout', params: { id: this.matchID } });

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
</style>

  
  
  
  