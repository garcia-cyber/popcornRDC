from django.contrib import admin
from .models import Produit

# Register your models here
# 
# .

class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    list_display = ['nom', 'prix','date_creation']
admin.site.register(Produit, ProduitAdmin)