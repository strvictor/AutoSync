$(document).ready(function () {
    $('.select-cliente').select2({
        placeholder: 'Selecione um cliente',
        allowClear: true,
        minimumResultsForSearch: 4, // Mostra a barra de pesquisa sempre
        maximumInputLength: 20,    // Limita o número de caracteres que podem ser digitados
    });
});

function add_carro() {
    const container = document.getElementById("form-carro");

    const id = `carro-${Date.now()}`; // Gera um ID único para cada linha
    const html = `
        <br id="br-${id}">
        <div class="row" id="${id}">
            <div class="col-md">
                <input type="text" placeholder="Veículo" class="form-control" name="carro" required>
            </div>
            <div class="col-md">
                <input type="text" placeholder="Placa" class="form-control" name="placa" required>
            </div>
            <div class="col-md">
                <input type="text" placeholder="Ano" class="form-control" name="ano" required>
            </div>
            <div class="col-md-auto">
                <button type="button" class="btn btn-danger" onclick="remove_carro('${id}')">X</button>
            </div>
        </div>
    `;

    container.innerHTML += html;
}

function remove_carro(id) {
    const carroElement = document.getElementById(id);
    const brElement = document.getElementById(`br-${id}`);
    if (carroElement) carroElement.remove();
    if (brElement) brElement.remove();
}

function exibir_form(tipo){
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('atualizar_cliente')

    if (tipo == '1'){
        att_cliente.style.display = 'none'
        add_cliente.style.display = 'block'
        
    } else if(tipo == '2'){
        att_cliente.style.display = 'block'
        add_cliente.style.display = 'none'
    }
}

function dados_clientes() {
    id_cliente = document.getElementById('cliente-select').value
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){

        id_cliente_front = document.getElementById('id_cliente')
        id_cliente_front.value = id_cliente
  
        document.getElementById('form-atualiza-cliente').style.display = 'block'
        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ''
        if (data['carros'].length > 0) {
            for (i = 0; i < data['carros'].length; i++) {
                id_carro = data['carros'][i]['id']
                carro = data['carros'][i]['fields']['carro']
                placa = data['carros'][i]['fields']['placa']
                ano = data['carros'][i]['fields']['ano']

                div_carros.innerHTML += `
                <form action='atualiza_carro/${id_carro}' method='POST'>
                    <div class='row'>
                        <div class='col-md'>
                            <p>Nome:</p>
                            <input type='text' name='carro' class='form-control' value='${carro}'>
                        </div>
                        <div class='col-md'>
                            <p>Placa:</p>
                            <input type='text' name='placa' class='form-control' value='${placa}'>
                        </div>
                        <div class='col-md'>
                            <p>Ano:</p>
                            <input type='text' name='ano' class='form-control' value='${ano}'>
                        </div>
                        <div class='col-md'>
                            <p>Ação:</p>
                            <input type='submit' class='btn btn-success' value='Atualizar Carro'>
                        </div>
                    </div>
                </form>
                <br>
            `;
            }
        } else {
            div_carros.innerHTML = `
                <form id="novo-carro-form" method="POST" action="/clientes/salva_carro/">
                <h6>Cadastre um veículo:</h6>
                    <div class="row">
                        <div class="col-md">
                            <p>Veículo:</p>
                            <input type="text" name="carro" class="form-control" placeholder="Digite o nome do veículo" required>
                        </div>
                        <div class="col-md">
                            <p>Placa:</p>
                            <input type="text" name="placa" class="form-control" placeholder="Digite a placa" required>
                        </div>
                        <div class="col-md">
                            <p>Ano:</p>
                            <input type="text" name="ano" class="form-control" placeholder="Digite o ano" required>
                        </div>
                        <input type="hidden" name="id_cliente" class="form-control" value="${id_cliente}">
                        <div class="col-md">
                            <p>Ação:</p>
                            <button type="button" id="adicionar-carro" class="btn btn-primary">Adicionar Carro</button>
                        </div>
                    </div>
                </form>
                <br>
            `;

            document.getElementById('adicionar-carro').addEventListener('click', function() {
                const novoCarroForm = document.getElementById('novo-carro-form');
                const novoCarroData = new FormData(novoCarroForm);

                fetch("/clientes/salva_carro/", {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrf_token,
                    },
                    body: novoCarroData
                }).then(response => response.json()).then(result => {
                    if (result.success) {
                        alert('Carro adicionado com sucesso!');
                        dados_clientes(); // Atualiza os dados do cliente
                    } else {
                        alert('Erro ao adicionar o carro.');
                    }
                });
            });
        }
    })
}

function update_cliente() {
    id = document.getElementById('id_cliente').value
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value

    fetch('/clientes/update_cliente/' + id,{
        method: 'POST',
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
        })

    }).then(function(result){
        return result.json
    }).then(function(data){

        console.log(data)
    })
}