//智能浮动
// var $smartFloat = function(elements) {
//     var position = function(element) {
//         var top = element.getPosition().y, pos = element.getStyle("position");
//         window.addEvent("scroll", function() {
//             var scrolls = this.getScroll().y;
//             if (scrolls > top) {
//                 if (window.XMLHttpRequest) {
//                     element.setStyles({
//                         position: "fixed",
//                         top: 0
//                     });    
//                 } else {
//                     element.setStyles({
//                         top: scrolls
//                     });    
//                 }
//             }else {
//                 element.setStyles({
//                     position: "absolute",
//                     top: top
//                 });    
//             }                       
//         });
//     };
//     if ($type(elements) === "array") {
//         return elements.each(function(items) {
//             position(items);                         
//         });
//     } else if ($type(elements) === "element") {
//         position(elements);    
//     }
// };
// //绑定
// $smartFloat($("float"));







// $.ajax({
//     url: "http://106.13.106.1/film/i/film_review_comment/?review_id=",
//     type: "get",
//     dataType: "json",
//     success: function(data){
//         /*这个方法里是ajax发送请求成功之后执行的代码*/
//         showData(data);
//         },
//     error: function(msg){
//         alert("ajax连接异常："+msg);
//     }
// });
// function showData(data) {
//     var str = "";//定义用于拼接的字符串
//     for (var i = 0; i < data.length; i++) {
//         str = "<p><span>" + data[i].list.news_id +  "</span></p>";
//         //替换原来的文本
//         $("#main").replaceWith(str);         
//     }
// }

/***
 * 服务器地址
 */
const ServerURL = function () {
    let __URL =  "http://106.13.106.1";  //在ajax属性内拼接
    return ()=>{
        return __URL;
    }
};
/***
 * 接口
 */
const Url_Interface = {
    REQUEST_FOR_DETAILED_REVIEW: "\\film\\i\\film_review",
    REQUEST_FOR_FILE_REVIEW_COMMENT: "\\film\\i\\film_review_comment"
};
/***
 * 长评：单例模式
 */
let createDetailedComment = function (json) {
    let detailedComment = {};
    let types = ["comment_id","content", "author_id","author_name","author_head","time"];
    for(let i in types){
        if(types.hasOwnProperty(i)){
            user[types[i]] = json[types[i]];
        }
    }
    return detailedComment;
};
let getDetailedComment = function (json) {
    let detailedComment;
    return function () {
        return detailedComment || (detailedComment = createDetailedComment.apply(this, json));
    }
};
/***
 * 获取URL中的comment_id
 */
let comment_id;
function getCommentIDFromURL() { 
    let url = window.location.href.split("?")[1];
    if(url){
        if(url.split("=")[0] === "comment_id"){
            let comment_id = url.split("=")[1];
            if(Number(comment_id)){
                return Number(comment_id);
            }else{
                alert("评论id不合法");
                window.location.href = "index.html";
            }
        }else{
            alert("请前往别的模块");
            window.location.href = "index.html";
        }
    }else{
        alert("该评论不存在");
        window.location.href = "index.html";
    }
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
window.onload = ()=>{
    comment_id = getCommentIDFromURL();
};