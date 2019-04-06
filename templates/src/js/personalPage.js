/////////////////
/***
 * 全局User
 */
let user;
/***
 * CookieUtils
 * @param name
 * @param value
 * @param expireDays
 */
function setCookie(name, value, expireDays) {
    let exdate = new Date();
    exdate.setDate(exdate.getDate() + expireDays);
    document.cookie = name + "=" + (value) + ((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
}
function getCookie(c_name) {
    if (document.cookie.length>0)
    {
        let c_start=document.cookie.indexOf(c_name + "=");
        if (c_start!==-1)
        {
            c_start=c_start + c_name.length+1;
            let c_end=document.cookie.indexOf(";",c_start);
            if (c_end===-1) c_end=document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}
/***
 * 处理个人信息
 */
let createUser = function () {
    let user = {};
    let types = ["user_id","username", "head","email"];
    types.forEach(item, (item)=>{
        user[item] = json[item];
    });
    //测试用
    user = {"user_id": "1", "username": "newive", "head": "#","email": "738767136@qq.com"};
    types.forEach(item, ()=>{
        user[item] = json[item];
    });
    return user;
};
let getUserInfo = function (json) {
    let user;
    return function () {
        return user || (user = createUser.apply(this, json));
    }
};
/***
 * 取得请求用户信息的接口
 * @returns {function(): string}
 * @constructor
 */
const UserServerURL = function () {
    let __URL =  "http://106.13.106.1\\account\\i\\user\\info";  //在ajax属性内拼接
    // let __URL = "ellipse.png";
    return ()=>{
        return __URL;
    }
};
/***
 *
 * @type {HTMLElement}
 */
let username = document.getElementById("username");
let userPortrait = document.getElementById("user_portrait");
let pre_username = document.getElementById("input_username");

window.onload = (function checkIsLogIn() {
    if(!getCookie("user_id")){
        alert("请登录");
        window.location.href = "logIn.html";
    }else{
        let user_name = getCookie("user_name");
        let user_id = getCookie("user_id");
        getRequest(UserServerURL() + "\\" + user_id, "json", "application/x-www-form-urlencoded", "GET").then(
            (json)=>{
                if(json["status"] === "unknow_user"){
                    alert("找不到用户");
                }else if(json["status"] === "ok") {
                    user = getUserInfo(json);
                    console.log(user);
                }else{
                    alert("未知错误");
                }
            },
            (error)=>{
                alert(error.message);
            }
        )
    }
    user = (getUserInfo())();
    console.log(user);
    username.innerText = user["username"];
    pre_username.value = user["username"];
    userPortrait = user["head"];
});
////////////////

let changeNickname = document.getElementById("change_nickname");
let nicknameSubmit = document.getElementById("nickname_submit");
let changePassword = document.getElementById("change_password");
let passwordSubmit = document.getElementById("password_submit");
/***
 * 获取服务器URL
 * @returns {function(): string}
 * @constructor
 */
const ServerURL = function () {
    let __URL =  "http://106.13.106.1";  //在ajax属性内拼接
    return ()=>{
        return __URL;
    }
};
/***
 * @type {{REGISTER: string, VERIFY_PICTURE: string, VERIFY_CODE: string}}
 */
const Url_Options = {
    UPLOAD_PORTRAIT: "\\account\\i\\upload_head",
    CHANGE_NICKNAME: "\\account\\i\\change_nick",
    CHANGE_PASSWORD: "\\account\\i\\changepasswd"
};
/***
 * 正则匹配模式
 * @type {{PASSWORD_PATTERN: RegExp, CHINESE_PATTERN: RegExp, NICKNAME_PATTERN: RegExp}}
 */
const RegExpPattern = {
    PASSWORD_PATTERN: /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[_])[\da-zA-Z_]{6,16}$/,
    NICKNAME_PATTERN: /^((?! !@#$%^&*()).)*$/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/,
};
/***
 * 错误信息
 * @type {{PASSWORD_PATTERN: string, CONFIRM_PASSWORD: string, CHINESE_PATTERN_ERROR: string, EMAIL_PATTERN: string, ENSURE_CODE: string, IS_EMPTY: string, NICKNAME_PATTERN: string}}
 */
const ERROR_MESSAGE = {
    IS_EMPTY: "不能为空",
    NICKNAME_PATTERN: "请使用数字+字母+下划线",
    PASSWORD_PATTERN: "请使用数字+字母+特殊字符",
    CONFIRM_PASSWORD: "两次输入的密码相同",
    CHINESE_PATTERN_ERROR: "内容包含中文"
};
/***
 * 输入框name与匹配模式的映射
 * @type {{password: RegExp, nickname: RegExp, verify_code: string, email: RegExp, username: RegExp}}
 */
const typesReflect = {
    'password': RegExpPattern.PASSWORD_PATTERN,
    'nickname': RegExpPattern.NICKNAME_PATTERN,
};
/***
 * 输入框的name与错误信息的映射
 * @type {{password: string, email: string, username: string, confirm_password: string}}
 */
const errorMessageReflect = {
    'nickname': ERROR_MESSAGE.NICKNAME_PATTERN,
    'password': ERROR_MESSAGE.PASSWORD_PATTERN,
    'confirm_password': ERROR_MESSAGE.NOT_SAME_PASSWORD,
};
/***
 * 标识input状态
 * @constructor
 */
let InputStatus = function () {
    this.password = "0";
    this.nickname = "1";
    this.confirm_password = "0";
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
InputStatus.prototype.getGroupStatus = function(array){
    let flag = true;
    for(let i = 0; i < array.length; i++){
        let element = this[array[i]];
        console.log(element);
        if(element === "0"){
            flag = false;
            return flag;
        }
    }
    return flag;
};
let inputStatus = new InputStatus();
/***
 * 校验策略组
 * @type {{isEmpty: CheckValidationStrategies.isEmpty, checkIsTheSame: CheckValidationStrategies.checkIsTheSame, checkValidate: CheckValidationStrategies.checkValidate, hasChinese: CheckValidationStrategies.hasChinese, checkBaseValidate: CheckValidationStrategies.checkBaseValidate}}
 */
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
        if(value_1 === value_2){
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
        }else if(dom.name === "nickname"){
            let preUserName = user["username"];
            if(dom.value === preUserName){
                return "与原用户名相同";
            }
            return CheckValidationStrategies.checkValidate(dom.value, dom.name);

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
    } else{
        inputStatus.setStatus(target.name, 1);
        target.style.borderColor = "green";
    }
}
changeNickname.addEventListener("focus", inputFocusHandler, true);
changeNickname.addEventListener("blur", inputBlurHandler, true);
changePassword.addEventListener("focus", inputFocusHandler, true);
changePassword.addEventListener("blur", inputBlurHandler, true);
/**
 *  表单序列化
 * */
function getFormJsonName(valueType){
    let types = {
        'password': ()=>{return "password"},
        "nickname": ()=>{return "username"},
    };
    return ((types[valueType])());
}
function getFormJsonObject(form) {
    let inputArray = form.getElementsByTagName("input");
    let formObj = {};
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name !== "item" && name !== "namedItem" && name !== "confirm_password"){
            formObj[getFormJsonName(name)] = input.value;
        }
    }
    console.log(formObj);
    return formObj;
}
/**
 * 获取表单JSON
 * */
function formSerialize(form) {
    return JSON.stringify(getFormJsonObject(form));
}
/**
 *
 * @param url
 * @param type
 * @param contentType
 * @param requestMethod
 * @param data
 * @returns {Promise<any>}
 */
function getRequest(url, type, contentType, requestMethod, data) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = getXMLObject();
        xmlHttp.onreadystatechange = function () {
            console.log(this.status);
            console.log(this.readyState);
            if(this.readyState === 4){
                if(this.status === 200){
                    resolve(this.response);
                }else{
                    reject(new Error("请求错误"));
                }
            }
        };
        xmlHttp.open(requestMethod, url);
        xmlHttp.responseType = type;
        xmlHttp.setRequestHeader("Content-Type", contentType + ";charset=utf-8");
        if(requestMethod === "POST"){
            xmlHttp.send(data);
        }else if(requestMethod === "GET"){
            xmlHttp.send(null);
        }
    });
}
/**
 * 获取XML对象
 * */
