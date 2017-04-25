

//关注
$(document).ready(function(){
  $(".followbtn").click(function(){
    var u_id = $(this).attr("follow_id")
    $.get("/people/do?follow_id="+u_id, function(response,status){
        if(status=='success') {parent.location.reload()}
        });;
    parent.location.reload()
  });
});


//任务完成
$(document).ready(function(){
  $(".task-done-btn").click(function(){
    var task_id = $(this).attr("tid")
    $.get("/task/do?done=true&id="+task_id, function(response,status){
        if(status=='success') {parent.location.reload()}
        });
  });
});


//任务删除
$(document).ready(function(){
  $(".task_delete_btn").click(function(){
      var task_id = $(this).attr("tid")
      if(confirm("删除后无法恢复，确定要删除吗")){
          $.get("/task/do?delete=true&id="+task_id, function(response,status){
              if(status=='success'){window.location.href="/task"}
              });
      }
  });
});



//评论开关
$(document).ready(function(){
  $(".comment_allow_btn").click(function(){
    var task_id = $(this).attr("tid")
	var comment_allow = $(this).attr("comment_status")
    $.get("/task/do?comment="+comment_allow+"&id="+task_id,  function(response,status){
        if(status=='success') {parent.location.reload()}
        });
  });
});


//点赞
$(document).ready(function(){
  $(".like_btn").click(function(){
    var task_id = $(this).attr("tid")
    $.get("/people/do?like_id="+task_id, function(response,status){
        if(status=='success') {parent.location.reload()}
        });


  });
});