/**
 *  获取服务器URL
 * */
const ServerURL = function () {
    let __URL =  "http://39.96.208.176";  //在ajax属性内拼接
    return ()=>{
        return __URL;
    }
};
/**
 * 接口
 * */
const Url_Options = {
    USER_INFORMATION: "account\\i\\user\\info",
    SEARCH: "\\i\\search",
    HOT_POT:"\\news\\i\\hotpot_list",
    FILM_LIST: "\\film\\i\\film_list",
    HOT_REVIEW_LIST: "\\film\\i\\hot_review_list"
};

/***
 * 限制字数
 * @param content
 * @param number
 * @returns {*}
 */
function limitWords(content, number) {
    if(content.length >= number){
        content = content.substr(0, number) + "...";
    }
    return content;
}
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
 * 获取dom对象
 * */
//正在热映
let hotMovieList = document.getElementById("hot_videos").getElementsByClassName("movie");
/**
 * 图片预加载
 * */
function preImgHandler(dom){
    dom.src = "../templates/marvel_captain_1.png";
}
/**
 * 预设值电影信息
 * */
/***
 * "total_num": "总数",
 "num":"数量(int)",
 "list":[{
    "title":"电影标题",
    "image":"缩略图",
    "info":"简介",
    "time":"YYYY-MM-DD hh:mm:ss",
    "film_id":"电影ID"
    }],
 "status": "ok"
 * @param dom
 * @param value
 */
function setDisplayingDefaultInfo(dom, value) {
    let setDefaultInfo = (domClass)=>{
        let types = ["movie_name", "movie_time", "movie_description"];
        for(let element in types){
            if(types.hasOwnProperty(element)){
                domClass.getElementsByClassName(types[element])[0].innerText = value;
            }
        }
    };
    let spanArray = dom.getElementsByTagName("ul")[0];
    setDefaultInfo(spanArray);
}
/**
 * 预设值电影封面
 * */
function setDisplayingDefaultCover(dom, value) {
    let coverElement = dom.getElementsByTagName("img")[0];
    coverElement.src = value;
}

/***
 * 请求正在热映电影信息
 */
function requestForFilmList(){
    let typeReflect = {
        "movie_name": "title",
        "movie_time": "time",
        "movie_description": "info"
    };
    /***
     * 设置电影信息
     */
    let successHandler = function (json) {
        if (json["status"] === "ok") {
            let filmList = json["list"];
            let types = ["movie_name", "movie_time", "movie_description"];
            for (let i = 0; i < hotMovieList.length; i++) {
                for (let element in types) {
                    if (types.hasOwnProperty(element)) {
                        if (types[element] === "movie_description") {
                            hotMovieList[i].getElementsByClassName(types[element])[0].innerText = limitWords((filmList[i])[typeReflect[types[element]]], 100);
                        } else if (types[element] === "movie_time") {
                            hotMovieList[i].getElementsByClassName(types[element])[0].innerText = (filmList[i])[typeReflect[types[element]]].split("-")[0];
                        } else {
                            hotMovieList[i].getElementsByClassName(types[element])[0].innerText = (filmList[i])[typeReflect[types[element]]];
                        }
                    }
                }
                hotMovieList[i].getElementsByTagName("img")[0].src = (ServerURL())() + (filmList[i])["image"];
                hotMovieList[i].getElementsByClassName("purchase_button")[0].addEventListener("click", (() => {
                    return () => {
                        window.location.href = "http://www.baidu.com?film_id=" + filmList[i]["film_id"];
                    }
                })(), true);
            }
        }else {
            console.log(json["status"]);
        }
    };
    /***
     *
     */
    let failHandler = function (error) {
        alert(error.message);
    };
    for(let element in hotMovieList){
        if(hotMovieList.hasOwnProperty(element)){
            getRequest((ServerURL())() + Url_Options.FILM_LIST + "\\num=4", "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
                successHandler(json);
            }, (error)=>{
                failHandler(error);
            })
        }
    }
}
/**
 * 预设置正在热映
 * */
