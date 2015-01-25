/*
* Author: Saran Chamling
* Source: http://www.sanwebe.com/2013/03/addremove-input-fields-dynamically-with-jquery
* Modified by: Matej Ramuta
*/

$(document).ready(function() {
    var max_fields      = 10; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
    var addCourseButton      = $("#addCourseButton"); //Add button ID

    var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        e.preventDefault();
        if(x < max_fields){ //max input box allowed
            x++; //text box increment
            $(wrapper).append('<div id="addedPrices"><input type="text" name="price_dot" placeholder="Price with dot"/> <input type="text" name="price_comma" placeholder="Price with comma"/> <input type="text" name="summary" placeholder="Summary"/> <a href="#" class="remove_field">Remove</a></div>'); //add input box
        }
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })

    addCourseButton.click(function() {
        alert("test");
        var pricesList = [];
        $("#addedPrices").each(function() {
            var priceDot = $(this).children().first().val();
            alert(priceDot);
        });
    });
});