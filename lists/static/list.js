window.Superlists = {};
window.Superlists.initialize = function () {
	console.log('initialize called');
	$('input[name="text"]').on('keypress', function() {
		console.log('in keypress handler');
		$('.invalid-feedback').hide();
	});
}

console.log('list.js loaded');