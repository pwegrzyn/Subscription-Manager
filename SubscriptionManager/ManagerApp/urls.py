from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='raw_index'),
    path('manager/', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('subscription/<int:id>/', views.subscription, name='subscription'),
    path('add_subscription/', views.add_subscription, name='add_subscription'),
    path('add_plan/', views.add_plan, name='add_plan'),
    path('add_plan/success', views.add_plan_success, name='add_plan_success'),
    path('add_plan/failure', views.add_plan_failure, name='add_plan_failure'),
    path('add_subscription/success', views.add_subscription_success, name='add_subscription_success'), # noqa E501
    path('add_subscription/failure', views.add_subscription_failure, name='add_subscription_failure'), # noqa E501
    path('recommendations/', views.recommendations, name='recommendations'),
    path('misc/', views.miscellaneous, name='miscellaneous'),
    path('misc/success/all', views.miscellaneous_success_all, name='miscellaneous_success_all'), # noqa E501
    path('misc/success/subs', views.miscellaneous_success_subs, name='miscellaneous_success_subs'), # noqa E501
    path('misc/success/stats', views.miscellaneous_success_stats, name='miscellaneous_success_stats'), # noqa E501
    path('summary/', views.summary, name='summary'),
    path('plans/', views.plan_management, name='plan_management'),
    path('plan/<int:id>/', views.plan, name='plan')
]
