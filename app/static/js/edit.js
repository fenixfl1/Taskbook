$(document).ready(function() {

    var itemsTable = [];
    var itemsOrder = {};

    $('#btn-edit').on('click', function() {

        $('tbody tr').each(function(e) {
            $('#editSubjects').modal('show');
            var valores = $(this).find('#td');
            itemsOrder.name = valores.filter(':eq(0)').text();

            itemsTable.push(itemsOrder);
        });

        $('#studyPlan').on('show.bs.modal', function(e) {
            $('#name').value = $('td').val();
        });
    });
});