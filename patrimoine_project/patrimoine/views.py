from django.shortcuts import render, get_object_or_404, redirect
from .models import Salle, Bureau, Materiel
from .forms import MaterielForm, SalleForm, BureauForm


# Create your views here.
def home(request):
    salles = Salle.objects.all()
    bureaux = Bureau.objects.all()
    materiels = Materiel.objects.all()
    context = {
        'salles': salles,'bureaux': bureaux,'materiels': materiels,
        }
    return render(request, 'patrimoine/home.html', context)


# --------------  salle ------------------------

def add_salle(request):
    """Ajout"""
    if request.method == 'POST':
        form = SalleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_salle')
    else:
        form = SalleForm()
    return render(request, 'patrimoine/add_salle.html', {'form': form})


def list_salle(request):
    '''Liste'''
    salles = Salle.objects.all()
    """Liste des salles avec recherche"""
    search_query = request.GET.get('search', '')

    if search_query:
        salles = salles.filter(
            Q(nom__icontains=search_query) |
            Q(niveau__icontains=search_query) |
            Q(type_salle__icontains=search_query)

        )
    salles = salles.order_by('niveau')

    context = { 'salles': salles, }
    return render(request, 'patrimoine/list_salle.html', context)


def detail_salle(request, pk):
    """Détail"""
    salle = get_object_or_404(Salle, id=pk)
    materiels = salle.materiels_set.all()
    context = { 'salle': salle, 'materiels': materiels, }
    return render(request, 'patrimoine/detail_salle.html', context)


def update_salle(request, pk):
    """Modification"""
    materiel = get_object_or_404(Materiel, id=pk)
    if request.method == 'POST':
        form = MaterielForm(request.POST, request.FILES, instance=materiel)
        if form.is_valid():
            form.save()
            return redirect('list_salle')
    else:
        form = MaterielForm(instance=materiel)
    context = { 'form': form, 'materiel': materiel, }
    return render(request, 'patrimoine/update_salle.html', context)


def delete_salle(request, pk):
    """Suppression d'une salle"""
    salle = get_object_or_404(Salle, id=pk)
    if request.method == 'POST':
        salle.delete()
        return redirect('list_salle',)
    context = { 'salle': salle, }
    return render(request, 'patrimoine/delete_salle.html', context)


# --------------  Bureau ------------------------

def add_bureau(request):
    """Ajout"""
    if request.method == 'POST':
        form = BureauForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_bureau')
    else:
        form = BureauForm()
    return render(request, 'patrimoine/add_bureau.html', {'form': form})


def list_bureau(request):
    """Liste"""
    bureaux = Bureau.objects.all()
    context = { 'bureaux': bureaux, }
    return render(request, 'patrimoine/list_bureau.html', context)


def detail_bureau(request, pk):
    """Détail"""
    bureau = get_object_or_404(Bureau, id=pk)
    materiels = bureau.materiels_set.all()
    context = { 'bureau': bureau, 'materiels': materiels, }
    return render(request, 'patrimoine/detail_salle.html', context)


def update_bureau(request, pk):
    """Modification"""
    bureau = get_object_or_404(Bureau, id=pk)
    if request.method == 'POST':
        form = BureauForm(request.POST, request.FILES, instance=bureau)
        if form.is_valid():
            form.save()
            return redirect('list_bureau')
    else:
        form = BureauForm(instance=bureau)
    context = { 'form': form, 'bureau': bureau, }
    return render(request, 'patrimoine/update_bureau.html', context)


def delete_bureau(request, pk):
    """Suppression d'une salle"""
    bureau = get_object_or_404(Bureau, id=pk)
    if request.method == 'POST':
        bureau.delete()
        return redirect('list_bureau',)
    context = { 'bureau': bureau, }
    return render(request, 'patrimoine/delete_bureau.html', context)


# -------------- Matériel ------------------------

def add_materiel(request):
    """Ajout"""
    if request.method == 'POST':
        form = MaterielForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_materiel')
    else:
        form = MaterielForm()
    return render(request, 'patrimoine/add_materiel.html', {'form': form})


def list_materiel(request):
    """Liste"""
    materiels = Materiel.objects.all()
    context = { 'materiels': materiels, }
    return render(request, 'patrimoine/list_materiel.html', context)


def detail_materiel(request, pk):
    """Détail"""
    materiel = get_object_or_404(Materiel, id=pk)
    context = { 'materiel': materiel, }
    return render(request, 'patrimoine/detail_materiel.html', context)


def update_materiel(request, pk):
    """Modification"""
    materiel = get_object_or_404(Materiel, id=pk)
    if request.method == 'POST':
        form = MaterielForm(request.POST, request.FILES, instance=materiel)
        if form.is_valid():
            form.save()
            return redirect('list_materiel')
    else:
        form = MaterielForm(instance=materiel)
    context = { 'form': form, 'materiel': materiel, }
    return render(request, 'patrimoine/update_materiel.html', context)


def delete_materiel(request, pk):
    """Suppression"""
    materiel = get_object_or_404(Materiel, id=pk)
    if request.method == 'POST':
        materiel.delete()
        return redirect('list_materiel',)
    context = { 'materiel': materiel, }
    return render(request, 'patrimoine/delete_materiel.html', context)



# -------------------------------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Bureau, Salle, Materiel
from .forms import BureauForm, SalleForm, MaterielForm



