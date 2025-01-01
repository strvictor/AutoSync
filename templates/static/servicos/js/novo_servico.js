document.addEventListener("DOMContentLoaded", function () {
    const clienteSelect = document.querySelector("#id_cliente");
    const carroSelect = document.querySelector("#id_carro");

    if (clienteSelect && carroSelect) {
        clienteSelect.addEventListener("change", function () {
            const clienteId = clienteSelect.value;

            // Faça a requisição para buscar os carros associados ao cliente selecionado
            fetch(`/servicos/carros-por-cliente/${clienteId}/`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                    // Limpa as opções do select de carros
                    carroSelect.innerHTML = '<option value="">Selecione um Veículo</option>';
                    data.carros.forEach((carro) => {
                        const option = document.createElement("option");
                        option.value = carro.id;
                        option.textContent = carro.nome; // Atualize conforme o campo relevante
                        carroSelect.appendChild(option);
                    });
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
    });
});