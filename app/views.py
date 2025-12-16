from django.shortcuts import render , get_object_or_404  , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login as auth , logout 
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Produit
from .forms import ProduitForm
from django.urls import reverse


# ==============================
#
# home 
def home(request) :
    return render(request , 'front/index.html') 

# ===============================
#
# authetification 
def login(request):
    msg = None
    
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password'] 

            user = authenticate(username = username , password = password) 
            if user :
                auth(request,user) 
                return redirect(reverse('app:dashboard')) 
            else:
                msg = "mot de passe erronne !!!:🤞"
    

    form = LoginForm()

    return render(request , 'back/login.html', {"form":form , 'msg':msg}) 

# ===================================
#
# dashboard
@login_required()
def dashboard(request):
    return render(request, 'back/index.html')

 # ==================================
 # 
 # deconnexion
def deco(request):
    logout(request)
    return redirect(reverse('app:home'))

# ===================================
# 
# produit add 
@login_required()
def produitAdd(request):
    return render(request, 'back/form.html')

@login_required()
# --- A. ENREGISTREMENT ---
def enregistrer_produit(request):
    """
    Vue pour l'enregistrement d'un nouveau produit via formulaire.
    Le code-barres et l'image sont générés automatiquement par la méthode save() du modèle.
    """
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            produit = form.save()
            # Redirection vers la page d'impression après l'enregistrement
            return redirect('app:imprimer_code_barre', produit_id=produit.id)
    else:
        form = ProduitForm()
        
    context = {
        'form': form,
        'titre': "Enregistrer un nouveau produit"
    }
    return render(request, 'back/enregistrement_produit.html', context)

# --- B. SCAN / RECHERCHE DE PRIX ---
@login_required()
def scanner_code_barre(request):
    """
    Recherche un produit par son code-barres (code de 12 ou 13 chiffres) et affiche son prix.
    """
    produit = None
    prix = None
    # L'entrée est généralement un champ de formulaire ou un paramètre GET
    code_entree = request.GET.get('code_barre', '').strip() 

    if code_entree:
        try:
            # Pour la recherche, nous devons rechercher à la fois les 12 chiffres stockés 
            # ET le code complet de 13 chiffres généré à la volée.
            # On utilise F() pour comparer le code entré avec la valeur générée.
            
            # Recherche simple sur les 12 chiffres stockés
            if len(code_entree) == 12:
                produit = Produit.objects.get(barcode=code_entree)
            
            # Si l'utilisateur scanne les 13 chiffres (le code complet)
            elif len(code_entree) == 13:
                # Filtrer tous les produits et vérifier si le code complet correspond
                # C'est moins performant, mais garantit la recherche sur 13 chiffres.
                produits_candidats = Produit.objects.all()
                for p in produits_candidats:
                    if p.get_full_barcode() == code_entree:
                        produit = p
                        break
            
            if produit:
                prix = produit.prix
                message = f"Prix trouvé pour {produit.nom}."
            else:
                message = f"Aucun produit trouvé avec le code : {code_entree}"
                
        except Produit.DoesNotExist:
            message = f"Aucun produit trouvé avec le code : {code_entree}"
        
    context = {
        'produit': produit, 
        'prix': prix, 
        'code_entree': code_entree,
        'message': message if 'message' in locals() else "Veuillez scanner un code-barres."
    }
    return render(request, 'back/resultat_scan.html', context) 
    
# --- C. IMPRESSION ---
def imprimer_code_barre(request, produit_id):
    """
    Affiche le produit et son code-barres dans un format imprimable.
    """
    produit = get_object_or_404(Produit, pk=produit_id) 
    
    # 
    return render(request, 'back/imprimer_barcode.html', {'produit': produit})

# --- D. LISTE (Optionnel) ---
def liste_produits(request):
    """
    Affiche la liste de tous les produits.
    """
    produits = Produit.objects.all()
    return render(request, 'produits/liste_produits.html', {'produits': produits})
