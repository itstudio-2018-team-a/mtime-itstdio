
let registerForm = document.getElementById("register");
let submit = document.getElementById("submit");
let requestVerifyPicButton = document.getElementById("request_verify_img_button");
let verifyImg = document.getElementById("verify_img");
let verifyCode = {};

/*
常量
 */
const Url_Options = {
    VERIFY_CODE: "\\i\\verify_code",
    VERIFY_PICTURE: "\\i\\verify_code_picture",
    LOGIN: "\\account\\i\\login"
};
const RegExpPattern = {
    EMAIL_PATTERN: /^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/,
};
const ErrorMessage = {
    IS_EMPTY: "不能为空",
    CHINESE_PATTERN_ERROR: "内容包含中文"
};

/*
Utils
 */
const ServerURL = ()=>{ //获取服务器地址
    let __URL = "106.13.106.1";
    return ()=>{
        return __URL;
    }
};
function getPatternType(valueType) {//获取匹配模式
    let types = {
        'username': ()=>{return RegExpPattern.EMAIL_PATTERN}
    };
    return ((types[valueType])());
}
function getXMLObject() {
    let xmlHttp;
    if(window.XMLHttpRequest){
        xmlHttp = new XMLHttpRequest();
    }else{
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlHttp;
}
/*
操作cookie
 */
let cookieUtils = {
    get: function (name) {
        var cookieName = encodeURIComponent(name) + "=";
        //只取得最匹配的name，value
        var cookieStart = document.cookie.indexOf(cookieName);
        var cookieValue = null;

        if (cookieStart > -1) {
            // 从cookieStart算起
            var cookieEnd = document.cookie.indexOf(';', cookieStart);
            //从=后面开始
            if (cookieEnd > -1) {
                cookieValue = decodeURIComponent(document.cookie.substring(cookieStart + cookieName.length, cookieEnd));
            } else {
                cookieValue = decodeURIComponent(document.cookie.substring(cookieStart + cookieName.length, document.cookie.length));
            }
        }

        return cookieValue;
    },

    set: function (name, val, options) {
        if (!name) {
            throw new Error("coolie must have name");
        }
        var enc = encodeURIComponent;
        var parts = [];

        val = (val !== null && val !== undefined) ? val.toString() : "";
        options = options || {};
        parts.push(enc(name) + "=" + enc(val));
        // domain中必须包含两个点号
        if (options.domain) {
            parts.push("domain=" + options.domain);
        }
        if (options.path) {
            parts.push("path=" + options.path);
        }
        // 如果不设置expires和max-age浏览器会在页面关闭时清空cookie
        if (options.expires) {
            parts.push("expires=" + options.expires.toGMTString());
        }
        if (options.maxAge && typeof options.maxAge === "number") {
            parts.push("max-age=" + options.maxAge);
        }
        if (options.httpOnly) {
            parts.push("HTTPOnly");
        }
        if (options.secure) {
            parts.push("secure");
        }

        document.cookie = parts.join(";");
    },
    delete: function (name, options) {
        options.expires = new Date(0);// 设置为过去日期
        this.set(name, null, options);
    }
};

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
                    reject();
                }
            }
        };
        xmlHttp.open(requestMethod, url);
        xmlHttp.responseType = type;
        xmlHttp.setRequestHeader("Content-Type", contentType + ";charset=utf-8");
        if(requestMethod === "POST"){
            xmlHttp.send(data);
        }else if(requestMethod === "GET"){
            xmlHttp.send();
        }
    });
}

/*
保存输入框状态
 */
