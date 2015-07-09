// Dealing with various kinds of accordion nonsense

var setExpanderText = function() {
	expander_text = $('#expander_text');
	if (expander_text.parent("a").hasClass("active")) {
		expander_text.text("Contract all");
	} else {
		expander_text.text("Expand all");
	}
};

var toggleAccordion = function(is_opened) {
	if (is_opened) {
		$('.accordion-navigation div.content').addClass('active');
	} else {
		$('.accordion-navigation div.content').removeClass('active');
	}
};

var getActiveIndicator = function() {
	indicator_matches = window.location.hash.match(/\#indicator_(\d*)/);
	return indicator_matches === null ? 1 : parseInt(indicator_matches[1]);
};

var shouldExpandIndicator = function() {
	return window.location.search.match(/expand=true/) !== null;
};

var showIndicator = function(indicator, expand_indicator) {
	indicator_container = $("#indicator_" + indicator);
	indicator_container.parents(".accordion-navigation div.content").addClass('active');
	if (expand_indicator) {
		indicator_container.children("a").trigger("click");
	}
};

var onIndicatorPage = function() {
	return window.location.pathname.match("countries") !== null;
};

$(document).ready(function() {
	$(document).foundation({
	  accordion: {
	    content_class: 'content',
	    active_class: 'active',
	    multi_expand: true,
	    toggleable: true
	  }
	});

	// Deal with expand all button
	$('a.expand-all').click(function(ev) {
		ev.preventDefault();
		$(this).toggleClass('active');
		setExpanderText();
		toggleAccordion($(this).hasClass('active'));
	});

	if (onIndicatorPage()) {
		indicator = getActiveIndicator();
		showIndicator(indicator, shouldExpandIndicator());
	}
});