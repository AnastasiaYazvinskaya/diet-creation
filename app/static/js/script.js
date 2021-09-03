var i = 1;

$(document).ready(function() {
    // "Add ingredient" button click handling
    $("#add").click(function() {
        // Finding the next index of product (if page was refreshed)
        for (let j=1; j<30; j++) {
            var check=document.getElementById('repeate_'+j);
            if (check) {
               i=j+1;
            }
        }
        // Adding new fields for nex ingredient (ingredient name and weight)
        $("#ingredientAdd").append('<div class="form-group">' +
'        <label for="name_'+i+'">Name</label>' +
'        <input list="products" name="name_'+i+'" class="form-control" placeholder="'+(i+1)+' product name"></input>' +
'        <datalist id="types">' +
'            {% for product in prods %}' +
'                <option value="{{product["name"]}} [{{product["shop"]}}]"></option>' +
'            {% endfor %}' +
'        </datalist>' +     
'        <label for="weight_'+i+'">Weight (gram)</label>' +
'        <input type="number" step="0.01" name="weight_'+i+'"' +
'            placeholder="0.00" class="form-control"></input>' +
'    </div>');
        // Changing index
        i += 1;
        // Hide adding button if 30 ingredients was added
        if (i > 30) {
            $(this).hide();
        }
    });
});