from django.forms import ModelForm
from .models import Materiel, Salle, Bureau


class SalleForm(ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'


class BureauForm(ModelForm):
    class Meta:
        model = Bureau
        fields = '__all__'


class MaterielForm(ModelForm):
    class Meta:
        model = Materiel
        fields = '__all__'