from django.contrib import admin
from .models import Bureau, Salle, Materiel


admin.site.index_title = "Manager"
admin.site.site_header = "Gestion du patrimoine"


# Register your models here.
class AdminSalle(admin.ModelAdmin):
    list_display = ('nom', 'type_salle', 'niveau')
    search_fields = ['nom', 'type_salle', 'niveau']
admin.site.register(Salle, AdminSalle)


class AdminBureau(admin.ModelAdmin):
    list_display = ('nom', 'type_bureau', 'niveau')
    search_fields = ['nom', 'type_bureau', 'niveau']
admin.site.register(Bureau, AdminBureau)


class AdminMateriel(admin.ModelAdmin):
    list_display = ('salle','bureau','nom', 'etat','quantite')
    search_fields = ['salle','bureau','nom', 'etat','quantite']
admin.site.register(Materiel, AdminMateriel)

