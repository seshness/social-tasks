$(function () {
  $('#create_form').submit(function (event) {
    event.preventDefault();
	$.ajax({
	  type: 'POST',
	  url: '/task/make/',
	  data: {'content': $('#task_text').val(), 'title': $('#task_title').val()},
	  success: function(response) {
        $('#main_content').load('ajax/home/');
	    $('#top_create').attr('class', '');
	    $('#top_mytasks').attr('class', 'active');	  
	  }
	});
  });
});
