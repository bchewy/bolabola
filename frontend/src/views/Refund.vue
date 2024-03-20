<template>
    <div class="refund">
      <h1 class="text-superblue">Refunded Tickets</h1>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Match Name</th>
            <th scope="col">Match Time</th>
            <th scope="col">Match Location</th>
            <th scope="col">Match Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ticket, index) in refundedTickets" :key="index">
            <td>{{ ticket.matchName }}</td>
            <td>{{ ticket.matchTime }}</td>
            <td>{{ ticket.matchLocation }}</td>
            <td>{{ ticket.matchPrice }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  

<!-- <script>
export default {
  computed: {
    refundedTickets() {
      return this.$store.state.refundedTickets;
    }
  }
};
</script> -->
  
<style scoped>
.text-superblue{
  color: #5356FF;
}

.refund {
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