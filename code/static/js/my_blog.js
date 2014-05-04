$(document).ready(function (){
	submit_comment();
});

function submit_comment() {
	$(document).keypress(function e() {
		if (e.ctrlKey && e.which === 13 || e.which === 10) {
			$("#comment_from").submit();
		});
}