function ( $ ) {
  function prepareCreateTask() {
    $('#create_task').click(function (event) {
	  event.preventDefault();
	  $('#main_content').load('home.html');
	});
  }
  
  prepareCreateTask();

}