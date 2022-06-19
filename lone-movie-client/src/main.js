import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
import VueVideoPlayer from "vue-video-player";

import "video.js/dist/video-js.css";

Vue.config.productionTip = false;
Vue.use(Buefy);
Vue.use(VueVideoPlayer);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
