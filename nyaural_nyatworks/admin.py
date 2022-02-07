from .models import *
from django.contrib import admin

admin.register(Report, Dataset, Preprocessor, Train)
