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
});
