//分页
    $(document).ready(function(){
 
    //分页 上一页
    $(document).on('click','.last-page',function(){
        var currPage = parseInt($('#currentPage').html());
        var lastPage = currPage-1;
        if(lastPage < 1){
            $('#currentPage').html(1);
        }else{
            $('#currentPage').html(lastPage);
            paginationRequest(); <!-- 获取后台数据的方法 -->
        }
    });
    //分页 下一页
    $(document).on('click','.next-page',function(){
        var currPage = parseInt($('#currentPage').html());
        var nextPage = currPage+1;
        var pageCount = $('#totalPage').html();
        if(nextPage <= pageCount){
            $('#currentPage').html(nextPage);
            paginationRequest();
        }else{
            $('#currentPage').html(pageCount);
        }
    });
    //分页处理
    function pagination(currentPage,totalPage){
        if(totalPage == 1){
            $('#pagination').hide();
        }else{
            $('#pagination').show();
            $('#currentPage').html(currentPage);
            $('#totalPage').html(totalPage);
        }
    }
    })
    //跳转
    function gotoPage(){
        params.pageNum = $.trim($('#toPage').val());
        getMappingData();	<!-- 获取后台数据的方法 -->
    }
    //分页请求数据
    function paginationRequest(){
        params.pageNum = $('#currentPage').html();
        getMappingData();
    }


//短评列表的
$.ajax({
    url: "http://106.13.106.1/film/i/short_comment_list/?film_id=",
    type: "get",
    dataType: "json",
    success: function(data){
        /*这个方法里是ajax发送请求成功之后执行的代码*/
        commentList(data);
        },
    error: function(msg){
        alert("ajax连接异常："+msg);
    }
});
function commentList(data) {
    var str = "";//定义用于拼接的字符串
    for (var i = 0; i < data.length; i++) {
        str = "<p><span>" + data[i].list.news_id +  "</span></p>";
        //替换原来的文本
        $("#main").replaceWith(str);         
    }
}