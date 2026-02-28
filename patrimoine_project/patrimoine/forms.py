from django import forms
from django.core.exceptions import ValidationError
from .models import Bureau, Salle, Materiel


class BureauForm(forms.ModelForm):
    """
    Formulaire pour ajouter/modifier un bureau
    """

    class Meta:
        model = Bureau
        fields = [
            'type_bureau',
            'nom',
            'niveau',
            'surface',
            'capacite',
        ]
        widgets = {
            'type_bureau': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le type de bureau'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bureau 101, Open Space RDC'
            }),
            'niveau': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: RDC, 1er étage, -1 (sous-sol)'
            }),
            'surface': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 25.5',
                'step': '0.01',
                'min': '0.01'
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 4',
                'min': '1'
            }),
        }
        labels = {
            'type_bureau': 'Type de bureau',
            'nom': 'Nom du bureau',
            'niveau': 'Niveau / Étage',
            'surface': 'Surface (m²)',
            'capacite': 'Capacité (personnes)',
        }
        help_texts = {
            'type_bureau': 'Sélectionnez le type de configuration du bureau',
            'nom': 'Donnez un nom identifiable au bureau',
            'niveau': 'Indiquez l\'étage ou le niveau du bureau',
            'surface': 'Surface en mètres carrés',
            'capacite': 'Nombre maximum de personnes pouvant occuper le bureau',
        }

    def clean_surface(self):
        """Validation personnalisée pour la surface"""
        surface = self.cleaned_data.get('surface')
        if surface is not None and surface <= 0:
            raise ValidationError('La surface doit être supérieure à 0.')
        return surface

    def clean_capacite(self):
        """Validation personnalisée pour la capacité"""
        capacite = self.cleaned_data.get('capacite')
        if capacite is not None and capacite < 1:
            raise ValidationError('La capacité doit être au moins de 1 personne.')
        if capacite is not None and capacite > 100:
            raise ValidationError('La capacité semble trop élevée pour un bureau (maximum 100).')
        return capacite

    def clean(self):
        """Validation globale du formulaire"""
        cleaned_data = super().clean()
        surface = cleaned_data.get('surface')
        capacite = cleaned_data.get('capacite')

        # Vérifier la cohérence surface/capacité
        if surface and capacite:
            ratio = capacite / surface
            if ratio > 1:  # Plus d'1 personne par m²
                raise ValidationError(
                    f'La capacité ({capacite} personnes) semble trop élevée pour la surface ({surface} m²). '
                    f'Ratio actuel: {ratio:.2f} personnes/m².'
                )

        return cleaned_data


class SalleForm(forms.ModelForm):
    """
    Formulaire pour ajouter/modifier une salle
    """

    class Meta:
        model = Salle
        fields = [
            'type_salle',
            'nom',
            'niveau',
            'capacite',
            'surface',
            'equipements',
            'disponible',
            'picture',
        ]
        widgets = {
            'type_salle': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le type de salle'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Salle Atlantique, Salle de réunion A'
            }),
            'niveau': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2ème étage, RDC'
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 20',
                'min': '1',
                'max': '1000'
            }),
            'surface': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 45.5',
                'step': '0.01',
                'min': '0.01'
            }),
            'equipements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Projecteur, Tableau blanc, WiFi, Climatisation, Tables, Chaises...',
                'rows': 4
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'type_salle': 'Type de salle',
            'nom': 'Nom de la salle',
            'niveau': 'Niveau / Étage',
            'capacite': 'Capacité (personnes)',
            'surface': 'Surface (m²)',
            'equipements': 'Équipements disponibles',
            'disponible': 'Salle disponible',
            'picture': 'Photo de la salle',
        }
        help_texts = {
            'type_salle': 'Type d\'utilisation de la salle',
            'nom': 'Donnez un nom identifiable à la salle',
            'niveau': 'Indiquez l\'étage ou le niveau de la salle',
            'capacite': 'Nombre maximum de personnes',
            'surface': 'Surface en mètres carrés',
            'equipements': 'Listez tous les équipements disponibles (un par ligne ou séparés par des virgules)',
            'disponible': 'Cochez si la salle est actuellement disponible',
            'picture': 'Photo de la salle (formats acceptés: JPG, PNG, WebP)',
        }

    def clean_surface(self):
        """Validation personnalisée pour la surface"""
        surface = self.cleaned_data.get('surface')
        if surface is not None and surface <= 0:
            raise ValidationError('La surface doit être supérieure à 0.')
        if surface is not None and surface > 10000:
            raise ValidationError('La surface semble trop élevée (maximum 10000 m²).')
        return surface

    def clean_capacite(self):
        """Validation personnalisée pour la capacité"""
        capacite = self.cleaned_data.get('capacite')
        if capacite is not None and capacite < 1:
            raise ValidationError('La capacité doit être au moins de 1 personne.')
        return capacite

    def clean_picture(self):
        """Validation personnalisée pour l'image"""
        picture = self.cleaned_data.get('picture')
        if picture:
            # Vérifier la taille du fichier (max 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError('La taille de l\'image ne doit pas dépasser 5 MB.')

            # Vérifier le type de fichier
            if not picture.content_type.startswith('image/'):
                raise ValidationError('Le fichier doit être une image.')

        return picture

    def clean(self):
        """Validation globale du formulaire"""
        cleaned_data = super().clean()
        surface = cleaned_data.get('surface')
        capacite = cleaned_data.get('capacite')
        type_salle = cleaned_data.get('type_salle')

        # Vérifier la cohérence surface/capacité
        if surface and capacite:
            ratio = capacite / surface

            # Ratio recommandés selon le type de salle
            ratios_max = {
                'reunion': 0.5,  # 2 m² par personne
                'conference': 0.67,  # 1.5 m² par personne
                'pleniere': 1.0,  # 1 m² par personne
                'formation': 0.4,  # 2.5 m² par personne
            }

            max_ratio = ratios_max.get(type_salle, 0.5)

            if ratio > max_ratio:
                raise ValidationError(
                    f'Pour une {dict(Salle.TYPE_SALLE_CHOICES).get(type_salle)}, '
                    f'la capacité ({capacite} personnes) semble trop élevée pour la surface ({surface} m²). '
                    f'Ratio actuel: {ratio:.2f} personnes/m². Maximum recommandé: {max_ratio:.2f} personnes/m².'
                )

        return cleaned_data


