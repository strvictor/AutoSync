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
                    // Limpa as opções do select de carros
                    carroSelect.innerHTML = '<option value="">---------</option>';
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
