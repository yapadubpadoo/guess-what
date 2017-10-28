store = new Vuex.Store({
  state: {
    cases: ''
  },
  mutations: {
    updateCases(state, payload) {
      state.cases = payload
    }
  },
  actions: {
    refreshCases(context) {
      return new Promise((resolve) => {
        this.$http.get('js/cases.js').then((response) => {
          context.commit('updateCases', response.data);
          resolve();
        });
      });
    }
  }
});

Vue.component('case-item', {
  props: ['data'],
  template: '\
    <div class="media" v-on:click="getThread">\
      <img class="mr-3" :src="data.author.picture">\
      <div class="media-body">\
        <span class="author mt-0">{{data.author.name}}</span>\
        <span role="presentation" aria-hidden="true"> · </span>\
        <span class="time-from-now">{{post_time_moment}}</span>\
        <div>{{data.text}}</div>\
        <div v-if="data.image"><img v-bind:src="data.image"></div>\
        <div><span class="tag badge badge-dark" v-for="tag in data.tags">{{tag}}</span></div>\
      </div>\
    </div>\
  ',
  methods: {
    getThread: function() {
      this.$emit('get-thread', this.data.id)
    }
  },
  computed: {
    post_time_moment: function () {
      return moment(this.data.post_time, "YYYY-MM-DD hh:ii:ss").fromNow()
    }
  },
})

Vue.component('reply-item', {
  props: ['data'],
  template: '\
    <div class="media">\
      <img class="mr-3" :src="data.picture">\
      <div class="media-body">\
        <input class="form-control" type="text">\
      </div>\
    </div>\
  ',
})

var main = new Vue({
  el: '#main',
  data: {
    page: {
      picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p200x200/14716270_1430563570305350_8075231906765003576_n.jpg?oh=c17e80ed0e6181b25d4cfe2e219316f9&oe=5A6C6529',
      name: 'TrueMove H',
    },
    cases: [],
    thread: []
  },
  methods: {
    getThread: function (id) {
      console.log(id)
      this.$http.get('js/thread'+id+'.json').then((response) => {
        this.thread = response.body
      });
    }
  },
  mounted: function () {
    this.$http.get('js/cases.json').then((response) => {
      this.cases = response.body
    });
  },
})