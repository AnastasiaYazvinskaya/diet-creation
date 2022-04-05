var n = 2;

function find_prod_index() {
    // Finding the next index of product (if page was refreshed)
    let index=1;
    for (let j=0; j<30; j++) {
        var check=document.getElementById('repeate_'+j);
        if (check) {
           index=j+1;
        }
    }
    return index;
}
function find_step_index() {
    let index=1;
    for (let j=0; j<30; j++) {
        var check=document.getElementById('step_repeate_'+j);
        if (check) {
           index=j+1;
        }
    }
    return index;
}

$(document).ready(function() {
    /* Recipe Creation */
    // "Add ingredient" button click handling
    let i=find_prod_index();
    $("#add").click(function() {
        // Adding new fields for next ingredient (ingredient name and weight)
        $("#ingredientAdd").append('<div class="form-group">' +
'        <label for="name_'+i+'">Название '+(i+1)+'-го продукта</label>' +
'        <input list="products" name="name_'+i+'" class="form-control" placeholder="Название продукта"></input>' +
'        <datalist id="products">' +
'            {% for product in products %}' +
'                <option value="{{product["name"] | capitalize}}"></option>' +
'            {% endfor %}' +
'            {% for product in r_products %}' +
'                <option value="{{product["name"]}}"></option>' +
'            {% endfor %}' +
'        </datalist>' +    
'        <div id="weight"><div class="form-group">' + 
'            <label for="weight_'+i+'">Количество</label>' + 
'            <input type="number" step="0.01" name="weight_'+i+'" placeholder="0.00"' + 
'               class="form-control" value=""></input></div>' + 
'       <div class="form-group">' + 
'           <label for="weight-type_'+i+'">Измерение</label>' + 
'           <input list="weight-types" name="weight-type_'+i+'" placeholder="кг, г, л, мл, шт и т.д."' + 
'               class="form-control" value=""></input>' + 
'           <datalist id="weight-types">' + 
'               <option value="кг"></option>' + 
'               <option value="г"></option>' + 
'               <option value="л"></option>' + 
'               <option value="мл"></option>' + 
'               <option value="шт"></option>' + 
'       </datalist></div></div>');
        // Changing index
        i++;
        // Hide adding button if 30 ingredients was added
        if (i >= 30) {
            $(this).hide();
        }
    });
    
    $("#addTypes").click(function() {
        $(this).hide();
        var data = 'data=' + 1;
        $.ajax({
            method: "POST",
            url: "/add_recipe_types",
            data: data,
            cache: false,
            success: function(data){
                var text = '<label for="mealtype">Прием пищи</label>'+
                '<input list="mealtypes" name="mealtype" class="form-control" '+
                '    placeholder="Завтрак/Перекус/Обед/Полдник/Ужин/другое" value=""></input>'+
                '<datalist id="mealtypes">';
                for (let i=0; i<data['id'].length; i++){
                    if (data['recipe_type'][i] == 2){
                        text += '<option value="'+data['type'][i].charAt(0).toUpperCase()+data['type'][i].slice(1)+'"></option>';
                        data['id'].splice(i, 1);
                        data['recipe_type'].splice(i, 1);
                        data['type'].splice(i, 1);
                        i--;
                    }
                }
                text += '</datalist>'+
                '<label for="kitchentype">Кухня</label>'+
                '<input list="kitchentypes" name="kitchentype" class="form-control" '+
                '    placeholder="Русская/Украинская/Китайская/Французская/другое" value=""></input>'+
                '<datalist id="kitchentypes">';
                for (let i=0; i<data['id'].length; i++){
                    if (data['recipe_type'][i] == 3){
                        text += '<option value="'+data['type'][i].charAt(0).toUpperCase()+data['type'][i].slice(1)+'"></option>';
                        data['id'].splice(i, 1);
                        data['recipe_type'].splice(i, 1);
                        data['type'].splice(i, 1);
                        i--;
                    }
                }
                text += '</datalist>'+
                '<label for="othertype">Прочее</label>'+
                '<input list="othertypes" name="othertype" class="form-control" '+
                '    placeholder="Рыба/Мясо/Диетическое/другое" value=""></input>'+
                '<datalist id="othertypes">';
                for (let i=0; i<data['id'].length; i++){
                    if (data['recipe_type'][i] == 4){
                        text += '<option value="'+data['type'][i].charAt(0).toUpperCase()+data['type'][i].slice(1)+'"></option>';
                        data['id'].splice(i, 1);
                        data['recipe_type'].splice(i, 1);
                        data['type'].splice(i, 1);
                        i--;
                    }
                }
                
                $("#typesAdd").html(text);
            }
        });
    });

    let step=find_step_index();
    $("#addStep").click(function() {
        // Adding new fields for next step
        $("#stepAdd").append('<div class="form-group">' +
'        <label for="step_'+step+'">Шаг '+(step+1)+'</label>' +
'        <textarea name="step_'+step+'" class="form-control" placeholder="Что нужно сделать на '+(step+1)+' шаге?"></textarea>' +
'        </div>');
        // Changing index
        step++;
        // Hide adding button if 30 ingredients was added
        if (step >= 30) {
            $(this).hide();
        }
    });

    $('#add-additional-info').click(function() {
        $(this).hide();
        $('#additional-infoAdd').html('<div class="form-group"><label for="portions">Количество порций</label>'+
        '<input type="number" step="0.5" name="portions" placeholder="1"'+
        'class="form-control" value="1"></input></div>');
    });
});