import fetch from '../../axios/fetch'
//主页分类数据
export const getCateMusicData=(getdata)=>fetch('/api/indexmusic/home/',getdata,'get')
//主页分类
export const getCateData=()=>fetch('/api/indexmusic/getCates/','','get')
//推荐模块
export const getRecommon=(recommon)=>fetch('/api/indexmusic/rec/',recommon,'get')
//详细歌单列表模块
export const getplaylist = (onename)=>fetch('/api/playlist/one/',onename,'get')
//详细歌曲模块
export const getsonglist=(onename)=>fetch('/api/song/one/',onename,'get')
//详细歌手模块
export const getsinglist=(onename)=>fetch('/api/sing/one/',onename,'get')
//详细列表模块
export const getuserlist=(onename)=>fetch('/api/user/one/',onename,'get')
//推荐模块
export const getNewsData=(newsInfo)=>fetch('/api/news/one',newsInfo,'get')
//获取用户以及标签
export const getLogin=()=>fetch('/api/indexmusic/login/','','get')
//登录
export const login=(logininfo)=>fetch('/api/indexmusic/login/',logininfo,'post')
//退出切换用户
export const layout=()=>fetch('/api/indexmusic/switchuser','','get')
