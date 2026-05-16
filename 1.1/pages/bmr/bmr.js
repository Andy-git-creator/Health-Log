Page({
  data: {
    genderArray: ["男", "女"],
    genderIndex: 0,
    activityArray: ["完全没有", "1-3次/周", "3-5次/周", "每天一次", "每天重度运动"],
    activityIndex: 0,
    result: null
  },
  onGenderChange(e) {
    this.setData({ genderIndex: parseInt(e.detail.value) });
  },
  onActivityChange(e) {
    this.setData({ activityIndex: parseInt(e.detail.value) });
  },
  onSubmit(e) {
    const f = e.detail.value;
    const age = Number(f.age);
    const gender = this.data.genderArray[this.data.genderIndex];
    const height = Number(f.height);
    const weight = Number(f.weight);
    const activityRatio = [1.2, 1.3, 1.5, 1.7, 1.9][this.data.activityIndex];

    let bmr = gender === "男"
      ? 10 * weight + 6.25 * height - 5 * age + 5
      : 10 * weight + 6.25 * height - 5 * age - 161;
    let cal = (bmr * activityRatio).toFixed(2);

    this.setData({
      result: {
        bmr: bmr.toFixed(2),
        cal
      }
    });
  }
});