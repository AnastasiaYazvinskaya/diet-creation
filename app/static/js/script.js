var i = 1;

$(document).ready(function() {
    $("#add").click(function() {
        $("#ingredientAdd").append('<div class="form-group">' +
'        <label for="name_'+i+'">Name</label>' +
'        <input list="products" name="name_'+i+'" class="form-control" placeholder="'+(i+1)+' product name"></input>' +
'        <datalist id="types">' +
'            {% for product in prods %}' +
'                <option value="{{product["name"]}} [{{product["shop"]}}]"></option>' +
'            {% endfor %}' +
'        </datalist>' +     
'        <label for="weight_'+i+'">Weight (gram)</label>' +
'        <input type="number" name="weight_'+i+'"' +
'            placeholder="0.00" class="form-control"></input>' +
'    </div>');
        i += 1;
        if (i > 30) {
            $(this).hide();
        }
    });

    $("#addProduct").append('<div class="form-group">' +
'    <label for="name">Name</label>' +
'    <input type="text" name="name"' +
'           placeholder="Product name" class="form-control" value="'+$("span#product").text()+'"></input>' +
'</div>' +
'<div class="form-group">' +
'    <label for="weight">Weight (gram)</label>' +
'    <input type="number" name="weight" placeholder="0.00"' +
'              class="form-control"></input>' +
'</div>' +
'<div class="form-group">' +
'    <label for="price">Price (rubles)</label>' +
'    <input type="number" name="price" placeholder="0.00"' +
'              class="form-control"></input>' +
'</div>' +
'<div class="form-group">' +
'    <label for="shop">Shop</label>' +
'    <input list="shops" name="shop" class="form-control" placeholder="Shop name"  value="{{ request.form["shop"] }}"></input>' +
'    <datalist id="shops">' +
'        {% for shop in shops %}' +
'        <option value="{{shop["name"]}}"></option>' +
'        {% endfor %}' +
'    </datalist>' +
'</div>');
        
       // '<div>'+$("span#product").text()+'</div>');
});