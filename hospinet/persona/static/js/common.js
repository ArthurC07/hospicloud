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
});
$(document).delegate('a, :button', 'click', function(e) {
    var lastClicked = $.data(this, 'lastClicked'),
        now = new Date().getTime();

    if (lastClicked && (now - lastClicked < 1000)) {
        e.preventDefault();
    } else {
        $.data(this, 'lastClicked', now);
    }
});