class MaterielForm(forms.ModelForm):
    """
    Formulaire pour ajouter/modifier du matériel
    """

    class Meta:
        model = Materiel
        fields = [
            'salle',
            'bureau',
            'nom',
            'description',
            'quantite',
            'etat',
            'numero_serie',
            'date_acquisition',
            'prix_unitaire',
        ]
        widgets = {
            'salle': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez une salle'
            }),
            'bureau': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez un bureau'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Projecteur Epson, Ordinateur Dell'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description détaillée du matériel...',
                'rows': 3
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1',
                'min': '0'
            }),
            'etat': forms.Select(attrs={
                'class': 'form-control',
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SN123456789'
            }),
            'date_acquisition': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 5000000.00',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'salle': 'Salle',
            'bureau': 'Bureau',
            'nom': 'Nom du matériel',
            'description': 'Description',
            'quantite': 'Quantité',
            'etat': 'État',
            'numero_serie': 'Numéro de série',
            'date_acquisition': 'Date d\'acquisition',
            'prix_unitaire': 'Prix unitaire (GNF)',
        }
        help_texts = {
            'salle': 'Salle où se trouve le matériel (laisser vide si dans un bureau)',
            'bureau': 'Bureau où se trouve le matériel (laisser vide si dans une salle)',
            'nom': 'Nom ou désignation du matériel',
            'description': 'Description détaillée du matériel',
            'quantite': 'Nombre d\'unités de ce matériel',
            'etat': 'État actuel du matériel',
            'numero_serie': 'Numéro de série ou d\'inventaire',
            'date_acquisition': 'Date d\'achat ou d\'acquisition',
            'prix_unitaire': 'Prix d\'achat unitaire en Francs Guinéens',
        }

    def __init__(self, *args, **kwargs):
        """Personnalisation du formulaire"""
        super().__init__(*args, **kwargs)

        # Rendre salle et bureau optionnels dans le formulaire
        # mais la validation dans clean() s'assurera qu'au moins un est renseigné
        self.fields['salle'].required = False
        self.fields['bureau'].required = False

        # Ajouter des options vides pour les select
        self.fields['salle'].empty_label = "-- Sélectionner une salle --"
        self.fields['bureau'].empty_label = "-- Sélectionner un bureau --"

    def clean_quantite(self):
        """Validation personnalisée pour la quantité"""
        quantite = self.cleaned_data.get('quantite')
        if quantite is not None and quantite < 0:
            raise ValidationError('La quantité ne peut pas être négative.')
        if quantite is not None and quantite > 10000:
            raise ValidationError('La quantité semble trop élevée (maximum 10000).')
        return quantite

    def clean_prix_unitaire(self):
        """Validation personnalisée pour le prix unitaire"""
        prix_unitaire = self.cleaned_data.get('prix_unitaire')
        if prix_unitaire is not None and prix_unitaire < 0:
            raise ValidationError('Le prix unitaire ne peut pas être négatif.')
        return prix_unitaire

    def clean(self):
        """Validation globale du formulaire"""
        cleaned_data = super().clean()
        salle = cleaned_data.get('salle')
        bureau = cleaned_data.get('bureau')

        # Vérifier qu'au moins salle ou bureau est renseigné
        if not salle and not bureau:
            raise ValidationError(
                'Vous devez associer le matériel soit à une salle, soit à un bureau.'
            )

        # Vérifier qu'on ne peut pas associer à la fois à une salle et un bureau
        if salle and bureau:
            raise ValidationError(
                'Le matériel ne peut pas être associé à la fois à une salle et à un bureau. '
                'Veuillez choisir uniquement l\'un des deux.'
            )

        return cleaned_data


# ========== FORMULAIRES DE RECHERCHE / FILTRAGE ==========

class BureauSearchForm(forms.Form):
    """Formulaire de recherche pour les bureaux"""

    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un bureau...'
        })
    )
    type_bureau = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + Bureau.TYPE_BUREAU_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    niveau = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Niveau/Étage'
        })
    )


class SalleSearchForm(forms.Form):
    """Formulaire de recherche pour les salles"""

    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher une salle...'
        })
    )
    type_salle = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + Salle.TYPE_SALLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    disponible = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Toutes'),
            ('true', 'Disponibles uniquement'),
            ('false', 'Non disponibles uniquement')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    capacite_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Capacité minimum'
        })
    )


class MaterielSearchForm(forms.Form):
    """Formulaire de recherche pour le matériel"""

    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher du matériel...'
        })
    )
    etat = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les états')] + Materiel.ETAT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    localisation = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Toutes les localisations'),
            ('salle', 'Dans les salles'),
            ('bureau', 'Dans les bureaux')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )