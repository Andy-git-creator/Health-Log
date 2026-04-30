Page({
  // 跳转到BMI/CMI计算页
  goToCalculator() {
    wx.navigateTo({
      url: '/pages/calculator/calculator'
    })
  },
  // 跳转到数据记录页
  goToRecorder() {
    wx.navigateTo({
      url: '/pages/recorder/recorder'
    })
  },
  // 跳转到历史数据页
  goToDataList() {
    wx.navigateTo({
      url: '/pages/dataList/dataList'
    })
  },
  // 跳转到趋势图表页
  goToTrend() {
    wx.navigateTo({
      url: '/pages/trend/trend'
    })
  },
  // 显示联系信息
  showContact() {
    wx.showModal({
      title: '联系我们',
      content: 'email: czyandyac@gmail.com\ngithub: Andy-git-creator',
      showCancel: false
    })
  }
})