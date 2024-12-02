from django.forms import ModelForm
from .models import Servicos, Carro, CategoriaManutencao
from django import forms

class ServicosForm(forms.ModelForm):
    class Meta:
        model = Servicos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verifica se o cliente está definido na instância
        if self.instance and self.instance.cliente:
            # Filtra os carros associados ao cliente
            self.fields['carro'].queryset = Carro.objects.filter(cliente=self.instance.cliente)
        else:
            # Exibe nenhum carro caso o cliente não esteja definido
            self.fields['carro'].queryset = Carro.objects.none()

class FormServico(ModelForm):
    class Meta:
        model = Servicos
        fields = "__all__"