const util = require('../../utils/util.js');

Page({
  data: {
    heartRate: 0,
    systolic: 0,
    diastolic: 0,
    weight: 0
  },

  // 输入心率
  inputHeartRate(e) {
    this.setData({ heartRate: parseFloat(e.detail.value) || 0 });
  },
  // 输入收缩压
  inputSystolic(e) {
    this.setData({ systolic: parseFloat(e.detail.value) || 0 });
  },
  // 输入舒张压
  inputDiastolic(e) {
    this.setData({ diastolic: parseFloat(e.detail.value) || 0 });
  },
  // 输入体重
  inputWeight(e) {
    this.setData({ weight: parseFloat(e.detail.value) || 0 });
  },

  // 保存数据
  saveData() {
    const { heartRate, systolic, diastolic, weight } = this.data;
    // 验证数据
    if (heartRate < 30 || heartRate > 250) {
      wx.showToast({ title: '心率需在30-250之间', icon: 'none' });
      return;
    }
    if (systolic < 60 || systolic > 250) {
      wx.showToast({ title: '收缩压需在60-250之间', icon: 'none' });
      return;
    }
    if (diastolic < 40 || diastolic > 150) {
      wx.showToast({ title: '舒张压需在40-150之间', icon: 'none' });
      return;
    }
    if (systolic <= diastolic) {
      wx.showToast({ title: '收缩压必须大于舒张压', icon: 'none' });
      return;
    }
    if (weight < 0.1) {
      wx.showToast({ title: '体重最小为0.1kg', icon: 'none' });
      return;
    }

    // 构造数据
    const newData = {
      recordTime: util.formatTime(new Date()),
      heartRate,
      systolic,
      diastolic,
      weight
    };

    // 读取本地存储的历史数据
    const historyData = wx.getStorageSync('bodyData') || [];
    historyData.push(newData);

    // 保存到本地存储
    wx.setStorageSync('bodyData', historyData);

    wx.showToast({ title: '保存成功' });
    setTimeout(() => {
      wx.navigateBack();
    }, 1000);
  }
});