from django.db.models import Sum, Count, Avg
from django.shortcuts import render
from .models import Bureau, Salle, Materiel


def dashboard(request):
    # ===== BUREAUX =====
    total_bureaux = Bureau.objects.count()
    surface_totale_bureaux = Bureau.objects.aggregate(Sum('surface'))['surface__sum'] or 0
    capacite_totale_bureaux = Bureau.objects.aggregate(Sum('capacite'))['capacite__sum'] or 0

    # ===== SALLES =====
    total_salles = Salle.objects.count()
    salles_disponibles = Salle.objects.filter(disponible=True).count()
    surface_totale_salles = Salle.objects.aggregate(Sum('surface'))['surface__sum'] or 0
    capacite_totale_salles = Salle.objects.aggregate(Sum('capacite'))['capacite__sum'] or 0

    # Moyenne taux occupation
    salles_avec_surface = Salle.objects.exclude(surface=None).exclude(capacite=None)
    taux_moyen = None
    if salles_avec_surface.exists():
        taux_list = [
            salle.capacite / float(salle.surface)
            for salle in salles_avec_surface
        ]
        taux_moyen = round(sum(taux_list) / len(taux_list), 2)

    # ===== MATERIEL =====
    total_materiel = Materiel.objects.count()
    valeur_totale = 0
    for m in Materiel.objects.all():
        if m.get_valeur_totale():
            valeur_totale += m.get_valeur_totale()

    # Répartition par état
    repartition_etat = Materiel.objects.values('etat').annotate(total=Count('etat'))

    context = {
        'total_bureaux': total_bureaux,
        'surface_totale_bureaux': surface_totale_bureaux,
        'capacite_totale_bureaux': capacite_totale_bureaux,

        'total_salles': total_salles,
        'salles_disponibles': salles_disponibles,
        'surface_totale_salles': surface_totale_salles,
        'capacite_totale_salles': capacite_totale_salles,
        'taux_moyen': taux_moyen,

        'total_materiel': total_materiel,
        'valeur_totale': valeur_totale,
        'repartition_etat': repartition_etat,
    }

    return render(request, 'dashboard.html', context)

# ==============================
# ======== BUREAU ==============
# ==============================

def bureau_list(request):
    bureaux = Bureau.objects.all()
    return render(request, 'bureaux/bureau_list.html', {'bureaux': bureaux})


def bureau_detail(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    return render(request, 'bureaux/bureau_detail.html', {'bureau': bureau})


def bureau_create(request):
    if request.method == 'POST':
        form = BureauForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bureau créé avec succès.")
            return redirect('bureau_list')
    else:
        form = BureauForm()
    return render(request, 'bureaux/bureau_form.html', {'form': form})


def bureau_update(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    if request.method == 'POST':
        form = BureauForm(request.POST, instance=bureau)
        if form.is_valid():
            form.save()
            messages.success(request, "Bureau modifié avec succès.")
            return redirect('bureau_detail', pk=pk)
    else:
        form = BureauForm(instance=bureau)
    return render(request, 'bureaux/bureau_form.html', {'form': form})


def bureau_delete(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    if request.method == 'POST':
        bureau.delete()
        messages.success(request, "Bureau supprimé avec succès.")
        return redirect('bureau_list')
    return render(request, 'bureaux/bureau_confirm_delete.html', {'bureau': bureau})


# ==============================
# ========= SALLE ==============
# ==============================

def salle_list(request):
    salles = Salle.objects.all()
    return render(request, 'salles/salle_list.html', {'salles': salles})


def salle_detail(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    return render(request, 'salles/salle_detail.html', {'salle': salle})


def salle_create(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle créée avec succès.")
            return redirect('salle_list')
    else:
        form = SalleForm()
    return render(request, 'salles/salle_form.html', {'form': form})


def salle_update(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            messages.success(request, "Salle modifiée avec succès.")
            return redirect('salle_detail', pk=pk)
    else:
        form = SalleForm(instance=salle)
    return render(request, 'salles/salle_form.html', {'form': form})


def salle_delete(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        salle.delete()
        messages.success(request, "Salle supprimée avec succès.")
        return redirect('salle_list')
    return render(request, 'salles/salle_confirm_delete.html', {'salle': salle})


# ==============================
# ========= MATERIEL ===========
# ==============================

def materiel_list(request):
    materiels = Materiel.objects.select_related('salle', 'bureau').all()
    return render(request, 'materiels/materiel_list.html', {'materiels': materiels})


def materiel_detail(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    return render(request, 'materiels/materiel_detail.html', {'materiel': materiel})


def materiel_create(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matériel créé avec succès.")
            return redirect('materiel_list')
    else:
        form = MaterielForm()
    return render(request, 'materiels/materiel_form.html', {'form': form})


def materiel_update(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == 'POST':
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
            form.save()
            messages.success(request, "Matériel modifié avec succès.")
            return redirect('materiel_detail', pk=pk)
    else:
        form = MaterielForm(instance=materiel)
    return render(request, 'materiels/materiel_form.html', {'form': form})


def materiel_delete(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == 'POST':
        materiel.delete()
        messages.success(request, "Matériel supprimé avec succès.")
        return redirect('materiel_list')
    return render(request, 'materiels/materiel_confirm_delete.html', {'materiel': materiel})

