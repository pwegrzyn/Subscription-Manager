from django.db import models
from django.utils import timezone

# Create your models here.


# Represents a custom Subscription Plan made by the user
class SubscriptionPlan(models.Model):

    name = models.CharField(max_length=128)
    planned_budget = models.IntegerField()
    planned_amount = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Plans"


# Represents meta data about a subscription (used for recommendations)
class Tag(models.Model):

    name = models.CharField(max_length=128)
    occurance = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tag Set"


# Represents a particular subscription submitted by the user
class Subscription(models.Model):

    service_name = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    start_time = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(default=30)
    notes = models.TextField(blank=True, default='')
    price = models.IntegerField()
    recurring = models.BooleanField(default=False)
    was_cancelled = models.BooleanField(default=False)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, default=None, blank=True, null=True) # noqa E501
    tags = models.CharField(max_length=512, blank=True, default='') # noqa E501
    personal_rating = models.IntegerField(default=0)  # 0 - 100

    def __str__(self):
        return '{} - {}'.format(self.service_name, self.start_time)

    class Meta:
        verbose_name_plural = "All Subscriptions"
