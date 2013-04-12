$(document).ready(function()
{
  $('input.datepicker').datepicker(
  {
    dateFormat : 'dd/mm/yy',
    changeMonth : true,
    changeYear : true,
    yearRange : '-100',
    maxDate: 0
  });
  $('input.datetimepicker').datetimepicker(
  {
    dateFormat : 'dd/mm/yy',
  });
  $(".thumbnail").colorbox(
  {
    photo : true,
    maxWidth : '100%',
    maxHeight : '100%',
    scalePhotos : true,
  });
  $('form').submit(function (e) {
      // $('form button').attr('disabled', "true");
      $(this).find('input[type=submit]').attr('disabled', "true");
  });
});
