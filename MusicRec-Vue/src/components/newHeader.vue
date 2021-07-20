<template>
  <div class="reHeader">
    <div class="headTop">
      <img class="topLogo" src="../assets/img/logo.png"/>
      <div class="userbtn">{{ getName }}，您好 <span @click="waitlayout" class="layouticon">切换用户</span></div>
    </div>
    <ul class="headNav">
      <li v-for="item in datas" :key="item.cate_id" @click="emitGetNews(item.cate_id)"
          :class="active==item.cate_id ? 'navActive':''">{{ item.cate_name }}
      </li>
      <li><a class="adminlink" :href="serverlink" target="_blank">进去后台</a></li>
    </ul>
  </div>
</template>

<script>
import {mapGetters, mapActions} from 'vuex'
import {getCateData, layout} from "../assets/js/api";
import {serverUrl} from "../assets/js/linkBase";

export default {
  data() {
    return {
      datas: [],
      serverlink: ''
    }
  },
  props: {
    active: String
  },
  computed: {
    ...mapGetters('vuexlogin', {
      getLogin: 'getLogin',
      getName: 'getName'
    })
  },
  methods: {
    ...mapActions('vuexlogin', {
      almuta: 'almuta',
      almuuser: 'almuuser'
    }),
    emitGetNews: function (cateid) {
      this.$emit('onGetnews', {'cateid': cateid})
    },
    waitlayout: function () {
      this.$layer.confirm('确定退出当前用户，切换其他用户?', {title: '亲~'}, () => {
        this.layout()
        this.$layer.closeAll()
      })
    },
    layout: function () {
      layout().then((res) => {
          if (res.code) {
            localStorage.removeItem('newlogintime')
            localStorage.removeItem('username', '')
            localStorage.removeItem('islogin', false)
            this.almuta(localStorage.getItem('islogin'))
            this.almuuser(localStorage.getItem('username'))
            this.$router.push('/login')
          }
        }, (err) => {
          console.log(err)
        }
      )
    },
    getCates: function () {
      this.loading('加载中。。。')
      getCateData().then((res) => {
        if (!res.code) {
          this.layout()
        } else {
          this.$layer.closeAll()
          this.datas = res.data
        }
      }, (err) => {
        this.$layer.msg('小主稍等，紧急恢复中。。。')
      })
    }
  },
  mounted() {
    this.serverlink = serverUrl + '/admin/'
    this.getCates()
  }
}
</script>
