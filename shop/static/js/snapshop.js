//cart = []

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

    $('.ingredient-list-container .navbar').click(function(event) {
	$(this).next().toggle();
    });

    $('#submit-navbar-form').click(function() {
	$('#navbar-form').submit();
    });


    //chosen.js doesn't support dynamic adding of tokens. 
    //This will do it for us now
    $('.chzn-select').chosen({no_results_text: "Add: "});
    $('.chzn-select').each(function() {
	chosen$ = $(this);
	var chosen_chzn$ = $("#"+chosen$.attr("id")+"_chzn");
	$('input',chosen_chzn$).first().keyup(function(event) {
	    var k = event.which;
	    if (k!=13) {
		return;
	    }
	    event.preventDefault();
	    var options = $('option',chosen$).map(function(i,e) {return e.value}).toArray();
	    var currentValue = $(this).val();
	    a = options;
	    if (options.indexOf(currentValue)==-1) {
		chosen$.append("<option selected value='"+currentValue+"'>"+currentValue+"</option>")
	    }
	    chosen$.trigger("liszt:updated");
	});
    });

    $('.ingredient-list .ingredient-item').click(function(event) {
        $(this).toggleClass("selected");
        updateCart(this);
    });

    $('.remove-ingredient-list').click(function(event) {
        $("#"+$(this).data("containerid")).remove()
    });

    $('.index-back').click(function(event) {
	var listElement$ = $("#"+$(this).data("target"))
	var keyword = listElement$.data("keyword");
	var newIndex = Math.max(0,parseInt(listElement$.data("page"))-1)
	listElement$.data("page",newIndex);
	$('#'+keyword+'-index').html(newIndex+1);
	$('.row-'+keyword).hide();

	$('#row-'+keyword+"-"+newIndex).show();
    });

    $('.index-forward').click(function(event) {
	var listElement$ = $("#"+$(this).data("target"))
	var keyword = listElement$.data("keyword");
	var newIndex = Math.min(20,parseInt(listElement$.data("page"))+1)
	$('#'+keyword+'-index').html(newIndex+1);
	listElement$.data("page",newIndex);
	$('.row-'+keyword).hide();

	$('#row-'+keyword+"-"+newIndex).show();
    });

    updateIconListeners();
}

function getCart() {
    var cart = {}
    var cart_json = $('#id_items_list').val();
    if (!cart_json) {
        cart_json = ""
    }
    if (cart_json.length > 0) {
        cart = $.parseJSON(cart_json);
        if (cart == null) {
            cart = {}
        }
    }
    return cart;
}

function renderPrice() {
    var target$ = $("#cart-table tbody");
    var cart = getCart();
    var total = 0;

    for (var item in cart) {
        if (cart.hasOwnProperty(item)) {
            var price = $('*[data-item-id="' + item + '"]').data("item-price");
            total += price * cart[item];
        }
    }

    $("tr.summary-row").remove();
    var summaryRow$ = $('<tr class="summary-row"><td><b>Total: </b></td><td></td><td><b id="cart_total">$' + (total/100.0).toFixed(2) + '</b></td><td></td></tr>');
    target$.append(summaryRow$);

    // if (total == 0) {
    //     target$.append("<td colspan='4'>You currently have no items in your cart")
    // }
}

function saveCartToServer(cart) {
    for (var item in cart) {
        if (cart.hasOwnProperty(item)) {
            if(cart[item] < 1) {
                delete cart[item];
            }
        }
    }

    $('#id_items_list').val(JSON.stringify(cart));

    // Send cart change to server, which will save it
    $.ajax({
        type: "POST",
        url: "/save_cart/",
        data: {'data': JSON.stringify(cart)}
    }).done(function() {
        //console.log('done saving cart')
    })
}

function updateIconListeners() {
    // TODO Fix Hacky method of ensuring click listeners only attached
    // once even if new elements appear
    $(".increase-quantity-icon").unbind();
    $(".decrease-quantity-icon").unbind();
    $(".remove-item-icon").unbind();
    $(".view-item-icon").unbind();

    $(".increase-quantity-icon").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');

        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            cart[item_id] += 1;
        }

        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);

        saveCartToServer(cart);
        renderPrice();
    });

    $(".decrease-quantity-icon").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            if (cart[item_id] > 1) {
                cart[item_id] -= 1;
            } else if (cart[item_id] <= 1) {
                // Remove item basically. Deselect from area above to prevent future from clicks from bringing back
                $('*[data-item-id="' + item_id + '"]').removeClass('selected');
                row$.remove();
                delete cart[item_id];
            }

        }

        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);

        saveCartToServer(cart);
        renderPrice();
    });

    $(".remove-item-icon").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            // Remove item basically. Deselect from area above to prevent future from clicks from bringing back
            $('*[data-item-id="' + item_id + '"]').removeClass('selected');
            row$.remove();
            delete cart[item_id];
        }

        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);

        saveCartToServer(cart);
        renderPrice();
    });

    $('.view-item-icon').click(function(event) {
	event.preventDefault();
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
	$.ajax({'url':'/view-item/'+item_id+'/',
		'success': function(data) {
		    $('#preview-modal-container').html(data);
		    $('#preview-modal-container .modal').modal();
		}});
    });
}

function updateCart(clickedElement) {
    var target$ = $("#cart-table tbody");

    // Add cart item to visible cart
    var element$ = $(clickedElement);
    var newRow$ = $('<tr>');
    var item_id = element$.data("item-id");

    var cart = getCart();

    newRow$.append("<td>" + '<img src="' + element$.children('img').attr('src') + '" width="24" height="24" />' + element$.data("item-name") + " (" + element$.data("item-size") + ") " + "<i class='icon-search view-item-icon'></i></td>");
    newRow$.append('<td class="quantity">1</td>')
    newRow$.append("<td>$" + (parseInt(element$.data("item-price"))/100.0).toFixed(2) + "</td>");
    newRow$.append('<td><i class="icon-chevron-down decrease-quantity-icon"></i> <i class="icon-chevron-up increase-quantity-icon"></i><i class="icon-remove remove-item-icon"></i></td>')
    newRow$.attr('data-item-id', item_id);
    target$.append(newRow$);

    updateIconListeners();      // update icon listeners each time we get a new row

    var element$ = $(clickedElement);
    // Add cart item to purchase form, which is a hidden input field

    // Decide whether we need to add new row or remove row
    if (cart.hasOwnProperty(item_id)) {
        // Clicking an item again toggles/removes it from cart
        if (cart[item_id] > 0) {
            cart[item_id] = 0;
            target$.children('tr[data-item-id="' + item_id + '"]').remove();
        } else {
            cart[item_id] = 1;
        }
    } else {
        cart[item_id] = 1;
    }

    saveCartToServer(cart);
    renderPrice();
}

$(document).ready(init);
