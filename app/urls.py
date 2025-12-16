from django.urls import path 
from .views import login , dashboard , deco , produitAdd , imprimer_code_barre
from . import views


app_name = 'app'


urlpatterns = [
    path('', views.home , name='home'),
    path('login/',login , name = 'login' ) , 
    path('dashboard/', dashboard , name= 'dashboard') , 
    path('deco/', deco , name='deco') ,
    path('produitAdd/' , produitAdd , name='produitAdd')  , 
    # Chemin pour enregistrer un nouveau produit
    path('nouveau/', views.enregistrer_produit, name='enregistrer_produit'),
    
    # Chemin pour simuler le scan et afficher le prix (recherche par code-barres)
    path('scan/', views.scanner_code_barre, name='scanner_code_barre'),
    
    # Chemin pour afficher le code-barres en vue d'impression
    path('produit/<int:produit_id>/imprimer/', imprimer_code_barre, name='imprimer_code_barre'),
    
    # Chemin d'accueil (optionnel)
    path('', views.liste_produits, name='liste_produits'),
]

