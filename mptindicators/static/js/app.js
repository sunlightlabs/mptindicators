$(document).ready(function(){
	// Autocomplete
	$("#autocomplete_chosen").chosen({width: "210px", search_contains: true});
	$("#autocomplete_chosen").change(function() {
	  $('.search-field').hide();
	  window.location.replace("/indicators/" + $(this).val() + "/");
	});
	style_current_indicator();

	// Country sorting
    $(document).ready(function() {
      $('select[name=o]').change(function() {
        var path = window.location.pathname;
        window.location = path + '?o=' + this.value;
      });
    });

    // Share stuff
    $(".facebook").click(function() {
    	FB.ui({
		  method: 'share',
		  link: window.location.href
		}, function(response){});
    });
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
