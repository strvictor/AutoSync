function atualiza_servico() {
    servicoId = document.getElementById("servico").value;
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value


    data = new FormData()
    data.append('servico_id', servicoId)

    fetch("/servicos/editar_servico/",{
        method: "POST",
        headers:{
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function(result){
        return result.json()
    }).then(function(data){

        console.log(data)
        
        console.log(data['valores'][0]['pk'])
        console.log(data['valores'][0]['fields']['titulo'])
        console.log(data['valores'][0]['fields']['cliente'])
        console.log(data['valores'][0]['fields']['carro'])
        console.log(data['valores'][0]['fields']['categoria_manutencao'])
        console.log(data['valores'][0]['fields']['data_inicio'])
        console.log(data['valores'][0]['fields']['data_entrega'])
        console.log(data['valores'][0]['fields']['finalizado'])

    })}
