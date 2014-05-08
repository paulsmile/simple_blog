$(document).ready(function (){
	submit_comment();
	back_to_post();
	create_code();
   change_code();
   control_submit();
   modify_perview();
});

function back_to_post(){
	//实现返回按钮
    $("#back_to_post").click(function () {
        window.history.back();
        });
}

function submit_comment() {
	//实现ctrl+enter提交评论
	$(document).keypress(function e() {
		if (e.ctrlKey && e.which === 13 || e.which === 10) {
			$("#comment_from").submit();
		}
	});
}

function change_code() {
	//更改验证码
	$("#checkCode").click(function () {
		create_code();
	});
}

var code ;
function create_code(){
	//生成验证码
    code = "";
    var codeLength = 4;
    var checkCode = $("#checkCode");
    var selectChar = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L',
                'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

    for(var i=0;i<codeLength;i++){
        var charIndex = Math.floor(Math.random()*36);
        code +=selectChar[charIndex];
    }

    if(checkCode){
        checkCode.addClass("code");
        checkCode.val(code);
    }
}

function verify_code (){
	//验证验证码
    var user_input_code = $("#user_input_code").val().toLowerCase().trim();
    if(user_input_code.length <=0){
        return false;
    } else if(user_input_code != code.toLowerCase()){
        return false;
    }
    return true;
}

function control_submit() {
	//当验证码验证成功后，才允许提交评论
    $("#user_input_code").keyup(function () {
    	if ($("#user_input_code").val().trim().length>=4) {    
          if (verify_code()) {
	           $("#submit_comment").attr("disabled", false);
	       } else {
	           $("#valid_faild").text("验证码错误");
	       }
    	} else {
    		 $("#valid_faild").text("");
    	}
    });
}

function modify_perview() {
	//修改评论模块的perview页面
	$("#my_preview").find("#id_name").attr("placeholder", "请输入您的昵称");
	$("#my_preview").find("#id_email").attr("placeholder", "请输入您的邮箱（不会被公开）");
	$("#my_preview").find("#id_comment").attr("placeholder", "请输入您的评论");
   $("#my_preview").find("#id_url").parent().remove();
}