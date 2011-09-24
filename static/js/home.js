$(function () {
  $('#create_task').click(function (event) {
     event.preventDefault();
     $('#main_content').load('task/create/');
	 $('#top_create').attr('class', 'active');
	 $('#top_mytasks').attr('class', '');
  });
  
  $('a.task_entry').click(function (event) {
    event.preventDefault();
	alert('binding function');
	$('#main_content').load('task/'+$('this').id+'/');
  });
});
