from django import forms 
from .models import Produit


class LoginForm(forms.Form) :
    
    username = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'class': 'form-control'}) ) 
    password = forms.CharField(max_length=200,  widget=forms.PasswordInput(attrs={'class': 'form-control'})) 

# ===================================
# produits



class ProduitForm(forms.ModelForm):
    """
    Formulaire utilisé pour l'enregistrement d'un nouveau produit.
    """
    class Meta:
        model = Produit
        # Nous n'incluons que les champs que l'utilisateur doit saisir manuellement.
        # 'barcode' et 'barcode_image' sont exclus car ils sont générés
        # automatiquement dans la méthode save() du modèle.
        fields = ['nom', 'prix']
        
        # Vous pouvez aussi définir des labels plus explicites
        labels = {
            'nom': 'Nom du Produit',
            'prix': 'Prix de Vente (FC)',
        }
        
        # Vous pouvez ajouter des widgets pour une meilleure expérience utilisateur
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control'}),
            'prix': forms.NumberInput(attrs={ 'class':'form-control'}),
        }

        # 'nom': forms.TextInput(attrs={'placeholder': 'Ex: T-shirt en coton bleu'}),