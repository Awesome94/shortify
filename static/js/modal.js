$(document).ready(function(){
	$(document).on('click','.signup-tab',function(e){
		e.preventDefault();
	    $('#signup-taba').tab('show');
	});	
	

	$(document).on('click','.signin-tab',function(e){
	   	e.preventDefault();
	    $('#signin-taba').tab('show');
	});

	$('.edit-button').on('click', function(evt){
		$('#edit-modal').modal();
		var id = parseInt(this.dataset.id);
		$('input[name="url-id"]').val(id)
	});

	function onDeleteClick (evt) {
		$('#delete-modal').modal();
		var id = parseInt(this.dataset.id);
		console.log(this)
		$('input[name="link-id"]').val(id)
		
	}

	$('.delete-button').on('click', onDeleteClick);

});

function changeStatus(id){
	$.get( "/change-status/" + id, function( data ) {
		console.log( "Status was changed." );
	});
}
