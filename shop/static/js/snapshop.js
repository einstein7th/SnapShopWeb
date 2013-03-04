
function init() {

    $('.tooltipped').tooltip();
    $('.half-height').each(function(index,element) {
	var targetHeight =  $(element).height();
	var parentHeight = $(element).parent().height();
	
	$(element).css("position","relative");
	$(element).css("top",(parentHeight-targetHeight)/2)
	$(element).css("margin-top",0)
	$(element).css("margin-bottom",0)
		
    });

    $('.ingredient-list .ingredient-item').click(function(event) {
	$(this).toggleClass("selected");
	updateCart();
    });
}

function updateCart() {
    var target$ = $("#cart-table tbody");
    var total = 0

    target$.html("");

    $('.ingredient-list .ingredient-item.selected').each(function(index,element) {
	var element$ = $(element);
	var newRow$ = $('<tr>');

	total+=element$.data("item-price");

	newRow$.append("<td>" + element$.data("item-name")+"</td>");
	newRow$.append("<td>1</td>")
	newRow$.append("<td>$" + parseInt(element$.data("item-price"))/100.0+ "</td>");
	newRow$.append("<td></td>")
	target$.append(newRow$);
    });
}



$(document).ready(init);
