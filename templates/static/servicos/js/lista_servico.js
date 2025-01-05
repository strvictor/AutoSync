
// document.getElementById('searchInput').addEventListener('keyup', function () {
//     let input = document.getElementById('searchInput').value.toLowerCase();
//     let rows = document.querySelectorAll('tbody tr');
    
//     rows.forEach(row => {
//         let text = row.textContent.toLowerCase();
//         if (text.includes(input)) {
//             row.style.display = ''; // Mostra a linha
//         } else {
//             row.style.display = 'none'; // Esconde a linha
//         }
//     });
// });

$(document).ready(function() {
    $('.table').DataTable({
        "processing": true,
        "pageLength": 10,
        "paging": true,
        // "pagingType": "first_last_numbers",
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" + 
               "<'row'<'col-sm-12'tr>>" + 
               "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        "language": {
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "Nada encontrado!",
            "info": "Mostrando página _PAGE_ de _PAGES_",
            "infoEmpty": "Nenhum registro disponível",
            "infoFiltered": "(filtrado de _MAX_ registros no total)",
            "search": "",
            "paginate": {
                "first": "Primeiro",
                "last": "Último",
                "next": "Próximo",
                "previous": "Anterior"
            }
        },
        "initComplete": function() {
            // Adiciona o placeholder no campo de busca
            const searchBox = $('div.dataTables_filter input');
            searchBox.attr('placeholder', 'O que deseja buscar?');
        }
        
    });
});