$(function () {
  $('#main_content').load('/ajax/home/');

  $('#top_mytasks').click(function (event) {
    event.preventDefault();
    $('#main_content').load('ajax/home/');
	$('#top_create').attr('class', '');
	$('#top_mytasks').attr('class', 'active');
  });
  
  $('#top_create').click(function (event) {
    event.preventDefault();
    $('#main_content').load('task/create/');
	$('#top_create').attr('class', 'active');
	$('#top_mytasks').attr('class', '');
  });
});