function getXMLObject() {
    let xmlHttp;
    if(window.XMLHttpRequest){
        xmlHttp = new XMLHttpRequest();
    }else{
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlHttp;
}
/***
 * 请求修改用户昵称
 * request:{"new_nick}
 * response: {"result"}
 */
function requestChangeNickname() {
    let currentNickname = document.getElementById("input_username");
    if(currentNickname.value === user["username"]){
        alert("未作修改");
        return null;
    }
    let nicknameJson = formSerialize(changeNickname);
    let successHandler = (json)=> {
        /*
            接口待完善
         */
        alert(json["result"]);
        /*
        修改input
        */
    };
    let failHandler = (error)=>{
        alert(error.message);
    };
    getRequest((ServerURL())() + Url_Options.CHANGE_NICKNAME, "json", "application/json", "POST", nicknameJson).then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    })
}
function nicknameSubmitHandler(){
    let flag = inputStatus.getGroupStatus(["nickname"]);
    if(flag === true){
        requestChangeNickname();
    }else{
        alert("表单填写有误");
    }
}
nicknameSubmit.onclick = nicknameSubmitHandler;
/***
 * 请求修改用户密码
 * request:{"new_nick}
 * response: {"result"}
 */
function requestChangePassword() {
    let passwordJson = formSerialize(changePassword);
    let successHandler = (json)=> {
        let result = {
            "0": "成功",
            "1": "原密码错误",
            "2": "验证码错误",
            "3": "未登录",
            "4": "未知错误"
        };
        alert(result[String(json["result"])]);
    };
    let failHandler = (error)=>{
        alert(error.message);
    };
    getRequest((ServerURL())() + Url_Options.CHANGE_PASSWORD + "\\" + "Frontend_test02", "json", "application/json", "POST", passwordJson).then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    })
}
function passwordSubmitHandler(){
    let flag = inputStatus.getGroupStatus(["password","confirm_password"]);
    if(flag === true){
        requestChangePassword();
    }else{
        alert("表单填写有误");
    }
}
passwordSubmit.onclick = passwordSubmitHandler;
/***
 * 头像上传
 */
