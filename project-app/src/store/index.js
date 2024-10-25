import { createStore } from 'vuex';
import createPersistedState from "vuex-persistedstate";
export default createStore({
    state: {
      refresh: null,
      access: null,
      currentPage:'dashboard',
      isDark: false,
      usercat:null,
    },
    getters: {
        refresh: state => state.refresh,
        access: state => state.access,
        usercat: state => state.usercat,
        currentPage: state => state.currentPage,
        isDark: state => state.isDark,
    },
    mutations: {
      setRefresh(state, refresh) {
        state.refresh = refresh;
      },
      setAccess(state, access) {
        state.access = access;
      },
      setUsercat(state, usercat) {
        state.usercat = usercat;
      },
      setCurrentPage(state, currentPage) {  // Renamed from currentPage to setCurrentPage
        state.currentPage = currentPage;
      },
      setIsDark(state, isDark) {  // Renamed from isDark to setIsDark
        state.isDark = isDark;
      },
      resetStore(state) {
        state.refresh = null;
        state.access = null;
        state.isDark = false;
        state.currentPage = 'dashboard';
        state.usercat = null;
      },
    },
    actions: {
    },
    modules: {
    },
    plugins: [
      createPersistedState({
        // Options to configure persistence
        storage: window.sessionStorage, //window.localStorage,
      })
    ]
  })
  