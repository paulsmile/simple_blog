$(document).ready(function (){
	submit_comment();
	back_to_post();
});

function back_to_post(){
    $("#back_to_post").click(function () {
        window.history.back();
        });
}

function submit_comment() {
	$(document).keypress(function e() {
		if (e.ctrlKey && e.which === 13 || e.which === 10) {
			$("#comment_from").submit();
		}
	});
}