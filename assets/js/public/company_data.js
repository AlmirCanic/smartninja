$(document).ready(function() {
    var companyData = $("#company-data");

    companyData.hide();

    $("#company-invoice").change(function() {
        if(this.checked) {
            companyData.show();
        } else {
            companyData.hide();
        }
    });
});