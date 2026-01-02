"""
WSGI config for movie_review_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
import os
import sys

# Add your project directory to the sys.path (at the beginning!)
path = '/home/israelmalachy/movie-review-api'  # ← this is correct based on your find command
if path not in sys.path:
    sys.path.insert(0, path)  # ← changed from append() to insert(0, ...)

os.environ['DJANGO_SETTINGS_MODULE'] = 'movie_review_api.settings'  # ← underscore, correct inner folder

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()