(function setDisplayingImg(){
    for(let element in hotMovieList){
        if(hotMovieList.hasOwnProperty(element)){
            setDisplayingDefaultCover(hotMovieList[element], "../templates/marvel_captain_1.png");
            setDisplayingDefaultInfo(hotMovieList[element], "null");
        }
    }
    requestForFilmList();
})();
/***
 * 请求即将上映的电影
 */
let display_movies = document.getElementById("display_movies").getElementsByClassName("movie");
/**
 * 预设即将上映的电影的海报
 * */
function setDefaultDisplayMoviesInfo(dom, value){
    let setDefaultInfo = (domClass)=>{
        let types = ["time", "title", "hot_degree", "movie_content"];
        for(let element in types){
            if(types.hasOwnProperty(element)){
                domClass.getElementsByClassName(types[element])[0].getElementsByTagName("span")[0].innerText = value;
            }
        }
    };
    setDefaultInfo(dom);
}

/**
 * 请求即将上映的电影
 * */
function requestDisplayingFilmList(){
    let typeReflect = {
        "title": "title",
        "time": "time",
        "movie_content": "info"
    };
    let successHandler = function (json) {
        if(json["status"] === "ok"){
            let filmList = json["list"];
            let types = ["time", "title", "hot_degree", "movie_content"];
            for (let i = 0; i < display_movies.length; i++) {
                for (let element in types) {
                    if (types.hasOwnProperty(element)) {
                        if (types[element] === "movie_content") {
                            display_movies[i].getElementsByClassName(types[element])[0].innerText = limitWords((filmList[i])[typeReflect[types[element]]], 30);
                        } else if (types[element] === "time") {
                            let wholeTime = (filmList[i])[typeReflect[types[element]]];
                            display_movies[i].getElementsByClassName(types[element])[0].innerText = wholeTime.split("-")[1] + "月" + wholeTime.split("-")[2].split(" ")[0] + "日";
                        } else {
                            display_movies[i].getElementsByClassName(types[element])[0].innerText = (filmList[i])[typeReflect[types[element]]];
                        }
                    }
                }
                display_movies[i].getElementsByTagName("img")[0].src = (ServerURL())() + (filmList[i])["image"];
                display_movies[i].getElementsByClassName("purchase_early_button")[0].addEventListener("click", (() => {
                    return () => {
                        window.location.href = "http://www.baidu.com?film_id=" + filmList[i]["film_id"];
                    }
                })(), true);
            }
        }else{
            console.log(json["status"]);
        }
    };
    let failHandler = function (error) {
        console.log(error.message);
    };
    for(let element in display_movies){
        if(hotMovieList.hasOwnProperty(element)){
            getRequest((ServerURL())() + Url_Options.FILM_LIST + "\\num=4", "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
                successHandler(json);
            }, (error)=>{
                failHandler(error);
            })
        }
    }
}
(function setDisplayMovies(){
    for(let element in display_movies){
        if(display_movies.hasOwnProperty(element)){
            setDisplayingDefaultCover(display_movies[element], "../templates/cover_3.png");
            setDefaultDisplayMoviesInfo(display_movies[element], "null");
        }
    }
    requestDisplayingFilmList();
})();

/***
 * 获取dom
 */
let newsList = document.getElementById("news_today").getElementsByClassName("news");
/**
 * 请求今日热点
 * */
