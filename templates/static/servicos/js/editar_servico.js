function atualiza_servico() {
    const servicoId = document.getElementById('servico').value;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    const data = new FormData();
    data.append('servico_id', servicoId);

    fetch("/servicos/editar_servico/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        if (data.error) {
            alert(data.error);
            return;
        }

        const servico = data['valores'];

        document.getElementById('form-atualiza-servico').style.display = 'block';

        document.getElementById('id_servico').value = servico.id;
        document.getElementById('titulo').value = servico.titulo;
        document.getElementById('cliente').value = `${servico.cliente.nome} ${servico.cliente.sobrenome}`;
        document.getElementById('carro').value = `${servico.carro.carro} (${servico.carro.placa})`;
        document.getElementById('categoria_manutencao').value = servico.categorias.map(categoria => categoria.titulo).join(', ');
        document.getElementById('data_inicio').value = servico.data_inicio;
        document.getElementById('data_entrega').value = servico.data_entrega;
    });
}

document.getElementById('salvar-servico').addEventListener('click', function() {
    const servicoId = document.getElementById('id_servico').value;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    const data = new FormData();
    data.append('servico_id', servicoId);
    data.append('titulo', document.getElementById('titulo').value);
    data.append('cliente', document.getElementById('cliente').value);
    data.append('carro', document.getElementById('carro').value);
    data.append('categoria_manutencao', document.getElementById('categoria_manutencao').value);
    data.append('data_inicio', document.getElementById('data_inicio').value);
    data.append('data_entrega', document.getElementById('data_entrega').value);

    fetch("/servicos/atualiza_servico/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        alert('Serviço atualizado com sucesso!');
    }).catch(function(error) {
        console.error('Erro ao atualizar serviço:', error);
    });
});

$(document).ready(function () {
    $('.select-servico').select2({
        placeholder: 'Selecione um serviço',
        allowClear: true,
        minimumResultsForSearch: 4, // Mostra a barra de pesquisa sempre
        maximumInputLength: 20,    // Limita o número de caracteres que podem ser digitados
    });
});
