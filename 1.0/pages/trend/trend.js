import wxCharts from '../../miniprogram_npm/wx-charts/wx-charts.js';

Page({
  data: {
    bodyData: []
  },

  onLoad() {
    // 读取本地存储的身体数据
    const bodyData = wx.getStorageSync('bodyData') || [];
    this.setData({ bodyData });
    
    if (bodyData.length === 0) {
      wx.showToast({ title: '暂无数据', icon: 'none' });
      return;
    }
    this.drawCharts(bodyData);
  },

  // 绘制图表
  drawCharts(data) {
    // 适配不同屏幕宽度
    const windowWidth = wx.getSystemInfoSync().windowWidth - 60;
    
    // 处理X轴标签（取记录时间的简化版，避免文字过长）
    const xAxis = data.map((item, index) => {
      // 截取时间的“月-日 时:分”部分
      return item.recordTime.substring(5, 16);
    });
    
    // 提取各维度数据
    const heartRate = data.map(item => item.heartRate);
    const systolic = data.map(item => item.systolic);
    const diastolic = data.map(item => item.diastolic);
    const weight = data.map(item => item.weight);

    // 1. 心率折线图
    new wxCharts({
      canvasId: 'heartRateChart',
      type: 'line',
      categories: xAxis,
      series: [{
        name: '心率',
        data: heartRate,
        color: '#e74c3c',
        format: function (val) {
          return val + ' 次/分';
        }
      }],
      width: windowWidth,
      height: 300,
      yAxis: {
        min: Math.min(...heartRate) - 10, // Y轴最小值（留余量）
        max: Math.max(...heartRate) + 10  // Y轴最大值（留余量）
      },
      legend: false,
      animation: true
    });

    // 2. 收缩压折线图
    new wxCharts({
      canvasId: 'systolicChart',
      type: 'line',
      categories: xAxis,
      series: [{
        name: '收缩压',
        data: systolic,
        color: '#3498db',
        format: function (val) {
          return val + ' mmHg';
        }
      }],
      width: windowWidth,
      height: 300,
      yAxis: {
        min: Math.min(...systolic) - 10,
        max: Math.max(...systolic) + 10
      },
      legend: false,
      animation: true
    });

    // 3. 舒张压折线图
    new wxCharts({
      canvasId: 'diastolicChart',
      type: 'line',
      categories: xAxis,
      series: [{
        name: '舒张压',
        data: diastolic,
        color: '#2ecc71',
        format: function (val) {
          return val + ' mmHg';
        }
      }],
      width: windowWidth,
      height: 300,
      yAxis: {
        min: Math.min(...diastolic) - 10,
        max: Math.max(...diastolic) + 10
      },
      legend: false,
      animation: true
    });

    // 4. 体重折线图
    new wxCharts({
      canvasId: 'weightChart',
      type: 'line',
      categories: xAxis,
      series: [{
        name: '体重',
        data: weight,
        color: '#f39c12',
        format: function (val) {
          return val + ' kg';
        }
      }],
      width: windowWidth,
      height: 300,
      yAxis: {
        min: Math.min(...weight) - 2,
        max: Math.max(...weight) + 2
      },
      legend: false,
      animation: true
    });
  },

  // 跳转到数据录入页
  goToRecorder() {
    wx.navigateTo({
      url: '/pages/recorder/recorder'
    });
  }
});