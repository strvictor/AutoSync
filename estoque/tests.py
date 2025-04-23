estoque = 0

qtd_salva = 16
qtd_repassada = 17


if qtd_salva > qtd_repassada:
    diferenca = qtd_salva - qtd_repassada
    print(f'salvando no estoque: {diferenca}')
else:
    diferenca = qtd_repassada - qtd_salva
    print(f'retirando do estoque: {diferenca}')
