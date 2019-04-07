//完成
/**
*注册规格
* 用户名：允许使用 数字+字母+下划线 长度6-16字符
* 密码：允许使用 数字+字母+特殊字符 长度6-16字符
* 昵称： 禁止使用 特殊字符、Unicode扩展区文字（如果可以实现） 长度1-20字符
* 头像：提供默认头像，个人上传大小不超过2MB，不提供裁剪功能
* */
let registerForm = document.getElementById("register");
let submit = document.getElementById("submit");
const confirm_password = "confirm_password";
const ensure_code = "ensure_code";
const ServerURL = function () {
    let __URL =  "http://106.13.106.1";  //在ajax属性内拼接
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
    USERNAME_PATTERN: /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[_])[\da-zA-Z_]{6,16}$/,
    PASSWORD_PATTERN: /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[_])[\da-zA-Z_]{6,16}$/,
    NICKNAME_PATTERN: /^((?! !@#$%^&*()).)*$/,
    EMAIL_PATTERN: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/,
    ENSURE_PATTERN: ""
};
const ERROR_MESSAGE = {   //错误信息
    IS_EMPTY: "不能为空",
    NICKNAME_PATTERN: "请使用数字+字母+下划线",
    PASSWORD_PATTERN: "请使用数字+字母+特殊字符",
    CONFIRM_PASSWORD: "两次输入的密码不相同",
    EMAIL_PATTERN: "邮箱格式不正确",
    ENSURE_CODE: "验证码不正确",
    CHINESE_PATTERN_ERROR: "内容包含中文"
};
const typesReflect = {
    'username': RegExpPattern.USERNAME_PATTERN,
    'password': RegExpPattern.PASSWORD_PATTERN,
    'nickname': RegExpPattern.NICKNAME_PATTERN,
    'email': RegExpPattern.EMAIL_PATTERN,
    'verify_code': RegExpPattern.ENSURE_PATTERN
};
const errorMessageReflect = {
    'username': ERROR_MESSAGE.NICKNAME_PATTERN,
    'password': ERROR_MESSAGE.PASSWORD_PATTERN,
    'confirm_password': ERROR_MESSAGE.NOT_SAME_PASSWORD,
    'email': ERROR_MESSAGE.EMAIL_PATTERN
};
/*
标识input状态
 */
let InputStatus = function () {
    this.username = "0";
    this.password = "0";
    this.nickname = "0";
    this.confirm_password = "0";
    this.email = "0";
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

let CheckValidationStrategies = {
    isEmpty: (value)=>{
        if(value === "")
            return ERROR_MESSAGE.IS_EMPTY;
    },
    hasChinese: (value)=>{
        let chineseReg = new RegExp(RegExpPattern.CHINESE_PATTERN);
        if(chineseReg.test(value))
            return ERROR_MESSAGE.CHINESE_PATTERN_ERROR;
    },
    checkBaseValidate: function (value) {
        let errorMessage = this.isEmpty(value);
        if(errorMessage)
            return errorMessage;
        errorMessage = this.hasChinese(value);
        if(errorMessage)
            return errorMessage;
    },
    checkIsTheSame: function (value_1, value_2) {
        console.log(value_1 + " " + value_2);
        if(value_1 !== value_2){
            return ERROR_MESSAGE.CONFIRM_PASSWORD;
        }
    },
    checkValidate: function(value, regType){    //value待判断的值，regType为正则匹配模式的类型
        let errorMessage = this.checkBaseValidate(value);
        if(errorMessage){
            return errorMessage;
        }
        console.log(typesReflect[regType]);
        let typeReg = new RegExp(typesReflect[regType]);
        console.log(typeReg.test(value));
        if(!typeReg.test(value)){
            console.log(errorMessageReflect[regType]);
            return errorMessageReflect[regType];
        }
    }
};
/**
 * 校验业务组
 * */
const Validator = {
    validate: (dom)=>{
        let message = CheckValidationStrategies.checkBaseValidate(dom.value);
        if(message){
            return message;
        }
        if(dom.name === "confirm_password"){
            let password = document.getElementById("password").value;
            console.log(CheckValidationStrategies.checkIsTheSame(password, dom.value));
            return CheckValidationStrategies.checkIsTheSame(password, dom.value);
        }else if(dom.name === "verify_code"){
            return CheckValidationStrategies.isEmpty(dom.value);
        }else{
            return CheckValidationStrategies.checkValidate(dom.value, dom.name);
        }
    }
};
/**
 * input输入框绑定
 * */
function getTarget(event){
    return event.target || event.srcElement;
}
function inputFocusHandler(event) {
    let target = getTarget(event);
    target.style.borderColor = "rgba(91,136,180,1)";
}
function inputBlurHandler(event) {
    let target = getTarget(event);
    let message =  Validator.validate(target);
    if(message){
        inputStatus.setStatus(target.name, 0);
        target.style.borderColor = "red";
        let tips = target.parentNode.childNodes;
        for(let element in tips){
            if(tips.hasOwnProperty(element)){
                if(tips[element].className === "tips"){
                    tips[element].innerText = "*" + message;
                    tips[element].style.color = "red";
                }
            }
        }
        // tips.innerText = "*" + message;
        // tips.style.color = "red";
    }else{
        inputStatus.setStatus(target.name, 1);
        target.style.borderColor = "green";
        let tips = target.parentNode.childNodes;
        for(let element in tips){
            if(tips.hasOwnProperty(element)){
                if(tips[element].className === "tips"){
                    tips[element].innerText = " ";
                    tips[element].style.color = "blue";
                }
            }
        }
        // tips.innerText = "";
    }
}
registerForm.addEventListener("focus", inputFocusHandler, true);
registerForm.addEventListener("blur", inputBlurHandler, true);
/**
 * 获取验证码
 * */
function getXMLObject() {
    let xmlHttp;
    if (window.XMLHttpRequest) {
        xmlHttp=new XMLHttpRequest();
    } else {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlHttp;
}
/***
 *  获取请求对象
 * @param url
 * @param contentType
 * @param responseType
 * @param method
 * @param data
 * @returns {Promise<any>}
 */
function getRequest(url, contentType, responseType, method, data){
    return new Promise(function (resolve, reject) {
        let xmlHttp = getXMLObject();
        xmlHttp.onreadystatechange = function () {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    resolve(this.response);
                } else {
                    reject(new Error("请求失败"));
                }
            }
        };
        xmlHttp.open(method, url);
        xmlHttp.responseType = responseType;
        xmlHttp.setRequestHeader("Content-Type", contentType);
        if(method === "POST"){
            xmlHttp.send(data);
        }else{
            xmlHttp.send(null);
        }
    })
}
/**
 * 请求图片验证码
 * */
let requestVerifyPicButton = document.getElementById("request_verify_img_button");
let verifyPic = document.getElementById("verify_img");
let verifyCode = {};
function requestVerifyCodeHandler() {
    let successHandler = (json)=>{
        verifyCode = json;
        console.log(verifyCode);
        // return getRequest((ServerURL())() + Url_Options.VERIFY_PICTURE + "\\" + verifyCode["id"], "application/x-www-form-urlencoded", "blob", "GET");
        return getRequest("http://127.0.0.1:8080/webContent/dist/cover_1.png", "application/x-www-form-urlencoded", "blob", "GET").then((blob)=>{
            verifyImgHandler(blob);
        });
    };
    let failHandler = (error)=>{
        alert(error.message);
    };
    let verifyImgHandler = (blob)=>{
        console.log(blob);
        verifyPic.onload = function () {
            window.URL.revokeObjectURL(verifyPic.src);
            return new Promise(((resolve, reject) => {
                let countDown = Number(verifyCode.wait);
                let setTime = ()=>{
                    if(countDown === 0){
                        requestVerifyPicButton.innerText = "获取验证码";
                        clearInterval(click);
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
    };
    //getRequest((ServerURL())() + Url_Options.VERIFY_CODE, "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
    //getRequest((ServerURL())() + Url_Options.VERIFY_CODE, "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
    getRequest("demo.json", "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    })
}
const throttle = (func, wait)=>{
    let timer;
    return ()=>{
        if(timer){
            return;
        }
        timer = setTimeout(()=>{
            func();
        }, wait, ()=>{
            clearTimeout(timer);
        });
    };
};
requestVerifyPicButton.onclick = throttle(requestVerifyCodeHandler, 1000);
/**
 *  表单序列化
 * */
function getFormJsonName(valueType){
    let types = {
        'password': ()=>{return "password"},
        'verify_code': ()=>{return "verify_code"},
        "username": ()=>{return "user_id"},
        "nickname": ()=>{return "user_name"},
        "email": ()=>{return "email"}
    };
    return ((types[valueType])());
}
function getFormJsonObject() {
    let inputArray = registerForm.getElementsByTagName("input");
    let formObj = {};
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name !== "item" && name !== "namedItem" && name !== "confirm_password"){
            formObj[getFormJsonName(name)] = input.value;
        }
    }
    // formObj["verify_id"] = verifyCode["id"];
    formObj["verify_id"] = "1";
    console.log(formObj);
    return formObj;
}
/**
 * 获取表单JSON
 * */
function formSerialize() {
    return JSON.stringify(getFormJsonObject());
}
/**
 * 发送注册的请求
 * */
let postRegisterForm = function () {
    let json = formSerialize();
    console.log(json);
    if(json.hasOwnProperty("verify_id")){
        alert("未请求验证码");
        return null;
    }
    if(!inputStatus.getStatus()){
        alert("请完成表单查询");
        return null;
    }
    let successHandler = (json)=>{
        let result = json;
        let resultTypes = {
            "0": "注册成功",
            "1": "用户ID重复",
            "2": "电子邮件已被注册",
            "3": "验证码错误",
            "4": "无效的昵称",
            "5": "无效的密码",
            "6": "未知错误",
            "7": "无效的用户ID",
            "8": "注册数据不完整",
            "9": "josn格式错误"
        };
        if(String(result["result"]) === "0"){
            alert(resultTypes["0"]);
            window.location.href = "logIn.html";
        }else{
            alert(resultTypes[String(result["id"])]);
        }
    };
    let failHandler = (error)=>{
        alert(error.message);
    };
    getRequest((ServerURL())() + Url_Options.REGISTER, "application/json", "json", "POST", json).then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    })
};
submit.onclick = postRegisterForm;