Vue.component('case-item', {
  props: ['data'],
  template: '\
    <div class="media" v-on:click="getThread">\
      <img class="mr-3" :src="data.sender_profile_picture">\
      <div class="media-body">\
        <span class="author mt-0">{{data.sender_name}}</span>\
        <span role="presentation" aria-hidden="true"> · </span>\
        <span class="time-from-now">{{post_time_moment}}</span>\
        <div>{{data.message}}</div>\
        <div v-if="data.image"><img v-bind:src="data.image"></div>\
        <div>\
          <span class="tag badge badge-dark">{{data.tag}}</span> \
          <span class="tag badge" v-bind:class="data.sentiment">{{data.sentiment}}</span>\
        </div>\
      </div>\
    </div>\
  ',
  methods: {
    getThread: function() {
      this.$emit('get-thread', this.data._id)
    }
  },
  computed: {
    post_time_moment: function () {
      return moment(this.data.created_time, "YYYY-MM-DD hh:ii:ss").fromNow()
    }
  },
})

Vue.component('reply-item', {
  props: ['data'],
  template: '\
    <div class="media">\
      <img class="mr-3" :src="data.picture">\
      <div class="media-body">\
        <textarea class="form-control" rows="2"></textarea>\
        <div class="text-right mt-2">\
          <button class="btn btn-primary btn-sm">Send</button>\
        </div>\
      </div>\
    </div>\
  '
})

var main = new Vue({
  el: '#main',
  data: {
    page: {
      picture: 'https://graph.facebook.com/527202220962403/picture?height=32',
      name: 'TrueMove H',
    },
    cases: null,
    thread: null,
    active_case_id: null,
    main_is_loading: false,
  },
  methods: {
    getThread: function (id) {
      this.active_case_id = id
      this.main_is_loading = true
      this.thread = null
      this.$http.get('http://35.164.146.20:6032/ticket/'+id).then((response) => {
        this.thread = response.body.data
        this.main_is_loading = false
      });
    }
  },
  created: function () {
    this.$http.get('http://35.164.146.20:6032/tickets').then((response) => {
      this.cases = response.body.data
    });
  },
})
