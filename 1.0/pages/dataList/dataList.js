Page({
  data: {
    bodyData: []
  },

  onLoad() {
    const bodyData = wx.getStorageSync('bodyData') || [];
    this.setData({ bodyData });
  },

  deleteData(e) {
    const index = e.currentTarget.dataset.index;
    const bodyData = this.data.bodyData;
    bodyData.splice(index, 1);
    wx.setStorageSync('bodyData', bodyData);
    this.setData({ bodyData });
    wx.showToast({ title: '删除成功', icon: 'success' });
  },

  clearAllData() {
    wx.showModal({
      title: '确认清空',
      content: '是否确定清空所有历史数据？此操作不可恢复！',
      success: (res) => {
        if (res.confirm) {
          wx.setStorageSync('bodyData', []);
          this.setData({ bodyData: [] });
          wx.showToast({ title: '已清空全部数据', icon: 'success' });
        }
      }
    });
  },

  goToRecorder() {
    // 确保这里是标准的 wx.navigateTo，没有拼写错误
    wx.navigateTo({
      url: '/pages/recorder/recorder'
    });
  }
});