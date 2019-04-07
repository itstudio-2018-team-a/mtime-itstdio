//智能浮动
var $smartFloat = function(elements) {
    var position = function(element) {
        var top = element.getPosition().y, pos = element.getStyle(“position”);
        window.addEvent(“scroll”, function() {
            var scrolls = this.getScroll().y;
            if (scrolls > top) {
                if (window.XMLHttpRequest) {
                    element.setStyles({
                        position: “fixed”,
                        top: 0
                    });    
                } else {
                    element.setStyles({
                        top: scrolls
                    });    
                }
            }else {
                element.setStyles({
                    position: “absolute”,
                    top: top
                });    
            }                       
        });
    };
    if ($type(elements) === “array”) {
        return elements.each(function(items) {
            position(items);                         
        });
    } else if ($type(elements) === “element”) {
        position(elements);    
    }
};
//绑定
$smartFloat($(“float”));







$.ajax({
    url: "http://106.13.106.1/film/i/film_review_comment/?review_id=",
    type: "get",
    dataType: "json",
    success: function(data){
        /*这个方法里是ajax发送请求成功之后执行的代码*/
        showData(data);
        },
    error: function(msg){
        alert("ajax连接异常："+msg);
    }
});
function showData(data) {
    var str = "";//定义用于拼接的字符串
    for (var i = 0; i < data.length; i++) {
        str = "<p><span>" + data[i].list.news_id +  "</span></p>";
        //替换原来的文本
        $("#main").replaceWith(str);         
    }
}