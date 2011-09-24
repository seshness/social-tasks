!function ( $ ) {
  function prepareCreateTask() {
    $('#create_task').click(function (event) {
	  event.preventDefault();
	  $('#main_content').load('create_task.html');
	});
  }
  
  prepareCreateTask();

}( window.jQuery );