/*
This file will contain all of your custom skin JavaScript.
*/

function isIE6() {
	if (typeof document.body.style.maxHeight == "undefined") {
		return true;
	} 
	return false;
}

$(document).ready(function() {
	
	// ADD CLASSES TO DROPDOWNS
	$(".drop-down").each( function() {
		$(this).find("li:first").addClass("first");
		$(this).find("li:last").addClass("last");	
	});
	
	
	// HIDE DROPDOWN
	$("body").click( function() {
		
		$(".drop-down").hide();	
	});
	
	// SHOW DROPDOWN
	$(".drop-down").parent("li").addClass("drop-link");
	
	$(".drop-link").click( function() {
		var dlink = $(this);
		var p = dlink.position();
		var dleft = p.left;
		var dtop = p.top;
		var dheight = dlink.outerHeight();
		
		
		$(".drop-link").not(this).find(".drop-down").hide();	
		var ddown = $(this).find(".drop-down");
		ddown.css("top",dtop + dheight);
		
		if (!isIE6()) 
		{
			ddown.css("left",dleft);
		}
		ddown.slideDown();
		
	});
	
	// Reset Text Inputs
	$("[resetval]").each( function() {
		var sval = $(this).val();
		var resetval = $(this).attr("resetval");
		if (sval == "")
		$(this).val(resetval);
	});
	$("[resetval]").focus( function() {
		var resetval = $(this).attr("resetval");
		var textval = $(this).val();
		if (textval == resetval)
		$(this).val('');
	});
	$("[resetval]").blur( function() {
		var resetval = $(this).attr("resetval");
		var textval = $(this).val();
		if (textval == resetval ||  textval=='')
		$(this).val(resetval);
	});
	
	// ALTERNATING ROWS
	
	// Button CSS for deeply rooted buttons
    $("input[type=submit]").addClass("btn");
    $("input[type=button]").addClass("btn");
    $(".commentActions input").addClass("btn");
    $(".commentActions a").addClass("btn");
    $("#deki-page-alerts div.toggle a").attr("title","Manage notifications");
    $(".page a.disabled").parent().hide();
});