let InputStatus = function () {
    this.username = "0";
    this.password = "0";
    this.ensure_code = "0";
};
InputStatus.prototype.setStatus = function (name, value) {
    this[name] = value;
};
InputStatus.prototype.getStatus = function () {
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
    isEmpty: (value)=>{
        if(value === "") {
            return ErrorMessage.IS_EMPTY;
        }
    },
    hasChinese: (value)=>{
        if(new RegExp(RegExpPattern.CHINESE_PATTERN).test(value)){
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
    isEmail: (value)=>{
        let typeReg = new RegExp(RegExpPattern[RegExpPattern.EMAIL_PATTERN]);
        if(!typeReg.test(value)){
            return false;
        }
    }
};
/*
校验业务组
 */
let Validator = function () {};
Validator.prototype.validateBase = function (dom) {
    return CheckValidationStrategies.checkBaseValidate(dom.value);
};
Validator.prototype.checkIsEmail = function (dom) {
    return CheckValidationStrategies.isEmail(dom.value);
};
/*
获取验证码
 */
let requestVerifyCodeHandler = function () {
    let successHandler = (json)=>{
        verifyCode = json;
        console.log(verifyCode);
        return getRequest((ServerURL())() + Url_Options.VERIFY_PICTURE + "\\" + verifyCode.id);
    };
    let failHandler = ()=>{
        alert("请求超时");
    };
    getRequest((ServerURL())() + Url_Options.VERIFY_CODE, "json", "application/json", "GET").then((json)=>{
        return successHandler(json);
    },()=>{
        failHandler();
    }).then((blob)=>{
        verifyImg.onload = function () {
            window.URL.revokeObjectURL(verifyImg.src);
            return new Promise(((resolve, reject) => {
                let countDown = Number(verifyCode.wait);
                let setTime = ()=>{
                    if(countDown === 0){
                        requestVerifyPicButton.innerText = "获取验证码";
                        clearInterval(click);
                        requestVerifyPicButton.removeAttribute("disabled");
                    }else{
                        requestVerifyPicButton.disabled = "disabled";
                        requestVerifyPicButton.innerText = count + "S";
                        countDown--;
                    }
                };
                let click = setInterval(setTime, 1000);
            }));
        };
        verifyImg.src = window.URL.createObjectURL(blob);
    })
};
/*
* 表单序列化
* */
function getFormJsonName(valueType) {
    let types = {
        'username': ()=>{ return "user_id"},
        'password': ()=>{ return "password"},
        'email': ()=> {return "email"},
        'ensure_code': ()=>{return "verify_code"}
    };
    return ((types[valueType])());
}
function getFormJsonObject() {
    let inputArray = registerForm.getElementsByTagName("input");
    let formObj = {};
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name!=="confirm_password" && name !== "item" && name !== "nameItem"){
            if(name === "username"){
                let validator = new Validator();
                if(validator.checkIsEmail(input)){
                    formObj["email"] = input.value;
                }else{
                    formObj[getFormJsonName(name)] = input.value;
                }
            }else{
                formObj[getFormJsonName(name)] = input.value;
            }
        }
    }
    return formObj;
}
let formSerialize = function () {
    let obj = getFormJsonObject();
    if(verifyCode){
        obj["verify_id"] = verifyCode.id;
    }
    return JSON.stringify(getFormJsonObject());
};

/*
事件处理
 */
function getEventTarget(event) {
    return event.target || target.srcElement;
}
function inputFocusHandler(event) {
    let target = getEventTarget(event);
    target.style.borderColor = "rgba(91,136,180,1)";
}
function inputBlurHandler(event) {
    let target = getEventTarget(event);
    let message = validator.validate(target);
    if(message){
        inputStatus.setStatus(target.name, 0);
        target.style.borderColor = "red";
        /*
        是否加提示项待定
         */
    }else{
        inputStatus.setStatus(target.name, 1);
        /*
        是否加提示项待定
         */
    }
}

/*
提交
 */
function submitHandler() {
    let status = inputStatus.getStatus();
    if(Number(status) === 0){
        alert("请完成登陆信息填写");
        return false;
    }
    submit.style.background = "grey";
    submit.disabled = "disabled";
    let formJson = formSerialize();
    getRequest((ServerURL())() + Url_Options.LOGIN, "json", "application/json", "post", formJson).then(json=>{
        let types = {
            "0": ()=>{alert("登陆成功！")},
            "1": ()=>{alert("无效的用户名")},
            "2": ()=>{alert("无效的密码")},
            "3": ()=>{alert("验证码错误")},
            "4": ()=>{alert("账号被封禁")},
            "5": ()=>{alert("已登录")},
            "6": ()=>{alert("未知错误")}
        };
        let result = json["result"];
        (types[result])();
        if(result === "0"){
            /*
            * cookie待处理
            * */
            window.location.href = "index.html";
        }else{
            submit.removeAttribute("style");
            submit.removeAttribute("disabled");
        }
    });
}
requestVerifyPicButton.addEventListener("click", requestVerifyCodeHandler);
registerForm.addEventListener("focus", inputFocusHandler, true);
registerForm.addEventListener("blur", inputBlurHandler, true);
submit.onclick = submitHandler;