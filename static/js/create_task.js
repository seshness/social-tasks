$(function () {
  $('#submit_task').click(function (event) {
    event.preventDefault();
	.ajax({
	  type: 'POST',
	  url: '/task/make/',
	  data: $('#task_text').val(),
	  success: function(response) {
        $('#main_content').load('ajax/home/');
	    $('#top_create').attr('class', '');
	    $('#top_mytasks').attr('class', 'active');	  
	  }
	});
  });
});
