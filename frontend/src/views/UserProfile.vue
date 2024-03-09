<template>
  <div>
    <NavBar />
    <div class="about-view d-flex flex-column justify-content-center align-items-center">
      <h1 class="text-center">Profile page</h1>
      <p class="lead text-dark text-center">Confirmed Bookings</p>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Match Name</th>
            <th scope="col">Match Time</th>
            <th scope="col">Match Location</th>
            <th scope="col">Match Price</th>
            <th scope="col">Refund</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ticket, index) in tickets" :key="index">
            <td>{{ ticket.matchName }}</td>
            <td>{{ ticket.matchTime }}</td>
            <td>{{ ticket.matchLocation }}</td>
            <td>{{ ticket.matchPrice }}</td>
            <td>
              <button v-if="isRefundable(ticket)" class="btn btn-primary" @click="refundTicket(index)">Refund</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/Navbar.vue';

export default {
  name: "StreamingView",
  components: {
    NavBar,
  },
  data() {
    return {
      tickets: [
        { matchName: 'Match A', matchTime: '2024-03-10T14:00:00', matchLocation: 'Location A', matchPrice: 10 },
        { matchName: 'Match B', matchTime: '2024-03-11T15:00:00', matchLocation: 'Location B', matchPrice: 15 },
        { matchName: 'Match C', matchTime: '2025-01-13T10:00:00', matchLocation: 'Location C', matchPrice: 20 },
      ],
      refundedTickets: []
    };
  },
  methods: {
    isRefundable(ticket) {
      // Calculate if the ticket is more than 24 hours away from the current time
      const matchTime = new Date(ticket.matchTime);
      const currentTime = new Date();
      const timeDifference = matchTime.getTime() - currentTime.getTime();
      const hoursDifference = timeDifference / (1000 * 3600);
      return hoursDifference > 24;
    },
    refundTicket(index) {
      const refundedTicket = this.tickets.splice(index, 1)[0]; // Remove the ticket from the tickets array
      this.refundedTickets.push(refundedTicket); // Add the refunded ticket to the refundedTickets array
      this.$router.push('/views/refund');
    }
  }
};
</script>

<style scoped>
.about-view {
  text-align: center;
  margin-top: 50px;
}
</style>

  

<!-- should have some way of showing the ticket bought, and a refund button right next to it only if the match is less than 24hours away. THANKS -->