import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'

require('./bootstrap');

const mainWindow = require("./mainWindow/mainWindow.vue");

const workersWindow = require("./workersWindow/workersWindow.vue");

const runTask = require("./runTask/runTask.vue");

const routes = [
  {
    path: '/',
    name: 'root',
    component: mainWindow
  },
  {
    path: '/workers',
    name: 'workersWindow',
    component: workersWindow
  },
  {
    path: '/run_task',
    name: 'runTask',
    component: runTask
  },
];

Vue.use(Vuex);

const store = require('./store.js');

const router = new VueRouter({
  routes
});

Vue.use(VueRouter);

import vSelect from 'vue-select';
Vue.component('v-select', vSelect);


import VueDialog from 'vuedialog';

import  {default as plugin, Component as Vuedals, Bus} from 'vuedals';
Vue.use(plugin);

VueDialog.setBus(Bus);

const app = new Vue({
  el: '#app',
  router,
  store,
  methods: {
  },
  components: {
    'vuedals': Vuedals,
    'vuedialog': VueDialog
  }
});
