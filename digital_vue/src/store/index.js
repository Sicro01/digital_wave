import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state: {
    isAuthenticated: false,
    token: '',
    isLoading: false,
    snackbar: {
      show: false,
      text: '',
      alerttype: '',
      contentclass: '',
    },
    show: {
      planCalendar: false,
      phaseTabs: true,
    },
    selectedPlan: '',
    selectedPhaseData: {
      phase: null,
      index: null,
    },
    selectedStrategyData: {
      strategy: null,
      index: null,
    },
    storedCountries: [],
    storedChannels: [],
    axiosState: false,
  },
  getters: {

  },
  mutations: {
    PLAN_SELECTED(state, plan) {
      state.selectedPlan = plan
    },
    PHASE_DATA_SELECTED(state, payload) {
      state.selectedPhaseData.phase = payload.phase
      if (payload.index !== null) {
        state.selectedPhaseData.index = payload.index
      }
    },
    STRATEGY_DATA_SELECTED(state, payload) {
      state.selectedStrategyData.strategy = payload.strategy
      if (payload.index !== null) {
        state.selectedStrategyData.index = payload.index
      }
    },
    COUNTRIES_STORED(state, countries) {
      state.storedCountries = countries
    },
    CHANNELS_STORED(state, channels) {
      state.storedChannels = channels
    },
    PLAN_CALENDAR_TOGGLED(state) {
      state.show.planCalendar = !state.show.planCalendar
    },
    PHASE_TABS_TOGGLED(state) {
      state.show.phaseTabs = !state.show.phaseTabs
    },
    STRATEGY_TABS_TOGGLED(state) {
      state.show.strategyTabs = !state.show.strategyTabs
      console.log('state.show.strategyTabs: ', state.show.strategyTabs)
    },
    SNACKBAR_SHOW(state, payload) {
      let timeout = 300
      setTimeout(() => {
        state.snackbar.show = true
        state.snackbar.text = payload.text
        state.snackbar.alerttype = payload.alerttype
        state.snackbar.contentclass = payload.contentclass
      }, timeout)
      state.snackbar.show = false
    },
    SNACKBAR_HIDE(state) {
      state.snackbar.show = false
    },
  },
  actions: {
    selectPlan({ commit }, plan) {
      commit('PLAN_SELECTED', plan)
    },
    selectPhaseData({ commit }, payload) {
      commit('PHASE_DATA_SELECTED', payload)
    },
    selectStrategyData({ commit }, payload) {
      commit('STRATEGY_DATA_SELECTED', payload)
    },
    storeCountries({ commit }, payload) {
      commit('COUNTRIES_STORED', payload)
    },
    storeChannels({ commit }, payload) {
      commit('CHANNELS_STORED', payload)
    },
    togglePlanCalendar({ commit }) {
      commit('PLAN_CALENDAR_TOGGLED')
    },
    togglePhaseTabs({ commit }) {
      commit('PHASE_TABS_TOGGLED')
    },
    toggleStrategyTabs({ commit }) {
      commit('STRATEGY_TABS_TOGGLED')
    },
    showSnackBar({ commit }, payload) {
      commit('SNACKBAR_SHOW', payload)
    },
    hideSnackBar({ commit }) {
      commit('SNACKBAR_HIDE')
    },
  },
  modules: {
  }
})
