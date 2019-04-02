//未完成
/***
 * URLServer: 106.13.106.1
 * 请求邮箱验证码：
 * GET//i/email_verify_code?email=?
 * response
 * {"id","wait"}
 * @type {HTMLElement}
 */
let registerForm = document.getElementById("findBackPassword");
let submit = document.getElementById("submit");
let requestVerifyPicButton = document.getElementById("request_verify_img_button");
let verifyCode = {};
/***
 * 获取服务器URL
 * @returns {function(): string}
 * @constructor
 */
let ServerURL = ()=>{
    let __URL = "http://106.13.106.1";
    return ()=>{
        return __URL;
    }
};
const URL_INTERFACE = {
    REQUEST_FOR_EMAIL_VERIFY_CODE: "\\i\\email_verify_code",
    REQUEST_FOR_CHANGE_ORIDINARY_PASSWORD: "\\account\\i\\foget_passwd"
};
const RegExpPattern = {
    EMAIL_PATTERN: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
    CHINESE_PATTERN: /^[\u4e00-\u9fa5]*$/,
    PASSWORD_PATTERN: /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[_])[\da-zA-Z_]{6,16}$/
};
const ERROR_MESSAGE = {
    IS_EMPTY: "不能为空",
    CHINESE_PATTERN_ERROR: "内容包含中文",
    NOT_SAME_PASSWORD: "密码不相同",
    PASSWORD_PATTERN: "请使用数字+字母+特殊字符",
    CONFIRM_PASSWORD: "两次输入的密码不相同",
    EMAIL_PATTERN: "邮箱格式不正确"
};
const typesReflect = {
    'password': RegExpPattern.PASSWORD_PATTERN,
    'email': RegExpPattern.EMAIL_PATTERN,
};
const errorMessageReflect = {
    'password': ERROR_MESSAGE.PASSWORD_PATTERN,
    'confirm_password': ERROR_MESSAGE.NOT_SAME_PASSWORD,
    'email': ERROR_MESSAGE.EMAIL_PATTERN
};
/***
 * 标识input状态
 */
let InputStatus = {
    email: "0",
    password: "0",
    confirm_password: "0",
    verify_code: "0",
    setStatus: function (name, value) {
        this[name] = String(value);
    },
    getStatus: function () {
        let flag = true;
        let status = Object.getOwnPropertyNames(this);
        console.log(status);
        for(let i in status){
            console.log(this[status[i]]);
            if(this[status[i]] === "0"){
                flag = false;
                break;
            }
        }
        return flag;
    }
};
/**
 * 策略组
 * */
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
 * input输入表单
 * 事件绑定
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
/***
 * 请求邮箱验证码handler
 */
function getEmailVerifyCode() {
    let email = document.getElementById("email");
    let result = Validator.validate(email);
    if(result === false || result === ERROR_MESSAGE.IS_EMPTY){
        alert(new Error("邮箱为空或格式错误"));
        return null;
    }else {
        let successHandler = (json) => {
            verifyCode = json;
            console.log(verifyCode);
            return new Promise(() => {
                let countDown = Number(verifyCode.wait);
                let setTime = () => {
                    if (countDown === 0) {
                        requestVerifyPicButton.innerText = "获取验证码";
                        clearInterval(click);
                        requestVerifyPicButton.removeAttribute("disabled");
                    } else {
                        requestVerifyPicButton.disabled = "disabled";
                        requestVerifyPicButton.innerText = countDown + " S";
                        countDown--;
                    }
                };
                let click = setInterval(setTime, 1000);
            })
        };
        let failHandler = (error) => {
            alert(error.message);
        };
        getRequest((ServerURL())() + URL_INTERFACE.REQUEST_FOR_EMAIL_VERIFY_CODE + "?" + "email=" + email.value, "application/x-www-form-urlencoded", "json", "GET")
            .then((json) => {
                return successHandler(json);
            }, (error) => {
                failHandler(error);
            });
    }
}
requestVerifyPicButton.addEventListener("click", getEmailVerifyCode);
/**
 * 序列化表单
 * */
function getFormJsonName(valueType){
    let types = {
        'password': ()=>{return "new_password"},
        'verify_code': ()=>{return "verify_code"},
    };
    return ((types[valueType])());
}
function getFormJsonObject() {
    let inputArray = registerForm.getElementsByTagName("input");
    let formObj = {};
    for(let i in inputArray){
        let input = inputArray[i];
        let name = input.name;
        if(name && name !== "item" && name !== "namedItem" && name !== "email" && name !== "confirm_password"){
            formObj[getFormJsonName(name)] = input.value;
        }
    }
    formObj["verify_id"] = verifyCode["id"];
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
 * 发送修改密码请求
 * */
let postFindBackForm = function () {
    if(!InputStatus.getStatus()){
        alert("请完成表单查询");
        return null;
    }
    let successHandler = (json)=>{
        let result = json;
        let resultTypes = {
            "0": "修改成功",
            "1": "验证码错误",
            "2": "新密码不合法",
            "3": "用户不存在",
            "4": "未知错误"
        };
        if(result["result"] === "0"){
            alert(resultTypes["0"]);
            window.location.href = "logIn.html";
        }else{
            alert(resultTypes[result["id"]]);
        }
    };
    let failHandler  = (error)=>{
        alert(error.message);
    };
    getRequest((ServerURL())() + URL_INTERFACE.REQUEST_FOR_CHANGE_ORIDINARY_PASSWORD, "application/json", "json", "POST", formSerialize())
        .then((json) => {
            return successHandler(json);
        }, (error) => {
            failHandler(error);
        });
};
submit.onclick = postFindBackForm;
