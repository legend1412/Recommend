import fetch from '../../axios/fetch'
// 获取用户以及标签
export const getLogin = () => fetch('/api/indexbook/login/', '', 'get')
// 登录
export const login = (loginInfo) => fetch('/api/indexbook/login/', loginInfo, 'post')
// 退出切换用户
export const layout = () => fetch('/api/indexbook/switchuser/', '', 'get')
// 主页分类数据
export const getMainData = (getData) => fetch('/api/indexbook/home/', getData, 'get')
// 主页分类详情
export const getOneData = (oneData) => fetch('/api/indexbook/one/', oneData, 'get')
// 足迹
export const getHistory = (hisData) => fetch('/api/indexbook/history/', hisData, 'get')
