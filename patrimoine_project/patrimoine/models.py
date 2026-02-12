from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Bureau(models.Model):
    """
    Modèle représentant un bureau dans le patrimoine immobilier
    """
    TYPE_BUREAU_CHOICES = [
        ('box', 'Box office'),
        ('cloisonne', 'Cloisonné'),
        ('open', 'Open Office'),
        ('entier', 'Entier'),
    ]

    type_bureau = models.CharField(
        "Type de bureau",
        max_length=100,
        choices=TYPE_BUREAU_CHOICES
    )
    nom = models.CharField(
        "Nom",
        max_length=100,
        blank=True,  # Utiliser blank=True au lieu de null=True pour CharField
        default=""
    )
    niveau = models.CharField(
        "Niveau",
        max_length=100,
        blank=True,
        default="",
        help_text="Étage ou niveau du bureau"
    )
    # Champs supplémentaires recommandés
    surface = models.DecimalField(
        "Surface (m²)",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        help_text="Surface en mètres carrés"
    )
    capacite = models.IntegerField(
        "Capacité (personnes)",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Nombre de personnes pouvant occuper le bureau"
    )
    date_creation = models.DateTimeField(
        "Date de création",
        auto_now_add=True
    )
    date_modification = models.DateTimeField(
        "Date de modification",
        auto_now=True
    )

    def __str__(self):
        return self.nom if self.nom else f"Bureau {self.type_bureau}"

    class Meta:
        verbose_name = "Bureau"
        verbose_name_plural = "Bureaux"
        ordering = ['nom']


class Salle(models.Model):
    """
    Modèle représentant une salle dans le patrimoine immobilier
    """
    TYPE_SALLE_CHOICES = [
        ('reunion', 'Réunion'),
        ('conference', 'Conférence'),
        ('pleniere', 'Plénière'),
        ('formation', 'Formation'),  # Ajout d'un type supplémentaire
    ]

    type_salle = models.CharField(
        "Type de salle",
        max_length=100,
        choices=TYPE_SALLE_CHOICES
    )
    nom = models.CharField(
        "Nom",
        max_length=100,
        blank=True,
        default=""
    )
    niveau = models.CharField(
        "Niveau",
        max_length=100,
        blank=True,
        default="",
        help_text="Étage ou niveau de la salle"
    )
    capacite = models.IntegerField(
        "Capacité (personnes)",
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text="Nombre maximum de personnes"
    )
    surface = models.DecimalField(
        "Surface (m²)",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)],
        help_text="Surface en mètres carrés"
    )
    # Champs supplémentaires recommandés
    equipements = models.TextField(
        "Équipements",
        blank=True,
        default="",
        help_text="Liste des équipements disponibles"
    )
    disponible = models.BooleanField(
        "Disponible",
        default=True,
        help_text="Indique si la salle est disponible"
    )
    date_creation = models.DateTimeField(
        "Date de création",
        auto_now_add=True
    )
    date_modification = models.DateTimeField(
        "Date de modification",
        auto_now=True
    )

    def __str__(self):
        return self.nom if self.nom else f"Salle {self.type_salle}"

    def get_taux_occupation(self):
        """Retourne le taux d'occupation si surface et capacité sont définis"""
        if self.surface and self.capacite:
            return round(self.capacite / float(self.surface), 2)
        return None

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['nom']


class Materiel(models.Model):
    """
    Modèle représentant le matériel présent dans les salles et bureaux
    """
    ETAT_CHOICES = [
        ('bon', 'Bon état'),
        ('moyen', 'État moyen'),
        ('mauvais', 'Mauvais état'),
        ('hs', 'Hors service'),
        ('autre', 'Autre'),
    ]

    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='materiels',
        verbose_name="Salle",
        help_text="Salle où se trouve le matériel"
    )
    bureau = models.ForeignKey(
        Bureau,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='materiels',
        verbose_name="Bureau",
        help_text="Bureau où se trouve le matériel"
    )
    nom = models.CharField(
        "Nom du matériel",
        max_length=100,
        blank=True,
        default=""
    )
    description = models.TextField(
        "Description",
        blank=True,
        default="",
        help_text="Description détaillée du matériel"
    )
    quantite = models.IntegerField(
        "Quantité",
        default=1,
        validators=[MinValueValidator(0)],
        help_text="Nombre d'unités"
    )
    etat = models.CharField(
        "État",
        max_length=100,
        choices=ETAT_CHOICES,
        default='bon'
    )
    # Champs supplémentaires recommandés
    numero_serie = models.CharField(
        "Numéro de série",
        max_length=100,
        blank=True,
        default="",
        help_text="Numéro de série ou d'inventaire"
    )
    date_acquisition = models.DateField(
        "Date d'acquisition",
        null=True,
        blank=True
    )
    prix_unitaire = models.DecimalField(
        "Prix unitaire (€)",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Prix d'achat unitaire"
    )
    date_creation = models.DateTimeField(
        "Date de création",
        auto_now_add=True
    )
    date_modification = models.DateTimeField(
        "Date de modification",
        auto_now=True
    )

    def __str__(self):
        return self.nom if self.nom else f"Matériel #{self.id}"

    def clean(self):
        """Validation personnalisée"""
        from django.core.exceptions import ValidationError

        # Vérifier qu'au moins salle ou bureau est renseigné
        if not self.salle and not self.bureau:
            raise ValidationError(
                "Le matériel doit être associé soit à une salle, soit à un bureau."
            )

        # Vérifier qu'on ne peut pas associer à la fois à une salle et un bureau
        if self.salle and self.bureau:
            raise ValidationError(
                "Le matériel ne peut pas être associé à la fois à une salle et à un bureau."
            )

    def get_localisation(self):
        """Retourne la localisation du matériel"""
        if self.salle:
            return f"Salle: {self.salle.nom}"
        elif self.bureau:
            return f"Bureau: {self.bureau.nom}"
        return "Non localisé"

    def get_valeur_totale(self):
        """Calcule la valeur totale du matériel"""
        if self.prix_unitaire and self.quantite:
            return self.prix_unitaire * self.quantite
        return None

    class Meta:
        verbose_name = "Matériel"
        verbose_name_plural = "Matériels"
        ordering = ['nom']
        # Index pour améliorer les performances des requêtes
        indexes = [
            models.Index(fields=['salle']),
            models.Index(fields=['bureau']),
            models.Index(fields=['etat']),
        ]