from django.db import models

# Create your models here.
class Staff(models.Model):
    class Meta:
        db_table = 'staff'
        ordering = ['pk']
        managed = False
        app_label = 'staff'

    name = models.TextField(max_length=255)
    initialies = models.TextField(max_length=20)
    email = models.TextField(blank=True, null=True)
    loginname = models.CharField(max_length=255)
    accessinvoice = models.BooleanField()
    accessstatistics = models.BooleanField()

    def __str__(self):
        return self.name