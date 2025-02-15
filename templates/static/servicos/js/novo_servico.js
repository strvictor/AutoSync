document.addEventListener("DOMContentLoaded", function () {
    const clienteSelect = document.querySelector("#id_cliente");
    const carroSelect = document.querySelector("#id_carro");

    if (clienteSelect && carroSelect) {
        // Inicializa o Select2 nos selects
        $(clienteSelect).select2();
        $(carroSelect).select2();

        // Usa o evento específico do Select2
        $(clienteSelect).on("select2:select", function () {
            const clienteId = $(this).val(); // Obtém o valor selecionado

            // Faz a requisição para buscar os carros associados ao cliente selecionado
            fetch(`/servicos/carros-por-cliente/${clienteId}/`)
                .then((response) => response.json())
                .then((data) => {
                    // Limpa as opções do select de carros
                    $(carroSelect).empty().append(new Option("Selecione um Veículo", ""));

                    // Adiciona as novas opções
                    data.carros.forEach((carro) => {
                        const option = new Option(carro.nome, carro.id, false, false); // Texto e valor
                        $(carroSelect).append(option);
                    });

                    // Atualiza o Select2 para refletir as novas opções
                    $(carroSelect).trigger("change");
                })
                .catch((error) => {
                    console.error("Erro ao buscar carros:", error);
                });
        });
    }
});

$(document).ready(function () {
    $('#add-categoria').on('click', function () {
        // Duplica o primeiro elemento com a classe 'categoria-row'
        const newField = $('.categoria-row:first').clone();

        // Remove IDs duplicados e cria novos IDs únicos
        newField.find('[id]').each(function () {
            const originalId = $(this).attr('id');
            const newId = originalId + '_' + ($('.categoria-row').length + 1);
            $(this).attr('id', newId);
        });

        // Limpa os valores dos campos clonados
        newField.find('input, select').val('');

        // Remove a instância existente do Select2 no campo clonado
        newField.find('.select2').remove();

        // Adiciona o novo campo ao container
        $('#categorias-container').append(newField);

        // Inicializa o Select2 no novo campo
        const selectElement = newField.find('select');
        selectElement.select2({
            placeholder: 'Selecione um serviço',
            allowClear: true,
            minimumResultsForSearch: 4,
            maximumInputLength: 20,
        });

        // Garante que o Select2 tenha a largura correta
        selectElement.next('.select2-container').css('width', '100%');
    });

    // Inicializa o Select2 para os campos já existentes na página
    $('.categoria-row select').select2({
        placeholder: 'Selecione um serviço',
        allowClear: true,
        minimumResultsForSearch: 4,
        maximumInputLength: 20,
        width: 'resolve', // Ajusta a largura com base no elemento pai
    });
});


$(document).ready(function () {
    $('#categorias').select2({
        placeholder: 'Selecione um serviço',
        allowClear: true,
        minimumResultsForSearch: 4, // Mostra a barra de pesquisa sempre
        maximumInputLength: 20,    // Limita o número de caracteres que podem ser digitados
        dropdownCssClass: 'custom-dropdown',
        selectionCssClass: 'custom-selection',
    });
});

$(document).ready(function () {
    $('.select-cliente').select2({
        placeholder: 'Selecione um cliente',
        allowClear: true,
        minimumResultsForSearch: 4, // Mostra a barra de pesquisa sempre
        maximumInputLength: 20,    // Limita o número de caracteres que podem ser digitados
    });
});


function remover_servico(event) {
    console.log('Removendo serviço...');
    // Get the button that was clicked
    const button = event.target;
    // Find the closest row (categoria-row)
    var row = button.closest('.categoria-row');
    // Check if there is more than one row
    if ($('.categoria-row').length > 1) {
        // Remove the row
        row.remove();
    } else {
        alert('Você deve ter pelo menos uma categoria.');
    }
};