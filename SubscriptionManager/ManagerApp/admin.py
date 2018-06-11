from django.contrib import admin
from .models import Subscription, SubscriptionPlan, Tag

# Register your models here.


admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Tag)
