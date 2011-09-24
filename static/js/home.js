$(function () {
  $('#create_task').click(function (event) {
     event.preventDefault();
     $('#main_content').load('task/create');
  });
});