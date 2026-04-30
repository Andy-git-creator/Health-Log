Page({
  data: {
    activeTab: 'bmi',
    standard: 1,
    height: 0,
    weight: 0,
    bmiValue: 0,
    bmiDesc: '',
    bmiResult: false,
    resultColor: '',
    // CMI相关
    cmiHeight: 0,
    waist: 0,
    tg: 0,
    hdl: 0,
    cmiValue: 0,
    cmiDesc: '',
    cmiResult: false,
    cmiColor: ''
  },

  // 切换标签
  switchTab(e) {
    this.setData({
      activeTab: e.currentTarget.dataset.tab
    })
  },

  // 选择BMI标准
  changeStandard(e) {
    this.setData({
      standard: parseInt(e.detail.value)
    })
  },

  // 输入身高（BMI）
  inputHeight(e) {
    this.setData({
      height: parseFloat(e.detail.value) || 0
    })
  },

  // 输入体重（BMI）
  inputWeight(e) {
    this.setData({
      weight: parseFloat(e.detail.value) || 0
    })
  },

  // 计算BMI
  calcBMI() {
    const { height, weight, standard } = this.data;
    if (height <= 0 || weight <= 0) {
      wx.showToast({ title: '请输入有效数值', icon: 'none' });
      return;
    }
    // BMI公式：体重(kg) / (身高(m))²
    const bmi = weight / Math.pow(height / 100, 2);
    let desc = '';
    let color = '';

    // 亚洲标准
    if (standard === 1) {
      if (bmi < 18.5) {
        desc = '低体重（营养不足）';
        color = '#f44336';
      } else if (bmi < 23.0) {
        desc = '正常体重';
        color = '#4CAF50';
      } else if (bmi < 25.0) {
        desc = '肥胖前期（超重）';
        color = '#ff9800';
      } else if (bmi < 30.0) {
        desc = '一级肥胖（中度肥胖）';
        color = '#9c27b0';
      } else {
        desc = '二级肥胖（严重肥胖）';
        color = '#f44336';
      }
    } else {
      // 国际标准
      if (bmi < 18.5) {
        desc = '低体重（营养不足）';
        color = '#f44336';
      } else if (bmi < 25.0) {
        desc = '正常体重';
        color = '#4CAF50';
      } else if (bmi < 30.0) {
        desc = '肥胖前状态（超重）';
        color = '#ff9800';
      } else if (bmi < 35.0) {
        desc = '肥胖I级（中度肥胖）';
        color = '#2196F3';
      } else if (bmi < 40.0) {
        desc = '肥胖II类（严重肥胖）';
        color = '#9c27b0';
      } else {
        desc = '⚠️肥胖III类（极端肥胖）';
        color = '#f44336';
      }
    }

    this.setData({
      bmiValue: bmi,
      bmiDesc: desc,
      bmiResult: true,
      resultColor: color
    });
  },

  // CMI输入相关
  inputCMIHeight(e) {
    this.setData({ cmiHeight: parseFloat(e.detail.value) || 0 });
  },
  inputWaist(e) {
    this.setData({ waist: parseFloat(e.detail.value) || 0 });
  },
  inputTG(e) {
    this.setData({ tg: parseFloat(e.detail.value) || 0 });
  },
  inputHDL(e) {
    this.setData({ hdl: parseFloat(e.detail.value) || 0 });
  },

  // 计算CMI
  calcCMI() {
    const { cmiHeight, waist, tg, hdl } = this.data;
    if (cmiHeight <= 0 || waist <= 0 || tg <= 0 || hdl <= 0) {
      wx.showToast({ title: '请输入有效数值', icon: 'none' });
      return;
    }
    // CMI公式：(腰围/身高) * (甘油三酯/高密度脂蛋白)
    const cmi = (waist / cmiHeight) * (tg / hdl);
    let desc = '';
    let color = '';

    if (cmi <= 0.85) {
      desc = '正常';
      color = '#4CAF50';
    } else if (cmi > 1.42) {
      desc = '高风险';
      color = '#f44336';
    } else {
      desc = '有风险';
      color = '#ff9800';
    }

    this.setData({
      cmiValue: cmi,
      cmiDesc: desc,
      cmiResult: true,
      cmiColor: color
    });
  }
});