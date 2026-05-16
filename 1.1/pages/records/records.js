function format(d) {
  return `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()} ${d.getHours()}:${d.getMinutes()}`
}
Page({
  data: {
    list: [],
    showCanvas: false,
    weights: []
  },
  onLoad() {
    let d = wx.getStorageSync('bodydata') || [];
    this.setData({ list: d });
  },
  onRecord(e) {
    const v = e.detail.value;
    const item = {
      time: format(new Date()),
      heart: Number(v.heart),
      sbp: Number(v.sbp),
      dbp: Number(v.dbp),
      weight: Number(v.weight)
    }
    let nL = [...(this.data.list), item];
    this.setData({ list: nL });
    wx.setStorageSync('bodydata', nL);
    wx.showToast({title:'保存成功',icon:'success'});
  },
  showTrend() {
    this.setData({ showCanvas:true });
    const list = this.data.list, w = 280, h = 200;
    if (!list.length) return wx.showToast({title:'暂无数据', icon:'none'});
    const weights = list.map(x=>x.weight);
    const ctx = wx.createCanvasContext('trend', this);
    ctx.setFillStyle("#fff");
    ctx.fillRect(0,0,w,h);
    ctx.setStrokeStyle("#7B5BAA");
    ctx.setLineWidth(3);
    ctx.beginPath();
    let minW = Math.min(...weights), maxW = Math.max(...weights);
    let left = 30, right = w-30, top = 30, bot = h-30;

    weights.forEach((ww, i) => {
      let x = left + (right-left)*i/(weights.length-1);
      let y = bot - ( (ww-minW) / (maxW-minW+0.1) )*(bot-top);
      if(i===0) ctx.moveTo(x,y);
      else ctx.lineTo(x,y);
    });
    ctx.stroke();
    ctx.draw();
  },
  hideTrend() {
    this.setData({showCanvas:false});
  },
  onDeleteRecord(e) {
    const idx = e.currentTarget.dataset.index;
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条记录吗？',
      success: (res) => {
        if (res.confirm) {
          let nL = [...this.data.list];
          nL.splice(idx, 1);
          this.setData({ list: nL });
          wx.setStorageSync('bodydata', nL);
          wx.showToast({title:'已删除',icon:'success'});
        }
      }
    });
  },

  onClearAll() {
    wx.showModal({
      title: '��空全部',
      content: '确定要清空所有历史记录吗？此操作不可恢复。',
      success: (res) => {
        if(res.confirm){
          this.setData({ list: [] });
          wx.removeStorageSync('bodydata');
          wx.showToast({title:'已清空',icon:'success'});
        }
      }
    });
  },
});