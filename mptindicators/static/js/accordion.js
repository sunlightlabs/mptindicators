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

// for dealing with accordion nonsense
$(document).ready(function() {
	$(document).foundation({
	  accordion: {
	    // specify the class used for accordion panels
	    content_class: 'content',
	    // specify the class used for active (or open) accordion panels
	    active_class: 'active',
	    // allow multiple accordion panels to be active at the same time
	    multi_expand: true,
	    // allow accordion panels to be closed by clicking on their headers
	    // setting to false only closes accordion panels when another is opened
	    toggleable: true
	  }
	});
	setExpanderText();
	$('a.expand-all').click(function(ev) {
		ev.preventDefault();
		$(this).toggleClass('active');
		setExpanderText();
		toggleAccordion($(this).hasClass('active'));
	});
});