// index.js
Page({
  data: {
    show_fetched_Pic:false,
    show_selected_Pic:false,
    imgGot:'',//存放从后端请求到的图片路径
    imgSrc:'',//存放前端选择和要上传的图片路径
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: "log in",  // 根据实际需求设置标题
    });
  },
  navigateToChat_Alice: function () {
    wx.redirectTo({
      url: '/pages/chat/chat?param=0',
    });
  },
  navigateToChat_Bob: function () {
    // 使用 wx.redirectTo 跳转到第二页
    wx.redirectTo({
      url: '/pages/chat/chat?param=1',
    });
  },
})
