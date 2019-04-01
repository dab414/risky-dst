
function keyListen() {

	$(document).keydown(function(e){
		console.log(e.which);
		if (e.which == 32) {
			$('#keyToggle').show();
		}
	});

	$(document).keyup(function(e){
		if (e.which == 32) {
		$('#keyToggle').hide();
		}
	});

}