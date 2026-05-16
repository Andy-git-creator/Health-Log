Page({
  data: {
    typeArray: ["BMI", "CMI"],
    typeIndex: 0,
    bmiStdArray: ["亚洲", "国际"],
    bmiStdIndex: 0,
    result: ''
  },
  onTypeChange(e) {
    this.setData({ typeIndex: parseInt(e.detail.value), result: '' });
  },
  onBMIStdChange(e) {
    this.setData({ bmiStdIndex: parseInt(e.detail.value) });
  },
  onSubmit(e) {
    const v = e.detail.value;
    let res = '';
    if (this.data.typeIndex == 0) {
      // BMI
      const h = Number(v.bmi_height), w = Number(v.bmi_weight);
      if (!h || !w) return;
      const bmi = w / Math.pow(h / 100, 2);
      let msg = '', std = this.data.bmiStdArray[this.data.bmiStdIndex];
      if (std === "亚洲") {
        if (bmi < 18.5) msg = "低体重（营养不足）";
        else if (bmi < 23) msg = "正常体重";
        else if (bmi < 25) msg = "超重";
        else if (bmi < 30) msg = "中度肥胖";
        else msg = "严重肥胖";
      } else {
        if (bmi < 18.5) msg = "低体重（营养不足）";
        else if (bmi < 25) msg = "正常体重";
        else if (bmi < 30) msg = "超重";
        else if (bmi < 35) msg = "中度肥胖";
        else if (bmi < 40) msg = "严重肥胖";
        else msg = "极端肥胖";
      }
      res = `BMI=${bmi.toFixed(2)}，${msg}`;
    } else {
      // CMI
      const h = Number(v.cmi_height), w = Number(v.cmi_waist), tg = Number(v.cmi_tg), hdl = Number(v.cmi_hdl);
      if (!h || !w || !tg || !hdl) return;
      const cmi = (w / h) * (tg / hdl);
      let msg = '';
      if (cmi <= 0.85) msg = "正常";
      else if (cmi > 1.42) msg = "高风险";
      else msg = "有风险";
      res = `CMI=${cmi.toFixed(3)}，${msg}`;
    }
    this.setData({ result: res });
  }
});