let portraitSelect = document.getElementById("select_portrait");    //选取img
let displayPortrait = document.getElementById("display_portrait");   //img
let portraitSubmit = document.getElementById("confirm_portrait");   //上传头像
let uploadImgHandler = ()=>{
    console.log(portraitSelect.files[0].name);
    if(!portraitSelect.files.length || portraitSelect.files.length === 0){
        alert("您的头像未更改");
        return null;
    }else{
        let file = portraitSelect.files[0];
        let name = file.name;
        console.log(file);
        getRequest((ServerURL())() + Url_Options.UPLOAD_PORTRAIT + "\\" + name, "json", "application/", "POST", file).then((json)=>{
            console.log(json["result"]);
            if(json["result"] !== "成功"){
                console.log("error");
            }
        }, (error)=>{
            alert(error.message);
        });
    }
};
function portraitImgChangeHandler() {
    window.URL = window.URL || window.webkitURL;
    let displayPortrait = document.getElementById("display_portrait");   //img
    if(this.files.length === 0){
        return null;
    }

    console.log(this.files[0].name);
    let file =  this.files[0];
    if((file.size / 1024) > 1000){
        alert("头像不能超过1M");
        return null;
    }
    displayPortrait.src = window.URL.createObjectURL(this.files[0]);
    displayPortrait.onload = function () {
        window.URL.revokeObjectURL(this.src);
    }
}
portraitSelect.addEventListener("change", portraitImgChangeHandler);
portraitSubmit.onclick = uploadImgHandler;