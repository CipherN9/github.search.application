from django.db import models

class SearchType(models.TextChoices):
    USERS        = 'users',        'Users'
    REPOSITORIES = 'repositories', 'Repositories'

