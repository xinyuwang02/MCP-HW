// pages/chat/chat.js
Page({
  data: {
    domain_name:'',
    user_id: 0,// 0: Alice, 1: Bob 默认值是0
    inputText: '', //输入框获取的文本
    message_list: [],//存储消息的数组，此处的消息是明文
    imgSrc:'',
    imgStr:'',//图片Base64编码后的字符串
    my_key : new Uint8Array(16),
    other_key : new Uint8Array(16),
  },
  // 监听输入框的值变化
  onInputTextChange: function (e) {
    this.setData({
      inputText: e.detail.value
    });
  },
  //向后端请求并同步消息数组
  update_message_list:function(){
    const that = this;
    wx.request({
      url: that.data.domain_name + `/new_msg_polling/${that.data.user_id}`,
      method: 'GET',
      success: function (res) {
        if (res.data === true) { // 如果后端返回布尔值为 true，表示有新消息
          that.fetchNewMessages(); // 执行获取新消息的函数
        }
      },
      fail: function (error) {
        console.error('Failed to poll for new messages:', error);
      }
    });
    
  },
  
  // 定义一个函数，用于从图片序号请求图片
  fetchImage:function(img_id) {
    var that=this;
    return new Promise((resolve, reject) => {
      wx.request({
        url: that.data.domain_name + '/get_image/' +that.data.user_id.toString()+'/'+img_id,
        responseType: 'arraybuffer',
        success: function (res) {
          if (res.statusCode == 200) {
            console.log("img successfully fetch!")
            // 图片的 Base64 字符串
            const base64data = 'data:image/jpeg;base64,' + wx.arrayBufferToBase64(res.data);
            resolve(base64data);
            //（对方密钥更新）
            //res.data就是arrayBuffer
            const other_new_key=that.new_key(res.data);
            that.setData({
              other_key: other_new_key,
            });
            console.log("更新对方的密钥： ",that.data.other_key)
          } else {
            reject('Failed to fetch image');
          }
        },
        fail: function (error) {
          reject('Request failed: ' + error);
        }
      });
    });
  },

  // 使用递归来处理消息列表
  processMessages:function(index, messages, message_list) {
    var that=this;
    if (index < messages.length) {
      const new_msg = messages[index];
      if (new_msg.type === 1) {
        //如果是图片
        const img_id = new_msg.text;
        console.log("A pic detected: ", img_id);
        // 发送图片请求
        that.fetchImage(img_id)
          .then((base64data) => {
            new_msg.text = base64data;
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(() => {
            // 处理下一条消息
            message_list.push(new_msg);
            console.log("push an img msg");
            that.processMessages(index + 1, messages, message_list);
          });
      } else {
        // 如果是文字
        //（添加解密）因为是异或，所以直接用加密函数解密
        const de_msg=that.encryptMessage(that.data.other_key,new_msg.text);
        new_msg.text=de_msg;
        message_list.push(new_msg);
        console.log("push a text msg", new_msg);
        that.processMessages(index + 1, messages, message_list);
      }
    }
    else{
      that.setData({
        message_list
      });
      console.log("message list update!")
    }
  },
  // 获取新消息的函数
  fetchNewMessages: function () {
    const that = this;
    wx.request({
      url:that.data.domain_name +  `/download_messages/${that.data.user_id}`,
      method: 'GET',
      success: function (res) {
          const newMessages = res.data;
          const message_list = that.data.message_list;
          that.processMessages(0, newMessages, message_list);//用递归代替for循环
          
      },
      fail: function (error) {
        console.error('Failed to fetch new messages:', error);
      }
    });
  },
  // 发送消息
  sendMessage: function () {
    var that=this;
    const inputText = that.data.inputText;
    if (inputText) {
      //（添加加密后的文本）
      const en_msg=that.encryptMessage(that.data.my_key, inputText)
      const message_list = that.data.message_list;
      that.update_message_list();
      const user_id = that.data.user_id;//用户ID
      const date = new Date(); // 获取当前日期时间对象
      const timestamp = date.toLocaleString('zh-CN', { hour12: false }); //转换为字符串作为时间戳
      console.log(timestamp);
      const a_message_to_be_sent = {// 一条将被发送的消息对象
        text: en_msg,//密文
        timestamp: timestamp,
        type: 0,
        sender: user_id
      };
      // 发送 POST 请求将新消息传递给后端
      wx.request({
        url:that.data.domain_name + `/upload_message/${user_id}`, 
        method: 'POST',
        data: a_message_to_be_sent,
        success: function (res) {
          console.log('sent successfully:', res);
        },
        fail: function (error) {
          console.error('Failed to send:', error);
        }
      });
      a_message_to_be_sent.text=inputText;//将明文重新写回
      message_list.push(a_message_to_be_sent);
      that.setData({
        message_list,
        inputText: '' // 清空输入框
      });
    }
  },
  visit_gallery_and_send: function(){
    var that=this;
    wx.chooseMedia({
      count:1,
      success:function(res){
        var tmpPath=res.tempFiles[0].tempFilePath;
        that.setData({
          imgSrc:tmpPath,
        });
        //至此图片路径已经记录好了，下面发送
        that.send_img();
      }
    });
  },

  send_img: function(){
    var that=this;
    var tempFilePath=that.data.imgSrc;
    const date = new Date();
    const timestamp = date.toLocaleString('zh-CN', { hour12: false });
    //使用wx.uploadFile上传图片
    wx.uploadFile({
      url: that.data.domain_name + '/upload_image/',
      filePath: tempFilePath,
      name: 'image',
      method: 'POST',
      //formData设置 HTTP 请求中的表单数据，即要随文件一起上传的额外数据
      formData:{
        timestamp: timestamp,
        sender: that.data.user_id
      },
      success:function(res){
        console.log("Frontend img successfully upload!")
        console.log(res)
        //(自己密钥更新)
        //由图片路径更新my_key
        that.update_my_key(tempFilePath);
        //把图片消息写入message_list
        const message_list = that.data.message_list;
        that.update_message_list();
        const img_as_msg = {
          text: tempFilePath,
          timestamp: timestamp,
          type: 1,
          sender: that.data.user_id
        };
        message_list.push(img_as_msg);
        that.setData({
          message_list,
        });
      }
    });
  },

  // 简单异或加密函数，参数是字节数组形式的密钥和字符串格式的密文
  encryptMessage: function(keyBytes, message) {
    var that=this
    // 将消息转换为字节数组
    const messageBytes= message.split('').map(char => char.charCodeAt(0));
    const encryptedBytes = messageBytes.map((byte, index) => byte ^ keyBytes[index % keyBytes.length]);
    // 将加密后的字节数组转换为字符串
    const encryptedMessage = String.fromCharCode(...encryptedBytes);
    console.log(message.length,"vs",encryptedMessage.length)
    return encryptedMessage;
  },

  //由路径更新密钥
  update_my_key: function(path){
    const fs = wx.getFileSystemManager();
    fs.readFile({
      filePath: path,
      success: (fileData) => {
        // fileData.data 就是 ArrayBuffer
        const my_new_key = this.new_key(fileData.data);
        this.setData({
          my_key: my_new_key,
        });
        console.log("更新我的密钥： ",this.data.my_key)
      },
    });
  },
  //由图片的arrayBuffer 返回密钥（字节数组）
  new_key: function(arrayBuffer){
    // 获取JPEG的第241到256字节
    const myKeyArrayBuffer = arrayBuffer.slice(240, 256);
    // 字节数组
    const myKeyByteArray = new Uint8Array(myKeyArrayBuffer);
    return myKeyByteArray;
  },
  //初始化两个密钥，解决重新进入时不知道密钥的问题
  //然后初始化消息列表
  init_keys_and_update_messages: function(){
    var that=this;
    //先初始化自己的密钥
    wx.request({
      url:that.data.domain_name +  `/init_keys/${that.data.user_id}/0`,
      responseType: 'arraybuffer',
      success: function (res) {
        if (res.statusCode == 200) {
            console.log("收到自己的密钥图片了")
            const my_new_key=that.new_key(res.data);
            that.setData({
              my_key: my_new_key,
            });
            console.log("初始化自己的密钥： ",that.data.my_key);
        }
        //初始化对方的密钥
        wx.request({
          url:that.data.domain_name +  `/init_keys/${that.data.user_id}/1`,
          responseType: 'arraybuffer',
          success: function (res1) {
            if (res1.statusCode == 200) {
                console.log("收到对方的密钥图片了")
                const other_new_key=that.new_key(res1.data);
                that.setData({
                  other_key: other_new_key,
                });
                console.log("初始化对方的密钥： ",that.data.other_key);
            }
            that.update_message_list();       
          }
        })

      }
    })
  },
  //跳转到拍照页面的函数
  navigateToCamera: function () {
    wx.navigateTo({
      url: '/pages/camera/camera',
    });
  },
  // 开始定时执行 update_message_list
  startInterval: function () {
    this.intervalId = setInterval(this.update_message_list.bind(this), 2000);
  },
  // 停止定时执行 update_message_list
  stopInterval: function () {
    clearInterval(this.intervalId);
  },
  onLoad(options) {
    var that=this;
    const param = options.param;//启动页面时，param代表了用户身份
    console.log('Received parameter:', param);
    that.setData({
      user_id:param,
    });
    console.log('user_id:', that.data.user_id);
    //此处需要先向后端请求自己和对方的密钥，再同步消息列表
    that.init_keys_and_update_messages();
    that.startInterval();
  },
  onUnload: function () {
    this.stopInterval();
  }
})