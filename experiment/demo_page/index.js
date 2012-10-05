var postList = [
	{
		title:"test1",
		date : "2012-10-01",
		url:"post1.html"
	},
	{
		title:"test2",
      		date:"2012-10-12",
      		url:"post2.html"
	}
];
var gotoBlog = function(url){
	var callback = function(content){
		$(".blog_list").remove();
		$(".main_content").append(content);
	};
	var param = {
		url : url,
		success : callback,
		contentType: "text/html; charset=gbk"
	};
	$.ajax(param);
	
};

$(function(){
	var context = {
		"blog_list": postList
	}
		
	var template = $("#blog_list_template").html();
	var html = Mustache.to_html(template, context);
	$(".main_content").append(html);	
});
