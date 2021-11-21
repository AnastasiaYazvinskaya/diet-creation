var i = 1;
var n = 2;

function find_prod_index() {
    // Finding the next index of product (if page was refreshed)
    index=0;
    for (let j=0; j<30; j++) {
        var check=document.getElementById('repeate_'+j);
        if (check) {
           index=j+1;
        }
    }
    return index;
}

$(document).ready(function() {
    /* Recipe Creation */
    // "Add ingredient" button click handling
    i=find_prod_index()+1
    $("#add").click(function() {
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