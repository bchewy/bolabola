<template>
  <div>
    <NavBar />
    <div class="about-view d-flex flex-column justify-content-center align-items-center">
      <h1 class="text-center text-superblue">{{ userName }}'s Profile page</h1>
      <p class="lead text-dark text-center">Confirmed Bookings</p>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Match Name</th>
            <th scope="col">Match Time</th>
            <!-- <th scope="col">Match Location</th> -->
            <th scope="col">Quantity</th>
            <th scope="col">Category</th>
            <th scope="col">Refund</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ticket, index) in tickets" :key="index">
            <td>{{ ticket.matchName }}</td> 
            <td>{{ ticket.matchTime }}</td>
            <!-- <td>{{ ticket.matchLocation }}</td> -->
            <td>{{ ticket.quantity }}</td>
            <td>{{ ticket.ticket_category }}</td>
            <td>
              <button v-if="isRefundable(ticket)" class="btn btn-primary gradient-button1"
                @click="refundTicket(index)">Refund</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/Navbar.vue';
import axios from 'axios';

const FETCH_MATCH_DETAILS = `
  query FetchMatchDetails($_id: String!) {
    match_details(_id: $_id) {
      _id
      name
      home_team
      away_team
      home_score
      away_score
      date
      seats
      venue
    }
  }
`;

export default {
  name: "StreamingView",
  components: {
    NavBar,
  },
  computed: {
    userName() { // for displaying
      name = this.$auth0.user.value.name;
      // capitalize the first letter of the name
      return name.charAt(0).toUpperCase() + name.slice(1);
    },
    userId() { // for sending to the backend
      return this.$auth0.user.value.sub.split('|')[1];
    },
  },
  data() {
    return {
      tickets: [],
      refundedTickets: [],
      refund_success: true,
      tickets_with_match_info: [],
    };
  },
  methods: {
    // Function to get the user's information
    getUserInfo(userId) {
      // Send a request to the backend to get the user's information using their userId using get request
      fetch(`http://localhost:8000/api/v1/user/${userId}`)
        .then((response) => response.json())
        .then((data) => {
          this.tickets = data["data"].tickets;

          // Get the match information for each ticket
          this.tickets.forEach((ticket) => {
            // Send a request to the backend to get the match information using the matchId
            axios.post('http://localhost:8000/api/v1/match/', {
              query: FETCH_MATCH_DETAILS,
              variables: {
                _id: ticket.match_id,
              },
            })
              .then(response => {
                ticket.matchName = response.data.data.match_details.name;
                ticket.matchLocation = response.data.data.match_details.venue;
                ticket.matchTime = new Date(Number(response.data.data.match_details.date));
                this.tickets_with_match_info.push(ticket);
              })
              .catch(error => {
                console.error('Error fetching matches:', error);
              });
          });
        });
    },

    // Function to fetch the user's information
    async fetchUserInfo() {
      await this.getUserInfo(this.userId);
    },

    // Function to refund check if a ticket is refundable
    isRefundable(ticket) {
      // Calculate if the ticket is more than 24 hours away from the current time
      const matchTime = new Date(ticket.matchTime);
      const currentTime = new Date();
      const timeDifference = Math.abs(matchTime.getTime() - currentTime.getTime());
      const hoursDifference = timeDifference / (1000 * 3600);
      console.log(hoursDifference)
      return hoursDifference > 24;
    },

    // Function to refund tickets
    refundTicket(index) {
      // Send a request to the backend to refund the ticket
      fetch('http://localhost:8000/api/v1/refund/initiate-refund', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(
          {
            ticket_info: this.tickets[index],
            user_id: this.userId,
            email: this.$auth0.user.value.email
          }
        ),
      })
        .then((response) => response.json())
        .then((data) => {
          this.refund_success = data.success; // not tested yet
        });

      const refundedTicket = this.tickets.splice(index, 1)[0]; // Remove the ticket from the tickets array
      this.refundedTickets.push(refundedTicket); // Add the refunded ticket to the refundedTickets array
      if (this.refund_success) {
        this.$router.push('/views/refund');
      } else {
        alert('Unsuccessful Refund. Please try again.');
      }
    },
    
  },
  mounted() {
    this.fetchUserInfo();
  },
};
</script>


<style scoped>
.about-view {
  text-align: center;
  margin-top: 50px;
}

.text-superblue {
  color: #5356FF;
}

.gradient-button1 {
    background-image: linear-gradient(to right, #67C6E3, #5356FF); 
}
</style>
