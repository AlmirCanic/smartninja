$(document).ready(function() {
    var cd_first_name = $("#cd_first_name");
    var cd_last_name = $("#cd_last_name");
    var cd_email = $("#cd_email");
    var cd_address = $("#cd_address");
    var cd_phone = $("#cd_phone");
    var cd_price = $("#cd_price");
    var cd_submit = $("#cd_submit");

    $(cd_submit).click(function(e) {
        if(!cd_first_name.val()) {
            alert("Prosim napiši svoje ime.");
            e.preventDefault();
        } else if(!cd_last_name.val()) {
            alert("Prosim napiši svoj priimek.");
            e.preventDefault();
        } else if(!cd_email.val()) {
            alert("Prosim napiši svoj email naslov.");
            e.preventDefault();
        } else if(!cd_address.val()) {
            alert("Prosim napiši svoj naslov prebivališča.");
            e.preventDefault();
        } else if(!cd_phone.val()) {
            alert("Prosim napiši svojo telefonsko številko.");
            e.preventDefault();
        } else if(!cd_price.val()) {
            alert("Prosim izberi kotizacijo.");
            e.preventDefault();
        }
    });
});