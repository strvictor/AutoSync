
// Gráfico de Distribuição de Serviços
const servicesCtx = document.getElementById('servicesChart').getContext('2d');
new Chart(servicesCtx, {
    type: 'doughnut',
    data: {
        labels: ['Pendentes', 'Finalizados'],
        datasets: [{
            data: [{{ total_pendentes }}, {{ total_finalizados }}],
            backgroundColor: ['#ffc107', '#28a745']
        }]
    }
});

// Gráfico de Receita
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
new Chart(revenueCtx, {
    type: 'bar',
    data: {
        labels: ['Pendentes', 'Finalizados'],
        datasets: [{
            label: 'Receita (R$)',
            data: [{{ total_valor_pendentes }}, {{ total_valor_finalizados }}],
            backgroundColor: ['#ffc107', '#28a745']
        }]
    }
});
