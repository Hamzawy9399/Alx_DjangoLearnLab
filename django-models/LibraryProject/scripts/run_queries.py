# scripts/run_queries.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.query_samples import run_all

if __name__ == '__main__':
    run_all()
