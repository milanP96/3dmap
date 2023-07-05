from django.contrib.auth import get_user_model
from django.db import models


class Marker(models.Model):
    TYPES = (
        ("hiking", "hiking"),
        ("cycling", "cycling"),
        ("camping", "camping")
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    lng = models.FloatField(default=0)
    lat = models.FloatField(default=0)

    action_type = models.CharField(
        max_length=9,
        choices=TYPES,
        default="hiking",
        unique=True
    )
