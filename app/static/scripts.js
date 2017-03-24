$(document).ready(function(){
    $('#add_department').click(function(e) {
        $("#department_form").toggle();
        e.stopPropagation();
    });

    $('body').click(function(e) {
        popup = $('.popup').css('display');
        if ((popup != 'none') && (e.target.class == "popup" || $(e.target).parents(".popup").size())) {
            $('.popup').toggle();
        }
    });
});