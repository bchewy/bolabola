import { createStore } from 'vuex';

export default createStore({
    state: {
        selectedTickets: [],
        
    },
    mutations: {
        setSelectedTickets(state, tickets) {
            state.selectedTickets = tickets;
        }
    },
    actions: {
        updateSelectedTickets({ commit }, tickets) {
            commit('setSelectedTickets', tickets);
        }
    },
    getters: {
        getSelectedTickets(state) {
            return state.selectedTickets;
        }
    }
});
