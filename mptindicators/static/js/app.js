$(document).ready(function(){
	$("#autocomplete_chosen").chosen({width: "210px"});
	$("#autocomplete_chosen").change(function() {
	  $('.search-field').hide();
	  window.location.replace("/indicators/" + $(this).val() + "/");
	});
});

