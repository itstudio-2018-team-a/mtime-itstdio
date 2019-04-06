//cookie及后续未完成
let registerForm = document.getElementById("logInForm");
let submit = document.getElementById("submit");

/**
 * 登陆
 * 106.13.106.1/account/i/login
 * request: POST
 * {user_key:"","key_type":"","'password":""}
 * response
 * {"result": ""}
 * 0：登陆成功
 * 1：无效用户ID
 * 2：无效密码
 * 3：验证码错误
 * 4：账号被封禁
 * 5：已登陆
 * 6：未知错误
 * 8：登陆数据缺失
 * 9：json格式错误
 * */
const SERVER_URL = ()=>{
    let __URL = "http://106.13.106.1";
    return ()=>{
        return __URL;
    }
};
const URL_INTERFACE = {
    REQUEST_LOG_IN: "\\account\\i\\login",
};
const RegExpPattern = {
    EMAIL_PATTERN: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/
};
const ERROR_MESSAGE = {
    IS_EMPTY: "不能为空",
    CHINESE_PATTERN_ERROR: "内容包含中文"
};
/***
 * 标识input的状态
 */
let InputStatus = {
    username: "0",
    password: "0",
    setStatus: function (name, value) {
        this[name] = String(value);
    },
    getStatus: function () {
        let flag = true;
        let status = Object.getOwnPropertyNames(this);
        for(let i in status){
            if(this[status[i]] === "0"){
                flag = false;
                break;
            }
        }
        return flag;
    }
};
/**
 * 校验策略组
 * */
let CheckValidationStrategies = {
    isEmpty: (value)=>{
        if(value === "")
            return ERROR_MESSAGE.IS_EMPTY;
    },
    isEmail: (value)=>{
        let emailReg = new RegExp(RegExpPattern.EMAIL_PATTERN);
        return emailReg.test(value);
    },
    hasChinese: (value)=>{
        let chineseReg = new RegExp(RegExpPattern.CHINESE_PATTERN);
        if(chineseReg.test(value))
            return ERROR_MESSAGE.CHINESE_PATTERN_ERROR;
    },
    checkBaseValidate: function(value){
        let errorMessage = this.isEmpty(value);
        if(errorMessage)
            return errorMessage;
        errorMessage = this.hasChinese(value);
        if(errorMessage)
            return errorMessage;
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
        if(dom.name === "username"){
            return CheckValidationStrategies.isEmail(dom.value)
        }else{
            return CheckValidationStrategies.checkBaseValidate(dom.value)
        }
    }
};
/**
 * input输入框
 * 事件Handler
 * 绑定事件
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
        InputStatus.setStatus(target.name, 0);
        target.style.borderColor = "red";
    }else{
        InputStatus.setStatus(target.name, 1);
        target.style.borderColor = "green";
    }
}
registerForm.addEventListener("focus", inputFocusHandler, true);
registerForm.addEventListener("blur", inputBlurHandler, true);
/**
 * 序列化表单
 * */
function getFormJsonName(valueType){
    let types = {
        'username': ()=>{return "user_key"},
        'password': ()=>{return "password"}
    };
    return ((types[valueType])());
}
function getFormJsonObject() {
    let inputArray = registerForm.getElementsByTagName("input");
    let formObj = {};
    //测试
    // formObj["user_key"] = "fronttest";
    // formObj["key_type"] = "user_id";
    // formObj["password"] = "fronttest123";
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name !== "item" && name !== "namedItem"){
            if(name === "username"){
                if(Validator.validate(input)){
                    formObj["key_type"] = "email";
                }else{
                    formObj["key_type"] = "user_id";
                }
                formObj["user_key"] = input.value;
            }else{
                formObj[getFormJsonName(name)] = input.value;
            }
        }
    }
    console.log(formObj);
    return formObj;
}

/***
 * 获取form的JSON数据
 * @returns {string}
 */
function formSerialize() {
    return JSON.stringify(getFormJsonObject());
}
/**
 * 获取XMLHttpRequest
 * */
function getXMLObject(){
    let xmlHttp;
    if (window.XMLHttpRequest) {
        xmlHttp=new XMLHttpRequest();
    } else {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlHttp;
}

/***
 *
 * @param url
 * @param contentType
 * @param responseType
 * @param method
 * @param data
 * @returns {Promise<any>}
 */
function getRequest(url, contentType, responseType, method, data){
    return new Promise(function (resolve, reject) {
        console.log(data);
        let xmlHttp = getXMLObject();
        xmlHttp.onreadystatechange = function () {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    resolve(this.response);
                } else if(this.status === 404) {
                    console.log(this.response);
                    reject(this.response);
                }
            }
        };
        xmlHttp.open(method, url);
        xmlHttp.responseType = responseType;
        xmlHttp.setRequestHeader("Content-Type", contentType)
        if(method === "POST"){
            xmlHttp.send(data);
        }else{
            xmlHttp.send(null);
        }
    })
}
function postLogInForm(json) {
    let successHandler = (json)=>{
        if(json["result"] === 0){
            alert("登陆成功");
            console.log(getCookie("user_id"));
            window.location.href = "PersonalPage.html";
        }
    };
    let failHandler = (json)=>{
        let errorMessage = {
            "1": "无效用户ID",
            "2": "无效的密码",
            "3": "验证码错误",
            "4": "账号被封禁",
            "5": "已登录",
            "6": "未知错误",
            "8": "登陆数据缺失",
            "9": "json格式错误"
        };
        alert(errorMessage[String(json["result"])]);
        submit.removeAttribute("style");
        submit.removeAttribute("disabled");
    };
    getRequest((SERVER_URL())() + URL_INTERFACE.REQUEST_LOG_IN, "application/json","json", "POST", json).then((json)=>{
        successHandler(json);
    }, (json)=>{
        failHandler(json)
    });
}
/***
 * 提交处理handler
 */
function submitHandler() {
    let status = InputStatus.getStatus();
    if(Number(status) === 0){
        alert("请完成表单填写");
        return false;
    }
    submit.style.background = "grey";
    submit.disabled = "disabled";
    let formJson = formSerialize();
    console.log(formJson);
    postLogInForm(formJson);
}
submit.onclick = submitHandler;

/***
 * 全局User
 */
let user;

/***
 * CookieUtils
 * @param c_name
 */
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
 *
 * @type {HTMLElement}
 */
let username = document.getElementById("username");
let register = document.getElementsByClassName("register")[1];
window.onload = (function checkIsLogIn() {
    if(getCookie("user_id")){
        alert("您已登陆");
        console.log(user);
        window.location.href = "PersonalPage.html";
    }
});
