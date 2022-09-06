from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()

    class Meta:
        db_table = 'user'
        unique_together = (('username', 'email'),)

    def __str__(self) -> str:
        return f"{self.id} | {self.username} | {self.email}"
