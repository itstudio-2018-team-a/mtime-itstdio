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
