$(function () {
  $('#create_form').submit(function (event) {
    event.preventDefault();
	alert('sending ajax post');
	$.ajax({
	  type: 'POST',
	  url: '/task/make/',
	  data: {'content': $('#task_text').val(), 'title': $('#task_title').val()},
	  success: function(response) {
	    alert('successful post');
        $('#main_content').load('ajax/home/');
	    $('#top_create').attr('class', '');
	    $('#top_mytasks').attr('class', 'active');	  
	  }
	});
  });
});
