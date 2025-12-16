"""
WSGI config for conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Cette ligne indique à Django quel fichier de paramètres (settings.py) utiliser.
# 'conf.settings' pointe vers le fichier settings.py dans le dossier 'conf'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Cette variable 'application' est le point d'entrée que le serveur de production
# (comme Gunicorn) utilise pour lancer votre application Django.
application = get_wsgi_application()