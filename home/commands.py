from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from servicos.models import Servicos

# Agrupando por mês e somando o valor total dos serviços finalizados
servicos_por_mes = (
    Servicos.objects.filter(status="Finalizado")
    .annotate(mes=TruncMonth('data_finalizacao'))  # Agrupa por mês
    .annotate(  # Calcula o valor total para cada serviço
        valor_total=ExpressionWrapper(
            F('servicocategoriaquantidade__quantidade') * F('servicocategoriaquantidade__categoria__preco'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    .values('mes')
    .annotate(total_valor=Sum('valor_total'))  # Soma o valor total de todos os serviços no mês
    .order_by('mes')
)

print(servicos_por_mes)

for servico in servicos_por_mes:
    print(f"Mês: {servico['mes']}, Valor Total: R$ {servico['total_valor']:.2f}")
