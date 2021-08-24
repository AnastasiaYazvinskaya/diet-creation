var i = 2;
//ex = "#ingred"
//var val1 = "{{ request.form['name_"+i+"'] }}";
//var val2 = "{{ request.form['weight_"+i+"'] }}";
/*
$(document).ready(function() {
    $("button#add").click(function() {
        tag = ex + i;
        i += 1;
        $(tag).show();
        if (i == 29){
            $(this).hide();
        }
    });
});
*/

$(document).ready(function() {
    $("#add").click(function() {
        $("#ingredientAdd").append(addField());
        i += 1;
        if (i > 30) {
            $(this).hide();
        }
    });
});

function addField() {
    var div = document.createElement('div');
    var label_1 = document.createElement('label');
    var input_1 = document.createElement('input');
    var label_2 = document.createElement('label');
    var input_2 = document.createElement('input');

    div.setAttribute("class", "form-group");

    label_1.setAttribute("for", "name_"+i);
    label_1.textContent = "Name";
    input_1.setAttribute("type", "text");
    input_1.setAttribute("name", "name_"+i);
    input_1.setAttribute("placeholder", i+" Product name");
    input_1.setAttribute("class", "form-control");

    label_2.setAttribute("for", "weight_"+i);
    label_2.textContent = "Weight (gram)";
    input_2.setAttribute("type", "number");
    input_2.setAttribute("name", "weight_"+i);
    input_2.setAttribute("placeholder", "0.00");
    input_2.setAttribute("class", "form-control");

    div.appendChild(label_1);
    div.appendChild(input_1);
    div.appendChild(label_2);
    div.appendChild(input_2);

    return div;
}
