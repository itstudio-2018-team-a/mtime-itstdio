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
    // types.forEach(item, (item)=>{
    //     user[item] = json[item];
    // });
    //测试用
    user = {"user_id": "1", "username": "newive", "head": "#","email": "738767136@qq.com"};
    // types.forEach(item, ()=>{
    //     user[item] = json[item];
    // });
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
    // let __URL =  "http://106.13.106.1/account/i/user/info";  //在ajax属性内拼接
    let __URL = "ellipse.png";
    return ()=>{
        return __URL;
    }
};
/***
 *
 * @type {HTMLElement}
 */
let username = document.getElementById("username");
let pre_username = document.getElementById("input_username");

window.onload = (function checkIsLogIn() {
    // if(!getCookie("user_id")){
    //     alert("请登录");
    //     window.location.href = "logIn.html";
    // }else{
    //     let user_id = getCookie("user_id");
    //     getRequest(UserServerURL(), "json", "application/x-www-form-urlencoded", "GET").then(
    //         (json)=>{
    //             if(json["status"] === "unknow_user"){
    //                 alert("找不到用户");
    //             }else if(json["status"] === "ok") {
    //                 user = getUserInfo(json);
    //                 console.log(user);
    //             }else{
    //                 alert("未知错误");
    //             }
    //         },
    //         (error)=>{
    //             alert(error.message);
    //         }
    //     )
    // }
    user = (getUserInfo())();
    console.log(user);
    username.innerText = user["username"];
    pre_username.value = user["username"];
});
////////////////

let confirmPortrait = document.getElementById("select");
let portraitForm = document.getElementById("portrait");
let displayImg = document.getElementById("display_img");
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
    CONFIRM_PASSWORD: "两次输入的密码不相同",
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
    }else{
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
    formObj["verify_id"] = verifyCode["id"];
    // formObj["verify_id"] = "1";
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
nicknameSubmit.onclick = requestChangeNickname;
/***
 * 请求修改用户密码
 * request:{"new_nick}
 * response: {"result"}
 */
function requestChangeNickname() {
    let passwordJson = formSerialize(changePassword);
    let successHandler = (json)=> {
        /*

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



