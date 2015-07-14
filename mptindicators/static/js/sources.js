regexp = new RegExp(/http[^\s]*/g);
$.each($(".sources p"), function(index, e){
	new_text = $(e).html().replace(regexp, "<a href='$&'>$&</a>");
	new_text = new_text.replace(/<em>/g, "_");
	new_text = new_text.replace(/<\/em>/g, "_");
	$(e).html(new_text);
});
