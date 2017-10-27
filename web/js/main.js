
Vue.component('case-item', {
  props: ['data'],
  template: '\
    <div class="media">\
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
  computed: {
    post_time_moment: function () {
      return moment(this.data.post_time, "YYYY-MM-DD hh:ii:ss").fromNow();
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
    cases: [
      {
        id: 1,
        author: {
          picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p160x160/22049823_904876223022108_248343297152554844_n.jpg?oh=9e86d7bd7be295dda204aabe0d2426dd&oe=5AAE8E54',
          name: 'ญิ๋ง\' ป้อ',
        },
        text: 'มียี่ห้อไหน และรุ่นอะไรบ้างคะ ขอข้อมูลแบบละเอียดของแต่ละรุ่นที่ร่วมรายการด้วยค่ะ',
        post_time: '2017-10-27 17:00:00',
        tags: ['ร้องเรียน', 'negative']
      },
      {
        id: 2,
        author: {
          picture: 'https://www.facebook.com/profile.php?id=100004992157674&fref=ufi&rc=p',
          name: 'ญิ๋ง\' ป้อ',
        },
        text: 'เขาประกาศอำนวยความสะดวก เกี่ยวอะไรกับเครื่องฟรี',
        post_time: '2017-10-27 18:00:00',
        tags: ['สอบถาม', 'neutral']
      },
    ],
    thread: [
      {
        id: 0,
        author: {
          picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p200x200/14716270_1430563570305350_8075231906765003576_n.jpg?oh=c17e80ed0e6181b25d4cfe2e219316f9&oe=5A6C6529',
          name: 'TrueMove H',
        },
        text: `พิเศษ สำหรับลูกค้าแบบเติมเงิน ทั้งลูกค้าใหม่ ลูกค้าปัจจุบัน และ ย้ายค่ายเบอร์เดิม รับส่วนลดสมาร์ทโฟนสูงสุด 7,000 บาท
                เมื่อซื้อเครื่องพร้อมสมัครแพ็กเกจ Buffet Net Plus ให้โทรและเล่นเน็ต ไม่อั้น ไม่ลดสปีด
                เพิ่มเติม: http://truemoveh.truecorp.co.th/news/detail/630`,
        image: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-9/22788703_1887005421327827_2355845310634910527_n.jpg?oh=cf73fe68638809894aa7a148126333eb&oe=5A769A19',
        post_time: '2017-10-27 16:00:00',
        type: 'post',
      },
      {
        id: 1,
        author: {
          picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p160x160/22049823_904876223022108_248343297152554844_n.jpg?oh=9e86d7bd7be295dda204aabe0d2426dd&oe=5AAE8E54',
          name: 'ญิ๋ง\' ป้อ',
        },
        text: 'มียี่ห้อไหน และรุ่นอะไรบ้างคะ ขอข้อมูลแบบละเอียดของแต่ละรุ่นที่ร่วมรายการด้วยค่ะ',
        post_time: '2017-10-27 17:00:00',
        type: 'comment',
        tags: ['ร้องเรียน', 'negative'],
      },
      {
        id: 0,
        author: {
          picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p200x200/14716270_1430563570305350_8075231906765003576_n.jpg?oh=c17e80ed0e6181b25d4cfe2e219316f9&oe=5A6C6529',
          name: 'TrueMove H',
        },
        text: `สวัสดีค่ะ จะเป็นแคมเปญ pre pay smart value นะคะ เครื่องที่ร่วมรายการมีค่อนข้างหลายรุ่น สามารถตรวจสอบรุ่นที่ร่วมรายการได้ที่ http://truemoveh.truecorp.co.th/news/detail/630 ค่ะ 
หากต้องการสอบถามข้อมูลเกี่ยวเครื่องรุ่นใดเพิ่มสามารถแจ้งชื่อรุ่นที่สนใจเข้ามาได้ตลอด 24 ชม.นะคะ แอดมินยินดีตรวจสอบรายละเอียดแคมเปญให้ค่ะ`,
        image: 'https://www.facebook.com/TrueMoveH/photos/a.288679857827066.83862.204234332938286/1887005421327827/?type=3',
        post_time: '2017-10-27 16:00:00',
        type: 'reply-comment',
      },
      {
        id: 1,
        author: {
          picture: 'https://scontent.fbkk13-1.fna.fbcdn.net/v/t1.0-1/p160x160/22049823_904876223022108_248343297152554844_n.jpg?oh=9e86d7bd7be295dda204aabe0d2426dd&oe=5AAE8E54',
          name: 'ญิ๋ง\' ป้อ',
        },
        text: 'ต้องมีคุณสมบัติอะไรบ้างคะ ขอรายละเอียดด้วยค่ะ',
        post_time: '2017-10-27 17:00:00',
        type: 'reply-comment',
      },
    ]
  }
})