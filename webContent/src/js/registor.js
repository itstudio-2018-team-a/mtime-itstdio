/**
*注册规格
* 用户名：允许使用 数字+字母+下划线 长度6-16字符
* 密码：允许使用 数字+字母+特殊字符 长度6-16字符
* 昵称： 禁止使用 特殊字符、Unicode扩展区文字（如果可以实现） 长度1-20字符
* 头像：提供默认头像，个人上传大小不超过2MB，不提供裁剪功能
* */
const confirm_password = "confirm_password";
const ensure_code = "ensure_code";
const ServerURL = function () {
    let __URL =  "106.13.106.1";  //在ajax属性内拼接
    return ()=>{
        return __URL;
    }
};
const Url_Options = {
    VERIFY_CODE: "\\i\\verify_code",
    VERIFY_PICTURE: "\\i\\verify_code_picture",
    REGISTER: "\\account\\i\\register"
};
const RegExpPattern = { //匹配模式
    USERNAME_PATTERN: /^\w+$/,
    PASSWORD_PATTERN: /^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/,
    NICKNAME_PATTERN: /^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/,
    EMAIL_PATTERN: /^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/,
    ENSURE_PATTERN: ""
};
const ErrorMessage = {   //错误信息
    IS_EMPTY: "不能为空",
    NICKNAME_PATTERN: "请使用数字+字母+下划线",
    PASSWORD_PATTERN: "请使用数字+字母+特殊字符",
    CONFIRM_PASSWORD: "两次输入的密码不相同",
    EMAIL_PATTERN: "邮箱格式不正确",
    ENSURE_CODE: "验证码不正确",
    CHINESE_PATTERN_ERROR: "内容包含中文"
};
function getType(valueType) {   //获取匹配模式
    let types = {
        'username': ()=>{ return RegExpPattern.USERNAME_PATTERN},
        'password': ()=>{ return RegExpPattern.PASSWORD_PATTERN},
        'nickname': ()=>{ return RegExpPattern.NICKNAME_PATTERN},
        'email': ()=> {return RegExpPattern.EMAIL_PATTERN},
        'ensure_code': ()=>{return RegExpPattern.ENSURE_PATTERN}
    };
    return ((types[valueType])());
}
/*
标识input状态
 */
let InputStatus = function () {
    this.username = "0";
    this.password = "0";
    this.nickname = "0";
    this.confirm_password = "0";
    this.email = "0";
    this.ensure_code = "0";
};
InputStatus.prototype.setStatus = function(name, value){
    this[name] = value;
};
InputStatus.prototype.getStatus = function(){
    let flag = true;
    let status = Object.getOwnPropertyNames(this);
    for(let i in status){
        console.log(this[status[i]]);
        if(this[status[i]] === "0"){
            flag = false;
            break;
        }
    }
    return flag;
};
let inputStatus = new InputStatus();

/*
校验策略组
 */
let CheckValidationStrategies = {
    isEmpty: (value)=>{ //判断是否为空
        if(value === ""){
            return ErrorMessage.IS_EMPTY;
        }
    },
    hasChinese: (value)=>{  //判断内容是否包含中文
        let ChineseReg = new RegExp(RegExpPattern.CHINESE_PATTERN);
        if(ChineseReg.test(value)){
            return ErrorMessage.CHINESE_PATTERN_ERROR;
        }
    },
    checkBaseValidate: function(value){
      let errorMessage;
      errorMessage = this.isEmpty(value);
      if(errorMessage){
          return errorMessage;
      }
      errorMessage = this.hasChinese(value);
      if(errorMessage){
          return errorMessage;
      }
    },
    checkValidate: function(value, regType){    //value待判断的值，regType为正则匹配模式的类型
        let errorMessage = this.checkBaseValidate(value);
        if(errorMessage){
            return errorMessage;
        }else{
            let typeReg = new RegExp(RegExpPattern[regType]);
            if(!typeReg.test(value)){
                return ErrorMessage[regType];
            }
        }
    },
    confirmPassword: function (password, password_confirm) {
        if(password !== password_confirm){
            return ErrorMessage.CONFIRM_PASSWORD;
        }
    }
};

/*
校验业务组
 */
let Validator = function () {};
const validator = new Validator();
Validator.prototype.validate = function (dom) {
    if(dom.name === confirm_password){
        return CheckValidationStrategies.confirmPassword(document.getElementById("password").value, dom.value);
    }else if(dom.name === ensure_code){
        return CheckValidationStrategies.checkBaseValidate(dom.value);
    }else{
        let type = getType(dom.name);
        return CheckValidationStrategies.checkValidate(dom.value, type);
    }
};

let registerForm = document.getElementById("register");
let submit = document.getElementById("submit");

/*
事件处理
 */
