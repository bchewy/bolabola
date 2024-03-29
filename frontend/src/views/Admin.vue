<template>
    <NavBar />
    <div class="admin-page container-fluid">
        <h1>Admin Dashboard</h1>

        <div class="admin-section">

            <h2>Current Matches</h2>
            <table class="table table-striped table-hover">
                <thead class="thead-dark">
                    <tr>
                        <th>Match Name</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="match in matches" :key="match.id">
                        <td>{{ match.name }}</td>
                        <td>{{ match.date }}</td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="editMatch(match.id)">Edit</button>
                            <button class="btn btn-danger btn-sm" @click="deleteMatch(match.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Add Match -->
        <div class="admin-section mt-5">
            <h2 class="text-center mb-4">Add a New Match</h2>
            <form @submit.prevent="addMatch" class="needs-validation" novalidate>
                <div class="form-row">
                    <div class="col-md-6 mb-3">
                        <label for="match-name">Match Name</label>
                        <input id="match-name" type="text" class="form-control" v-model="newMatch.name"
                            placeholder="Enter Match Name" required>
                        <div class="invalid-feedback">
                            Match name is required.
                        </div>
                    </div>

                    <div class="col-md-6 mb-3">
                        <label for="match-date">Match Date</label>
                        <input id="match-date" type="datetime-local" class="form-control" v-model="newMatch.date"
                            placeholder="Select Match Date" required>
                        <div class="invalid-feedback">
                            Please select a match date.
                        </div>
                    </div>
                </div>

                <div class="form-row">
                    <div class="col-md-6 mb-3">
                        <label for="home-team">Home Team</label>
                        <input id="home-team" type="text" class="form-control" v-model="newMatch.home_team"
                            placeholder="Home Team Name" required>
                        <div class="invalid-feedback">
                            Home team is required.
                        </div>
                    </div>

                    <div class="col-md-6 mb-3">
                        <label for="away-team">Away Team</label>
                        <input id="away-team" type="text" class="form-control" v-model="newMatch.away_team"
                            placeholder="Away Team Name" required>
                        <div class="invalid-feedback">
                            Away team is required.
                        </div>
                    </div>
                </div>

                <h4 class="mt-4 mb-3">Ticket Categories</h4>
                <div v-for="(category, index) in newMatch.categories" :key="index" class="form-row align-items-end">
                    <div class="col-md-4 mb-3">
                        <label :for="'category-' + index">Category Name</label>
                        <input :id="'category-' + index" type="text" class="form-control" v-model="category.name"
                            placeholder="Category Name" required>
                        <div class="invalid-feedback">
                            Category name is required.
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <label :for="'quantity-' + index">Seats Quantity</label>
                        <input :id="'quantity-' + index" type="number" class="form-control" v-model="category.quantity"
                            placeholder="Number of Seats" required>
                        <div class="invalid-feedback">
                            Please specify the number of seats.
                        </div>
                    </div>
                </div>
                <button type="submit" class="btn btn-success btn-lg btn-block">Add Match</button>
            </form>
        </div>

        <!-- Livestreams -->
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

import NavBar from "../components/Navbar.vue";
import axios from "axios";
const FETCH_MATCHES = `
  query {
    matches_overview {
      _id,
      name,
      home_team,
      away_team,
      home_score,
      away_score,
      date,
      seats
    }
  }
`;


export default {
    components: {
        NavBar
    },
    data() {
        return {
            newMatch: {
                name: '',
                date: '',
                categories: [
                    { name: 'A', quantity: 0 },
                    { name: 'B', quantity: 0 },
                    { name: 'C', quantity: 0 }
                ] // Add this line

            },
            matches: [],
            selectedMatch: '',
            liveStreamUrl: ''
        }
    },
    methods: {
        async addMatch() {
            const mutation = `
            mutation CreateMatch($name: String!, $home_team: String!, $away_team: String!, $date: String!, $seats: Int!, $categories: [CategoryInput!]!) {
                createMatch(
                    name: $name,
                    home_team: $home_team,
                    away_team: $away_team,
                    date: $date,
                    seats: $seats,
                    categories: $categories
                ) {
                    _id
                    name
                    home_team
                    away_team
                    date
                    seats
                }
            }
        `;

            const variables = {
                name: this.newMatch.name,
                home_team: this.newMatch.home_team,
                away_team: this.newMatch.away_team,
                date: this.newMatch.date,
                seats: this.newMatch.categories.reduce((acc, category) => acc + category.quantity, 0),
                categories: this.newMatch.categories.map(category => ({
                    name: category.name,
                    quantity: category.quantity
                }))
            };

            try {
                const response = await fetch('http://localhost:8000/api/v1/match', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({
                        query: mutation,
                        variables: variables
                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const responseData = await response.json();
                console.log('Match added:', responseData);

                // Reset form
                this.newMatch = {
                    name: '',
                    date: '',
                    categories: [
                        { name: 'A', quantity: 0 },
                        { name: 'B', quantity: 0 },
                        { name: 'C', quantity: 0 }
                    ]
                };
            } catch (error) {
                console.error('Error adding match:', error);
            }
        },
        async addLiveStream() {
            // Placeholder for API call to add a live stream URL to a match
            console.log('Adding live stream URL:', this.liveStreamUrl, 'to match:', this.selectedMatch);
            this.liveStreamUrl = ''; // Reset form
        },
        fetchMatches() {
            axios.post('http://localhost:8000/api/v1/match/', {
                query: FETCH_MATCHES,
            })
                .then(response => {
                    this.matches = response.data.data.matches_overview.map(match => {
                        console.log(match);
                        return {
                            id: match._id,
                            name: match.name,
                            title: `${match.home_team} vs ${match.away_team}`,
                            home_team: match.home_team,
                            away_team: match.away_team,
                            home_score: match.home_score,
                            away_score: match.away_score,
                            date: new Date(parseInt(match.date)).toLocaleString(),
                            description: match.description,
                            venue: match.venue,
                            seats: match.seats
                        };
                    });
                })
                .catch(error => {
                    console.error('Error fetching matches:', error);
                });
        },
        
    },
    mounted() {
        // Placeholder for API call to fetch matches
        this.fetchMatches();

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
