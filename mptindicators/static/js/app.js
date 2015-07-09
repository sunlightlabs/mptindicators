$(document).ready(function(){
	$("#autocomplete_chosen").chosen({width: "210px"});
	$("#autocomplete_chosen").change(function() {
	  $('.search-field').hide();
	  window.location.replace("/indicators/" + $(this).val() + "/");
	});
	style_current_indicator();
});

get_current_indicator = function() {
	indicator_match = window.location.pathname.match(/\/indicators\/(.*)\//);
	return indicator_match === null ? false : indicator_match[1]; 
};

style_current_indicator = function(indicator) {
	indicator = get_current_indicator();
	if (indicator) {
		active_list_item = $("[data-indicator=" + indicator + "]").parent("li");
		active_list_item.addClass("current");
	}
};
