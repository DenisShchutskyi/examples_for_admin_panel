/*
*	Remove jQuery if you want pure css dropdown menus
*/

jQuery(document).ready(function($) {
	$("li.dropdown").hover(function() {
		var id = $(this).attr("rel");
		$(this).toggleClass("active");
		$("ul.dropdown-" + id).toggle("fade", 250);
	});
});