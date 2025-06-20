from django.contrib import admin # type: ignore
from .models import Product

admin.site.register(Product)