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
