let createUser = function (json) {
    let user = {};
    let types = ["user_id","username", "head","email"];
    types.forEach(item, (item)=>{
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
 * 全局User
 */
let user;
const UserServerURL = function () {
    let __URL =  "http://106.13.106.1/account/i/user/info";  //在ajax属性内拼接
    return ()=>{
        return __URL;
    }
};
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
 * 获取请求
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
            xmlHttp.send(null);
        }
    });
}
(function checkIsLogIn() {
    if(!getCookie("user_id")){
        alert("请登录");
        window.location.href = "logIn.html";
    }else{
        let user_id = getCookie("user_id");
        getRequest((UserServerURL())() + "/" + user_id, "application/x-www-form-urlencoded", "json", "GET").then(
            (json)=>{
                if(json["status"] === "unknow_user"){
                    alert("找不到用户");
                }else if(json["status"] === "ok") {
                    user = getUserInfo(json);
                }else{
                    alert("未知错误");
                }
            },
            (error)=>{
                alert(error.message);
            }
        )
    }
})();