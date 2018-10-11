"use strict";

import Vuex from 'vuex';
import axios from 'axios';

const store = new Vuex.Store({
  state: {
    items: [],
  },
  modules: {
  },
  getters: {
    getItems(state) {
      return state.items;
    }
  },
  mutations: {
    setItemsList(state, items) {
      state.items = rdfSchemesList;
    }
  },
  actions: {
    loadItems({commit}) {
      axios
        .get("/get_items")
        .then(response => {
          if (response.data.error) {
            commit('error', {
              message: "Ошибка загрузки данных",
              error: response.data.error,
            });
            commit('items', []);
            return;
          }
          commit('items', response.data);
        });
    }
  }
});

module.exports = store;