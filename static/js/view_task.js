$(function () {
  $('#create_comment').submit(function (event) {
    event.preventDefault();
	$.ajax({
	  type: 'POST',
	  url: '/task/make/',
	  data: {'content': $('#task_text').val()},
	  success: function(response) {
        alert('created comment');
	  }
	});
  });
});
