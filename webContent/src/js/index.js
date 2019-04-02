/***
 * 正在热映
 * 热门评论
 * 新闻
 */
/***
 * 获取服务器URL
 * @returns {function(): string}
 * @constructor
 */
let movie_covers = document.getElementsByClassName("movie_covers");

let ServerURL = ()=>{
    let __URL = "http://106.13.106.1";
    return ()=>{
        return __URL;
    }
};
const URL_INTERFACE = {
    REQUEST_FOR_MOVIE_LIST: "\\film\\i\\film_list",
    REQUEST_FOR_MOVIE_INFO: "\\film\\i\\film\\?film_id=",
    REQUST_FOR_MOVIE_COVER: "\\"
};
const preLoadImgSrc = "../templates/marvel_captain_1.png";
/***
 * 图片预加载
 */
let preImg = function(node){
    let imgNode = node;
    return {
        setSrc: function (src) {
            imgNode.src = src;
        }
    }
};
let proxyImg = (function(node){
    let img = new Image();
    img.onload = function (){
        (preImg(this))().setSrc(this.src);
    };
    return{
        setSrc: function (node, src) {
            (preImg(node))().setSrc(src);
        }
    }
})();
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
 * 加载正在热映
 * @param dom
 */
let movieListArray = [];
let hotVideos = document.getElementById("hot_videos");
let display_movies = document.getElementById("display_movies");
/***
 *设置单个dom的值（正在热映）
 * @param parentNode
 * @param className
 * @param valueObj
 */
function setMovieInfo(parentNode ,className, valueObj) {
    let string = limitWords(valueObj["txt"], valueObj["wordsNumber"]);
    parentNode.getElementsByName(className).innerText = value;
}
/***
 * 限制字数
 */
function limitWords(content, number) {
    if(content.length >= number){
        content = content.substr(0, number) + "...";
    }
    return content;
}
/***
 *设置详细电影信息（正在热映）
 * @param movie
 * @param infoObj
 */
function setDetailedMovieInfo(movie, infoObj) {
    let classNameLength = {
        "movie_name": "8",
        "movie_lang": "5",
        "movie_time": "4",
        "movie_type": "10",
        "movie_director": "20",
        "movie_actor": "30",
        "movie_length": "4",
        "movie_description": "97"
    };
    let spanArray = movie.getElementsByTagName("span");
    for(let i = 0; i < spanArray; i++){
        let className = spanArray[i].className.split(" ")[0];
        let length = nameTypeO
    }
}
/***
 *  请求
 * @param number
 */
function requestHotMovie(number) {
    let successHandler = (json)=>{
        movieListArray = json["list"];
        let movies = hotVideos.getElementsByClassName("movie");
        for(let i = 0; i < movies.length; i++){

        }
    };
    let failHandler = (error)=>{
        console.log(error.message);
    };
    getRequest((ServerURL())() + URL_INTERFACE.REQUEST_FOR_MOVIE_LIST + number, "application/x-www-form-urlencoded", "json", "GET").then(
        (json)=>{
            successHandler(json);
        }, (error)=>{
            failHandler(error);
        }
    )
}
