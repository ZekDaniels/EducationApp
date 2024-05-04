from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class BaseModelWithUser(BaseModel):
    created_by = models.ForeignKey('user.Profile', on_delete=models.CASCADE, related_name='%(class)s_created_by', null=True, blank=True)
    updated_by = models.ForeignKey('user.Profile', on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True, blank=True)

    class Meta:
        abstract = True