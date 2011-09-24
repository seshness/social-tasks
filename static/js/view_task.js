$(function () {
  $('#create_comment').submit(function (event) {
    event.preventDefault();
	$('#post_button').attr('disabled', 'disabled');
	var comment = $('#comment_text').val();
	$('#comment_text').val('');
	$.ajax({
	  type: 'POST',
	  url: '/task/comment/',
	  data: {'content': comment, 'task_id': $('#comment_text').attr('task_id')},
	  success: function(response) {
        $('#comments').append(response);
		$('#post_button').removeAttr('disabled');
	  }
	});
  });
});
