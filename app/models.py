from django.db import models
from django.utils.crypto import get_random_string
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import os # Nécessaire pour les chemins si non importé

class Produit(models.Model):
    """
    Modèle pour représenter un produit avec un code-barres et son image.
    """
    nom = models.CharField(
        max_length=255, 
        verbose_name="Nom du produit"
    )
    prix = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Prix (HT ou TTC)"
    )
    # Nous stockons les 12 chiffres de données (EAN-13 est 12 + 1 checksum)
    barcode = models.CharField(
        max_length=12,  # Changé à 12 pour la conformité EAN-13
        unique=True, 
        blank=True, 
        null=True,
        verbose_name="Code-barres (12 chiffres de données)"
    )
    barcode_image = models.ImageField(
        upload_to='barcodes/', 
        blank=True, 
        null=True,
        verbose_name="Image du code-barres"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Date de création"
    )

    def generate_unique_barcode(self):
        """
        Génère une chaîne aléatoire de 12 chiffres (données EAN-13).
        """
        length = 12 
        return get_random_string(length=length, allowed_chars='0123456789')

    def generate_barcode_image(self):
        """
        Génère l'image du code-barres à l'aide de python-barcode (EAN-13).
        """
        if not self.barcode:
            # Sécurité: Ne devrait pas arriver si save() est bien exécuté
            raise ValueError("Le produit doit avoir un code-barres numérique défini avant de générer l'image.")
        
        # Le code-barres doit être de 12 chiffres pour EAN13
        EAN = barcode.get_barcode_class('ean13')
        
        # Créer l'objet code-barres. EAN() va calculer le 13ème chiffre (checksum)
        ean = EAN(self.barcode, writer=ImageWriter()) 

        # Créer un objet BytesIO pour stocker l'image en mémoire
        buffer = BytesIO()
        
        # Écrire l'image dans le buffer
        ean.write(buffer)
        
        # Préparer le fichier Django pour le stockage
        filename = f'{self.barcode}.png'
        file_buffer = File(buffer, name=filename)
        
        # Mettre à jour le champ ImageField (save=False pour le sauver dans la 2e save)
        self.barcode_image.save(filename, file_buffer, save=False)
        return self.barcode_image

    def save(self, *args, **kwargs):
        """
        1. Génère le code-barres numérique s'il n'existe pas.
        2. Sauvegarde l'objet pour obtenir un PK (nécessaire pour les fichiers).
        3. Génère et sauvegarde l'image du code-barres.
        """
        is_new = self.pk is None
        
        # ÉTAPE 1: Générer le numéro de code-barres s'il est manquant
        if not self.barcode:
            new_barcode = self.generate_unique_barcode()
            while Produit.objects.filter(barcode=new_barcode).exists():
                new_barcode = self.generate_unique_barcode()
            self.barcode = new_barcode   
            
        # ÉTAPE 2: Sauvegarder l'objet initialement
        super().save(*args, **kwargs)
        
        # ÉTAPE 3: Générer et sauvegarder l'image si c'est nouveau ou manquant
        # On vérifie is_new ET s'il n'y a pas déjà d'image
        if is_new or not self.barcode_image:
             self.generate_barcode_image()
             # Sauvegarder à nouveau, cette fois pour enregistrer l'ImageField
             super().save(update_fields=['barcode_image']) 

    def get_full_barcode(self):
        """ Renvoie le code-barres complet de 13 chiffres (12 + checksum). """
        EAN = barcode.get_barcode_class('ean13')
        return EAN(self.barcode).get_fullcode()

    def __str__(self):
        return f"{self.nom} (Code: {self.get_full_barcode()})"

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']