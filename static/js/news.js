//新闻详情的
$.ajax({
    url: "http://106.13.106.1/news/i/news/?news_id=",
    type: "get",
    dataType: "json",
    success: function(data){
        /*这个方法里是ajax发送请求成功之后执行的代码*/
        newsList(data);
        },
    error: function(msg){
        alert("ajax连接异常："+msg);
    }
});
function newsList(data) {
    var str = "";//定义用于拼接的字符串
    for (var i = 0; i < data.length; i++) {
        str = "<p><span>" + data[i].list.news_id +  "</span></p>";
        //替换原来的文本
        $("#main").replaceWith(str);         
    }
}