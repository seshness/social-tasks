$(function () {
  $('#create_task').click(function (event) {
     event.preventDefault();
     $('#main_content').load('task/create');
  });
  
  $('td .task_entry').click(function (event) {
    event.preventDefault();
	$('main_content').load('task/'+$('this').id);
  });
});
