$(document).ready(function ($) {
    $('input.datepicker').datepicker(
        {
            dateFormat: 'dd/mm/yy',
            changeMonth: true,
            changeYear: true,
            yearRange: '-100',
            maxDate: 0
        });
    $('input.datetimepicker').datetimepicker(
        {
            dateFormat: 'dd/mm/yy'
        });
    $('input.future-datepicker').datepicker(
        {
            dateFormat: 'dd/mm/yy',
            changeMonth: true,
            changeYear: true
        });
    $('.table').tablesorter();
    $('body').append('<div id="toTop" class="btn btn-info"><i class="fa fa-arrow-up"></i></div>');
    $(window).scroll(function () {
        if ($(this).scrollTop() != 0) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });
    $('#toTop').click(function () {
        $("html, body").animate({scrollTop: 0}, 600);
        return false;
    });
    $('select').select2({
        theme: "bootstrap"
    });
    $('.select2-container').css('width', '100%');
});
