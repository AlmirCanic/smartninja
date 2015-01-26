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
            $(wrapper).append('<div id="addedPrices">' +
                '<input type="text" name="price_dot" placeholder="Price with dot" class="pricedot"/> ' +
                '<input type="text" name="price_comma" placeholder="Price with comma" class="pricecomma"/> ' +
                '<input type="text" name="summary" placeholder="Summary" class="pricesummary"/> ' +
                '<a href="#" class="remove_field">Remove</a>' +
                '</div>'); //add input box
        }
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //user click on remove text
        e.preventDefault(); $(this).parent('div').remove(); x--;
    })

    addCourseButton.click(function() {
        var priceDotList = [];
        var priceCommaList = [];
        var priceSummaryList = [];

        $.each($(".pricedot"), function() {
            var priceDot = $(this).val();
            if (priceDot === "") {
                alert("Please fill all the Price with dot fields in Prices.");
                priceDotList.push("0.0");
            } else {
                priceDotList.push(priceDot);
            }
        });

        $.each($(".pricecomma"), function() {
            var priceComma = $(this).val();
            if (priceComma === "") {
                alert("Please fill all the Price with comma fields in Prices.");
                priceCommaList.push("0,00");
            } else {
                priceCommaList.push(priceComma);
            }
        });

        $.each($(".pricesummary"), function() {
            var priceSummary = $(this).val();
            if (priceSummary === "") {
                alert("Please fill all the Price summary fields in Prices.");
                priceSummaryList.push("Invalid price");
            } else {
                priceSummaryList.push(priceSummary);
            }
        });

        var allPricesData = "";

        for (var i = 0; i < priceDotList.length; i++) {
            var singlePriceData = priceDotList[i] + "|" + priceCommaList[i] + "|" + priceSummaryList[i] + "{}";
            allPricesData += singlePriceData;
        }

        //alert(allPricesData);

        $("#allPricesData").val(allPricesData);
    });
});