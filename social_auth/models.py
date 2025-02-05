from django.db import models

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This makes it an abstract model (no table is created)
        db_table = 'base_model'  # Custom table name for metadata purposes

class SocialUser(BaseModel):
    email = models.EmailField(primary_key=True, unique=True)

    class Meta:
        db_table = 'social_user'  # Custom table name

    def __str__(self):
        return self.email
