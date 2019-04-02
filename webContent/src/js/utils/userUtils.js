/**
 * 用于获取用户信息
 * */
let json = {};
let ServerUrl = ()=> {
    let __URL = "106.13.106.1";
    return ()=>{
        return __URL;
    }
};
/***
 * 使用单例模式封装用户信息
 * */
let createUserInfo = function (json) {
    let user = {};
    let types = ["user_id", "username", "head", "email"];
    types.forEach(item, ()=>{
        user[item] = json[item];
    });
    return user;
};
let getUserInfo = (function (json) {
    let user;
    return function () {
        return user || (user = createUserInfo.apply(this, json));
    }
})(json);
let user_1 = getUserInfo();
let user_2 = getUserInfo();
if(user_1 === user_2){

}


