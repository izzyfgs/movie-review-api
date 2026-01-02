"""
WSGI config for movie_review_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
import os
import sys

# 1. This must be the folder containing manage.py
path = '/home/israelmalachy/movie-review-api'
if path not in sys.path:
    sys.path.insert(0, path)

# 2. This must be the folder containing settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'movie_review_api.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()