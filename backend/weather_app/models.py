from django.db import models


class Location(models.Model):
    user_identifier = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    weather_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
