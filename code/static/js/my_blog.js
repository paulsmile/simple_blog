$(document).ready(function () {
	var codeLength = 4;
	back_to_post();
	create_code(codeLength);
	change_code(codeLength);
	control_submit(codeLength);
	hide_top_btn();
	show_top_btn();
	top_btn();
	getAllComments();
});

function back_to_post() {
	//实现返回按钮
	$("#back_to_post").click(function () {
		window.history.back();
	});
}


function change_code(codeLength) {
	//更改验证码
	$("#checkCode").click(function () {
		create_code(codeLength);
	});
}

var code ;

function create_code(codeLength){
	//生成验证码
	code = "";
	var checkCode = $("#checkCode");
	var selectChar = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');
	for(var i=0; i<codeLength; i++) {
		var charIndex = Math.floor(Math.random()*36);
		code +=selectChar[charIndex];
	}
	if(checkCode) {
		checkCode.val(code);
	}
}

function verify_code () {
	//验证验证码
	var user_input_code = $("#user_input_code").val().toLowerCase().trim();
	if(user_input_code.length <=0) {
		return false;
	} else if(user_input_code != code.toLowerCase()) {
		return false;
	}
	return true;
}

function control_submit(codeLength) {
	//当验证码验证成功后，才允许提交评论
	$("#user_input_code").keyup(function () {
		var code_len = $("#user_input_code").val().trim().length
		if (code_len < codeLength) {
			$("#valid_failed").text("");
		} else if (code_len > codeLength) {
			$("#valid_failed").text("验证码错误");
		} else {
			if (verify_code()) {
				$("#submit_comment").attr("disabled", false);
			} else {
				$("#valid_failed").text("验证码错误");
			}
		}
	});
}

function hide_top_btn() {
	//隐藏返回顶部按钮
	$("#back-to-top").hide();
}

function show_top_btn() {
	//显示返回顶部按钮
	$(window).scroll(function () {
		if ($(window).scrollTop()>100) {
			$("#back-to-top").fadeIn(1000);
		} else {
			$("#back-to-top").fadeOut(1000);
		}
	});
}

function top_btn() {
	$("#back-to-top").click(function () {
		$("body, html").animate({scrollTop: 0}, 1000);
		return false;
	});
}

function getAllComments() {
	var url = $('#all_comments').attr('data-url');
	$('#all_comments').text('');
	$.getJSON(url, function(data) {
		$.each(data.comments, function(idx, comment) {
			var all_comments = "<li><p><b><a href='/blog/" + comment.blog_id + "#comment_content'>";
			all_comments += comment.author + "&nbsp;&nbsp;回复：" + comment.blog_title + "：</a></b></p>";
			all_comments += "<p>" + comment.content + "</p></li>";
			$('#all_comments').append(all_comments);
		});
	});
}