function getTarget(event) { //获取事件目标
    return event.target || target.srcElement;
}
function inputFocusHandler(event){
    let target = getTarget(event);
    target.style.borderColor = "rgba(91,136,180,1)";
}
function inputBlurHandler(event){
    let target = getTarget(event);
    let message =  validator.validate(target);
    if(message){
        inputStatus.setStatus(target.name, 0);
        target.style.borderColor = "red";
        let tips = target.parentNode.childNodes[3];
        tips.innerText = "*" + message;
        tips.style.color = "red";
    }else{
        inputStatus.setStatus(target.name, 1);
        target.style.borderColor = "green";
        let tips = target.parentNode.childNodes[3];
        tips.innerText = "";
    }
}
function submitHandler(){
    let status = inputStatus.getStatus();
    if(Number(status) === 0){
        alert("请完成表单填写");
        return false;
    }
    submit.style.background = "grey";
    submit.disabled = "disabled";
    let formJson = formSerialize();
    postFormInfo((ServerURL())() + Url_Options.REGISTER, formJson).then(json=>{
        let types = {
            "0": ()=>{alert("注册成功！")},
            "1": ()=>{alert("用户ID重复")},
            "2": ()=>{alert("电子邮箱已被注册")},
            "3": ()=>{alert("验证码错误")},
            "4": ()=>{alert("无效的用户名")},
            "5": ()=>{alert("无效的密码")},
            "6": ()=>{alert("未知错误")},
            "7": ()=>{alert("用户ID重复")}
        };
        let result = json["result"];
        (types[result])();
        if(result === "0"){
            window.location.href="login.html";
        }else{
            submit.removeAttribute("style");
            submit.removeAttribute("disabled");
        }
    });
    }
function postFormInfo(url, json) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = getXMLObject();
        xmlHttp.onreadystatechange = function () {
            console.log(this.status);
            console.log(this.readyState);
            if (this.status === 200 && this.readyState === 4) {
                resolve(this.response);
            }
        };
        xmlHttp.open("post", url, true);
        xmlHttp.responseType = type;
        xmlHttp.send(json);
    });
}

registerForm.addEventListener("focus", inputFocusHandler, true);
registerForm.addEventListener("blur", inputBlurHandler, true);
submit.onclick = submitHandler;

/*
序列化form表单
 */
function getFormJsonName(valueType) {   //获取匹配模式
    let types = {
        'username': ()=>{ return "user_id"},
        'password': ()=>{ return "password"},
        'nickname': ()=>{ return "user_name"},
        'email': ()=> {return "email"},
        'ensure_code': ()=>{return "verify_code"}
    };
    return ((types[valueType])());
}
function getFormJsonObject(){   //获取表单的name和value
    let inputArray = registerForm.getElementsByTagName("input");
    let formObj = {};
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name !== "confirm_password" && name !== "item" && name !== "namedItem"){
            formObj[getFormJsonName(name)] = input.value;
        }
    }
    return formObj;
}
let formSerialize = function () {   //OBject序列化为JSON
    let obj = getFormJsonObject();
    if(verifyCode){
        obj["verify_id"] = verifyCode.id;
    }
    return JSON.stringify(getFormJsonObject());
};


/*
* 验证码类
* 惰性创建对象
* 考虑使用单例模式
* */
let requestVerifyPicButton = document.getElementById("request_verify_img_button");
let verifyPic = document.getElementById("verify_img");
let verifyCode = {};
function getXMLObject() {
    let xmlHttp;
    if (window.XMLHttpRequest) {
        xmlHttp=new XMLHttpRequest();
    } else {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlHttp;
}
function requestVerifyCode(url, type) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = getXMLObject();
        xmlHttp.onreadystatechange = function () {
            console.log(this.status);
            console.log(this.readyState);
            if (this.readyState === 4) {
                if (this.status === 200) {
                    resolve(this.response);
                } else {
                    reject();
                }
            }
        };
        xmlHttp.open("GET", url);
        xmlHttp.responseType = type;
        xmlHttp.send(null);
    });
}
let requestVerifyCodeHandler = function () {
    let successHandler = (json)=>{  //object
        verifyCode = json;
        console.log(verifyCode);

        return requestVerifyCode((ServerURL())() + Url_Options.VERIFY_PICTURE + "\\" + verifyCode.id, "blob");
    };
    let failHandler = ()=>{
        alert("请求超时");
    };
    requestVerifyCode((ServerURL())() + Url_Options.VERIFY_CODE, "json").then((json)=>{
        return successHandler(json);
    },()=>{
        failHandler();
    }).then((blob)=>{
        verifyPic.onload = function () {
            window.URL.revokeObjectURL(verifyPic.src);
            return new Promise(((resolve, reject) => {
                let countDown = Number(verifyCode.wait);
                let setTime = ()=>{
                    if(countDown === 0){
                        requestVerifyPicButton.innerText = "获取验证码";
                        clearInterval(click);
                        requestVerifyPicButton.removeAttribute("disabled");
                    }else{
                        requestVerifyPicButton.disabled = "disabled";
                        requestVerifyPicButton.innerText = countDown + " S";
                        countDown--;
                    }
                };
                let click = setInterval(setTime, 1000);
            }))
        };
        verifyPic.src = window.URL.createObjectURL(blob);
    })
};
requestVerifyPicButton.addEventListener("click", requestVerifyCodeHandler);