$(document).ready(function() {

  $('#table').DataTable({
    searching: false,
    lengthChange: false,
    ordering: false,
    lengthMenu: [8],
    "info": false
  });

  var $rows = $('#table tr');
  $('#search').keyup(function() {

      var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
          reg = RegExp(val, 'i'),
          text;

      $rows.show().filter(function() {
          text = $(this).text().replace(/\s+/g, ' ');
          return !reg.test(text);
      }).hide();
  });
});