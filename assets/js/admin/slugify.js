$(document).ready(function(){

    // SLUGIFY
    function slugify(text)
    {
        return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
    }

    function myFunc() {
        var title = $("#blogTitle").val();
        var ts = new Date().getTime();
        $("#blogSlug").val(slugify(title+" "+ts));
    }
    myFunc();

    $('#blogTitle').keyup(function(){
        myFunc();
    }).change(function(){
        myFunc(); //or direct assignment $('#txtHere').html($(this).val());
    });
});