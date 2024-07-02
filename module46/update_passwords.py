import os
import django
from django.contrib.auth.hashers import make_password

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'module46.settings')
django.setup()

# Hash the password
raw_password = 'password9'  # Replace with the actual password you want to hash
hashed_password = make_password(raw_password)
print(hashed_password)
