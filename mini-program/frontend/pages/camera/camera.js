// pages/camera/camera.js
Page({
  data: {
    photoPath: '' // 存储拍摄照片的临时路径
  },

  takePhoto: function () {
    const context = wx.createCameraContext(); // 创建摄像头上下文
    context.takePhoto({
      quality: 'high',
      //默认就是JPEG格式(jpg)
      success: (res) => {
        //拍摄成功PhotoPath就不为空了
        const photoPath = res.tempImagePath;
        this.setData({
          photoPath
        });
      }
    });
  },

  sendPhoto: function () {
    const photoPath = this.data.photoPath;
    if (photoPath) {
      // 获取聊天页面的实例
      const pages = getCurrentPages();
      const chatPage = pages[pages.length - 2]; 
      // 将拍摄的照片路径传递给聊天页面
      chatPage.setData({
        imgSrc: this.data.photoPath
      });
      // 返回聊天页面，并传递数据
      wx.navigateBack({
        delta: 1,
        success: function () {
          chatPage.send_img();
        }
      });
    } else {
      wx.showToast({
        title: '请先拍摄照片',
        icon: 'none'
      });
    }
  }
});
