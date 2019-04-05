# 时光网Javascript开发文档

```
//后台
106.13.106.1/admin
public
public123
```



- 一切皆对象

  - user类使用**单例**模式，通过历遍对象属性取出（完成）
  - 表单验证使用**策略**模式（完成）
  - 表单验证规则封装进一个常量类（完成）
  - 向服务器请求数据一律使用Promise对象，回调函数自己滚回去封装（完成）
  - 获取验证码有bug
  - **注意将程序后端接口封装进常量类**，以便后期修改
    - **完成首页图片预加载**
    - **完成个人首页图片上传的逻辑，测试使用本地tomcat测试**
      - **注意图片大小和格式**
    - **完成修改个人信息的逻辑**，**在本地tomcat测试**
    - **优化*注册*代码的结构，注意在本地tomcat测试**（闭包的内存释放）
    - **完成新闻页的逻辑，并尝试在远程服务器测试**
    - **优化UI界面的尺寸**，注意UI不合理的UI规划的尺寸

- **3.26**

  - 事件委托

    - focus、blur的事件处理

      - 事件冒泡：自子元素至父元素
      - 事件捕获：自父元素至子元素
      - DOM2级事件：
        - 包含三个阶段，事件捕获阶段、处于目标阶段、事件冒泡阶段
      - DOM2级事件监听器
        - addEventListener、removeEventListener
          - 第三个参数可以接受Boolean类
            - true：在捕获阶段调用事件处理程序
            - false：在冒泡阶段调用事件处理程序
      - 焦点事件focus、blur不会冒泡

      ```javascript
      function inputFocusHandler(event){
          let target = getTarget(event);
          target.style.borderColor = "rgba(91,136,180,1)";
      }
      function inputBlurHandler(event){
          let target = getTarget(event);
          validator.validate(target);
      }
      //解决方案
      registerForm.addEventListener("focus", inputFocusHandler, true);
      registerForm.addEventListener("blur", inputBlurHandler, true);
      ```

      

- **3.27**

  - JSON复习
    - 文件类型：.json
    - MINE类型：application/json
      - MINE：多用途互联网邮件扩展程序。设定某种扩展名的文件用一种应用程序来打开的方式，当该扩展名文件被访问的时候，浏览器会自动使用指定类型的应用程序来打开。
    - JSON.parse(string)：解析string并转化为json数据

  - AJAX

    ```javascript
    //创建XMLHttpRequest
    let variable = new XMLHttpRequest();
    //IE
    let variable = new ActiveXObject("Microsoft.XMLHTTP");
    
    //适应浏览器
    var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    
    //向服务器发送请求
    //规定请求类型
    xml.open(method, url, async);
    //method: GET/POST
    //url
    //async: true 异步/false 同步
    //将请求发送至服务器0
    ```

    

  - $.ajax()方法

    ```javascript
    //jQuery.ajax([settings]);
    //参数
    options
    //Object,ajax请求设置，所有选项都可选
    async
    //Boolean，默认为true（异步）
    beforeSend(XHR)
    //function 发送请求前可以修改XMLHttpRequest对象，如定义HTTP头,ajax事件
    complete(XMLHTTPRequest, string)
    //function 回调函数，ajax事件
    contentType
    类型：String
    
    默认值: "application/x-www-form-urlencoded"。发送信息至服务器时内容编码类型。
    
    默认值适合大多数情况。如果你明确地传递了一个 content-type 给 $.ajax() 那么它必定会发送给服务器（即使没有数据要发送）。
    ```

    

    - 使用ajax提交表单

      ```javascript
      //表单序列化
      formNode.serialize();
      
      ```

      

- 3.28

  - JSON对象

    ```javascript
    JSON.parse()将JSON转化为Object
    JSON.stringify()将Object转化为JSONn'h'h
    ```

    

  - Promise对象

    ```javascript
    let promise = new Promise((resolve, reject) => {
        if(success){
            resolve(res);
        }else{
            reject(err);
        }
    });
    new Promise((resolve, reject) => {
        if(success){
            resolve(res);
        }else{
            reject(err);
        }
    })
    
    promise.then(result => {
        
    }, error=>{
        
    }).catch(err => {
        
    });
    
    ```

  - AJAX

    ```javascript
    //$.ajax()会将返回值返回给success回调函数的返回值
    //获取json
    //设置dataType为json
    //发送json
    //设置contentType为application/json;charset=utf-8
    new Promise((resolve, reject) => {
            $.ajax({
                url: (ServerURL())(),
                type: "get",
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                data: formSerialize(),
                success: resolve(data),
                error: reject(data)
            })
        });
    ```

    

  - 请求本地文件

    ```
    status 值会由以下几个步骤确定：
    
        1.If the state is UNSENT or OPENED, return 0.
    
        2.If the error flag is set, return 0.
    
        3.Return the HTTP status code.
    
    也就是说，如果 readyState 是 UNSENT（0）或 OPENED（1）状态，status 返回值为 0；如果出现某种网络错误或者请求终止，error flag 就会由 unset 变为 set，status 返回值也为 0；否则，返回 http 状态码。
    ```

    

  - 我的tomcatURL：[http://127.0.0.1:8080](http://127.0.0.1:8080/)

  - ![1553760357058](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\1553760357058.png)

- 上传文件，contentType设置为false