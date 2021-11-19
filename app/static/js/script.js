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
    
    /* Menu Creation */
    /*
    $("#addWeek").click(function() {
        // Adding new fields for nex ingredient (ingredient name and weight)
        $("tbody").append('<tr><th scope="row" rowspan="3">'+n+'</th>' +
        '{% for d in range(7) %}' +
        '<td class="drop breakfast">Breakfast</td>' +
        '{% endfor %}d></tr>' +
        '<tr>{% for d in range(7) %}' +
        '<td class="drop lunch">Lunch</td>' +
        '{% endfor %}</tr>' +
        '<tr>{% for d in range(7) %}' +
        '<td class="drop dinner">Dinner</td>' +
        '{% endfor %}</tr>');
        // Changing index
        n += 1;
        // Hide adding button if 30 ingredients was added
        if (n > 4) {
            $(this).hide();
        }
    });

    for (let j=0; j<10; j++){
        let sel1 = "#show_"+j;
        let sel2 = "#"+j+"_hide";
        $(sel1).click(function(){
            $(sel2).show();
            for (let k=0; k<10; k++){
                let sel3 = "#"+k+"_hide";
                if (k != j){
                    $(sel3).hide();
                }
            }
        });
    } 
    
    $(".drag").draggable({
        containment: "#container",
        helper: "clone",
    });
    $(".dinner").droppable({
        accept: "#1",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.clone())
                .css("background-color", "rgb(195, 226, 192)");
        }
    });

    $(".breakfast").droppable({
        accept: "#2",
        tolerance: "intersect",
        drop: function( event, ui ) {
            $(this).css("background-color", "rgb(195, 226, 192)").text(ui.draggable.text());
            $('breakfast_0').val(ui.draggable.text());
        }
    });
    $(".salad").droppable({
        accept: "#3",
        drop: function( event, ui ) {
            let val = document.get
          $( this )
            .addClass( "ui-state-highlight" )
            .html( "Salad dropped" )
            .css("border", "thin solid rgb(40, 190, 52)");
        }
    });
    */
});