// helper functions

/**
 * Requires a modal#modal element present
 * Show a modal with customized message
 * @param  {String} message Message to show
 * @return {Void}
 */
function showModal(message) {
	// set error message
	$('#modal .modal-body').html(message);
	// show modal
	$('#modal').modal();
}