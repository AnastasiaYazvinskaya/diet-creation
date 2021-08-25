var i = 2;

$(document).ready(function() {
    $("#add").click(function() {
        $("#ingredientAdd").append('<div class="form-group">' +
'        <label for="name_'+i+'">Name</label>' +
'        <input list="products" name="name'+i+'" class="form-control" placeholder="'+i+' product name"></input>' +
'        <datalist id="types">' +
'            {% for product in prods %}' +
'                {% for shop in shops %}' +
'                    {% if product["shop_id"] = shop["id"] %}' +
'                        <option value="{{product["name"]}}"></option>' +
'                    {% endif %}' +
'                {% endfor %}' +
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
/*
    $("#addProduct").append('<!-- Modal -->' +
'    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">' +
'      <div class="modal-dialog" role="document">' +
'        <div class="modal-content">' +
'          <div class="modal-header">' +
'            <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>' +
'            <button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
'              <span aria-hidden="true">&times;</span>' +
'            </button>' +
'          </div>' +
'          <div class="modal-body">' +
'            ' +
'          </div>' +
'          <div class="modal-footer">' +
'            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>' +
'            <button type="button" class="btn btn-primary">Save changes</button>' +
'          </div>' +
'        </div>' +
'      </div>' +
'    </div>');
*/
});