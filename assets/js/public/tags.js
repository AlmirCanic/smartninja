$(document).ready(function(){

    $(".sometag").click(function() {
        var selected_tag = $(this).text();

        $(".somecourse").each(function() {
            var input_tag = $(this).find("input").val();

            var tags_list = input_tag.split(",");

            if(jQuery.inArray(selected_tag, tags_list) >= 0) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $("#allcourses").click(function() {
        $(".somecourse").each(function() {
            $(this).show();
        });
    });
});