function requestHotPot(){

    let successHandler = function (json) {
        if(json["status"] === "ok"){
            let list = json["list"];
            for (let i = 0; i < newsList.length; i++) {
                let element = newsList[i];
                element.getElementsByClassName("news_info")[0].getElementsByTagName("span")[0].innerText = list[i]["title"];
                element.getElementsByClassName("news_info")[1].getElementsByTagName("span")[0].innerText = list[i]["title"];
                let content = list[i]["content"].split(">")[1].split("<")[0];
                element.getElementsByClassName("detail")[0].getElementsByTagName("span")[0].innerText = limitWords(content, 20);
                element.getElementsByTagName("img").src = ((ServerURL())() + list[i]["picture"]);
            }
        }else{
            console.log(json["status"])
        }
    };
    let failHandler = function (error) {
        console.log(error.message);
    };
    getRequest((ServerURL())() + Url_Options.HOT_POT, "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    });
}
(function loadHotPot() {
    requestHotPot();
})();

/**
 * 热门影评
 * */
let hotCommentsList = document.getElementById("hot_comments").getElementsByClassName("hot_comment");
function requestHotComments() {
    let typeReflect = {
        "user_name": "author_name",
        "comment_time": "create_time",
        "content": "content",
        "title": "title",
        "movie_name": "film_name"
    };
    let successHandler = function (json) {
        let commentList = json["list"];
        // let types = ["user_name", "comment_time", "title", "content","movie_name"];
        let types = ["user_name", "comment_time", "title","movie_name"];
        for (let i = 0; i < hotCommentsList.length; i++) {
            for (let element in types) {
                if (types.hasOwnProperty(element)) {
                    if (types[element] === "content") {
                        hotCommentsList[i].getElementsByClassName(types[element])[0].innerText = limitWords((commentList[i])[typeReflect[types[element]]], 40);
                    } else if (types[element] === "comment_time") {
                        let wholeTime = (commentList[i])[typeReflect[types[element]]];
                        hotCommentsList[i].getElementsByClassName(types[element])[0].innerText = wholeTime.split("-")[0] + "." + wholeTime.split("-")[1] + "." + wholeTime.split("-")[2].split(" ")[0];
                    } else {
                        hotCommentsList[i].getElementsByClassName(types[element])[0].innerText = (commentList[i])[typeReflect[types[element]]];
                    }
                }
            }
            hotCommentsList[i].getElementsByClassName("portrait")[0].src = (ServerURL())() + (commentList[i])["author_head"];
            hotCommentsList[i].getElementsByClassName("img_cover")[0].src = (ServerURL())() + (commentList[i])["image"];
            hotCommentsList[i].getElementsByClassName("info_container")[0].addEventListener("click", (()=>{
                return ()=>{
                    window.location.href = "http://www.baidu.com?user_id=" + commentList[i]["author_id"];
                }
            })(), true);
        }
    };
    let failHandler = function (error) {
        console.log(error.message);
    };
    getRequest((ServerURL())() + Url_Options.HOT_REVIEW_LIST, "application/x-www-form-urlencoded", "json", "GET").then((json)=>{
        successHandler(json);
    }, (error)=>{
        failHandler(error);
    })
}
requestHotComments();
//回到顶部
//置顶
$(".toTop").click(function () {
    $('html,body').animate({scrollTop: '0px'}, 300);
});
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
 * 处理个人信息
 */
let createUser = function (json) {
    let user = {};
    let types = ["user_id","username", "head","email"];
    //测试用
    // user = {"user_id": "1", "username": "newive", "head": "#","email": "738767136@qq.com"};
    for(let i in types){
        if(types.hasOwnProperty(i)){
            user[types[i]] = json[types[i]];
        }
    }
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
    let __URL =  "http://39.96.208.176\\account\\i\\user\\info";  //在ajax属性内拼接
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
let register = document.getElementById("register");
let logIn = document.getElementById("logIn");
window.onload = (function checkIsLogIn() {
    if(getCookie("user_id")){
        console.log("1");
        let user_id = getCookie("user_id");
        getRequest(UserServerURL() + "\\" + user_id, "json", "application/x-www-form-urlencoded", "GET").then(
            (json)=>{
                if(json["status"] === "unknow_user"){
                    console.log("找不到用户");
                }else if(json["status"] === "ok") {
                    console.log(json);
                    user = getUserInfo(json);
                    console.log(user);
                    let usernameSpan = username.getElementsByTagName("span")[0];
                    let log = document.getElementsByClassName("log")[0];
                    log.href = "PersonalPage.html";
                    usernameSpan.innerText = user["username"];
                    username.style.display = "inline";
                    userPortrait.src = user["head"];
                    register.style.display = "none";
                    logIn.style.display = "none";
                }else{
                    console.log("未知错误");
                }
            },
            (error)=>{
                console.log(error.message);
            }
        )
    }
});
