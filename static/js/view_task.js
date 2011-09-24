$(function () {
  $('#create_comment').submit(function (event) {
    event.preventDefault();
	$.ajax({
	  type: 'POST',
	  url: '/task/comment/',
	  data: {'content': $('#comment_text').val(), 'task_id': $('#comment_text').attr('task_id')},
	  success: function(response) {
        alert('created comment');
	  }
	});
  });
});
