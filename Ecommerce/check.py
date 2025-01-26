

# from django.contrib.auth.models import User  # Default Django User model
# for field in User._meta.get_fields():
#     print(field.name, field.get_internal_type())


import os
import django

# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce.settings")

# Initialize Django
django.setup()

# Now you can use Django models and settings
from django.contrib.auth.models import User
users = User.objects.all()
print(users)
