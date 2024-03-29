<template>
  <div class="admin-page">
    <h1>Admin Dashboard</h1>
    <div class="admin-section">
      <h2>Add Match</h2>
      <form @submit.prevent="addMatch">
        <input type="text" v-model="newMatch.name" placeholder="Match Name" required>
        <input type="datetime-local" v-model="newMatch.date" placeholder="Match Date" required>
        <button type="submit">Add Match</button>
      </form>
    </div>
    <div class="admin-section">
      <h2>Live Stream</h2>
      <form @submit.prevent="addLiveStream">
        <select v-model="selectedMatch">
          <option v-for="match in matches" :value="match.id">{{ match.name }}</option>
        </select>
        <input type="url" v-model="liveStreamUrl" placeholder="Live Stream URL" required>
        <button type="submit">Add Live Stream</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newMatch: {
        name: '',
        date: ''
      },
      matches: [],
      selectedMatch: '',
      liveStreamUrl: ''
    }
  },
  methods: {
    async addMatch() {
      // Placeholder for API call to add a match
      console.log('Adding match:', this.newMatch);
      this.newMatch = { name: '', date: '' }; // Reset form
    },
    async addLiveStream() {
      // Placeholder for API call to add a live stream URL to a match
      console.log('Adding live stream URL:', this.liveStreamUrl, 'to match:', this.selectedMatch);
      this.liveStreamUrl = ''; // Reset form
    }
  },
  mounted() {
    // Placeholder for API call to fetch matches
    this.matches = [
      { id: '1', name: 'Match 1' },
      { id: '2', name: 'Match 2' }
    ]; // Sample data
  }
}
</script>

<style scoped>
.admin-page {
  padding: 20px;
}

.admin-section {
  margin-bottom: 20px;
}

.admin-section h2 {
  margin-bottom: 10px;
}
</style>
