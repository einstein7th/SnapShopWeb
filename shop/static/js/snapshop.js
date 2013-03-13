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

    $('.ingredient-list .ingredient-item').click(function(event) {
        $(this).toggleClass("selected");
        updateCart(this);
    });

    $('.remove-ingredient-list').click(function(event) {
        $("#"+$(this).data("containerid")).remove()
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
}

function updateCart(clickedElement) {
    var target$ = $("#cart-table tbody");

    // Add cart item to visible cart
    var element$ = $(clickedElement);
    var newRow$ = $('<tr>');
    var item_id = element$.data("item-id");

    var cart = getCart();

    newRow$.append("<td>" + '<img src="' + element$.children('img').attr('src') + '" width="24" height="24" />' + element$.data("item-name")+"</td>");
    newRow$.append('<td class="quantity">1</td>')
    newRow$.append("<td>$" + parseInt(element$.data("item-price"))/100.0+ "</td>");
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
    // console.log(cart);
    saveCartToServer(cart);
    renderPrice();
}

$(document).ready(init);
