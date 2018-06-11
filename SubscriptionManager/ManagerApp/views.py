from django.shortcuts import render, redirect
from .models import Subscription, Tag, SubscriptionPlan
from django.http import Http404
from .utils.utils import is_active
from .forms import SubscriptionForm, SubscriptionPlanForm
from random import shuffle
from operator import attrgetter
from django.utils import timezone
import datetime as DT


# Create your views here.

# View the main page
def index(request):
    context = dict()
    return render(request, 'ManagerApp/index.html', context)


# View the history tab
def history(request):
    context = dict()
    context['subscriptions'] = Subscription.objects.order_by('-start_time')

    summed_price = 0
    for sub in context['subscriptions']:
        summed_price += sub.price
    context['totally_spent'] = summed_price

    for sub in context['subscriptions']:
        sub.status = is_active(sub)

    return render(request, 'ManagerApp/history.html', context)


# View a particular subscription
def subscription(request, *args, **kwargs):
    context = dict()

    sub_id = kwargs['id']
    try:
        sub = Subscription.objects.get(pk=sub_id)
    except Subscription.DoesNotExist:
        raise Http404("Subscription does not exist!")

    sub.status = is_active(sub)
    context['subscription'] = sub

    return render(request, 'ManagerApp/subscription.html', context)


# View of adding a subscription
def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            new_sub = Subscription()
            new_sub.service_name = request.POST['service_name']
            new_sub.price = form.cleaned_data['price']
            new_sub.duration = form.cleaned_data['duration']
            new_sub.start_time = request.POST['start_time']
            new_sub.link = request.POST['link']
            new_sub.notes = request.POST['notes']
            new_sub.plan = form.cleaned_data['plan']
            new_sub.tags = request.POST['tags']
            rating = form.cleaned_data['personal_rating']
            new_sub.personal_rating = rating if rating >= 0 and rating <= 100 else 0 # noqa E501
            new_sub.save()

            tags = map(lambda s: s.lower(), new_sub.tags.split())
            for tag in tags:
                try:
                    found_tag = Tag.objects.all().get(name=tag)
                    found_tag.occurance += 1
                    found_tag.save()
                except Tag.DoesNotExist:
                    new_tag = Tag()
                    new_tag.name = tag
                    new_tag.occurance = 1
                    new_tag.save()

            return redirect('add_subscription_success')
        else:
            return redirect('add_subscription_failure')

    else:
        form = SubscriptionForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_subscription.html', context)


# View of adding a plan
def add_plan(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)

        if form.is_valid():
            new_plan = SubscriptionPlan()
            new_plan.name = request.POST['name']
            new_plan.planned_budget = form.cleaned_data['planned_budget']
            new_plan.planned_amount = form.cleaned_data['planned_amount']
            new_plan.save()
            return redirect('add_plan_success')
        else:
            return redirect('add_plan_failure')

    else:
        form = SubscriptionPlanForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_plan.html', context)


# View of the recommendations
def recommendations(request):
    context = dict()
    subs = Subscription.objects.all()
    all_tags = Tag.objects.all()
    context['subs_len'] = len(subs)
    context['suggestions'] = []

    most_popular_tag = max(all_tags, key=attrgetter('occurance'))
    least_popular_tag = min(all_tags, key=attrgetter('occurance'))
    best_rated_sub = max(subs, key=attrgetter('personal_rating'))
    worst_rated_sub = min(subs, key=attrgetter('personal_rating'))
    cheapest_sub = min(subs, key=attrgetter('price'))
    most_expensive_sub = max(subs, key=attrgetter('price'))

    most_reasonable_sub_rating = -1
    for sub in subs:
        if sub.personal_rating / sub.price > most_reasonable_sub_rating:
            most_reasonable_sub_rating = sub.personal_rating / sub.price
            most_reasonable_sub = sub

    context['suggestions'].append('... ' + most_popular_tag.name + ", because you have the most subscriptions of this type") # noqa E501
    context['suggestions'].append('... ' + best_rated_sub.service_name + ", because you have rated this subscription the highest") # noqa E501
    context['suggestions'].append('... ' + cheapest_sub.service_name + ", because it is the cheapest") # noqa E501
    context['suggestions'].append('... ' + most_reasonable_sub.service_name + ", because it is has the biggest Rating/Price ratio") # noqa E501
    context['suggestions'].append('... to avoid ' + worst_rated_sub.service_name + ", because you don't seem to like it") # noqa E501
    context['suggestions'].append('... to avoid ' + most_expensive_sub.service_name + ", because it is the most expensive") # noqa E501
    context['suggestions'].append('... to avoid ' + least_popular_tag.name + ", because you have the least amount of subscriptions of this type") # noqa E501
    shuffle(context['suggestions'])
    return render(request, 'ManagerApp/recommendations.html', context)


# View of the Summary Dashboard
def summary(request):
    context = dict()
    context['active_subs'] = [sub for sub in Subscription.objects.all() if is_active(sub)] # noqa E501
    for sub in context['active_subs']:
        if sub.start_time > timezone.now():
            sub.progress = 'width: 0%'
        elif (sub.start_time + DT.timedelta(days=sub.duration)) < timezone.now(): # noqa
            sub.progress = 'width: 100%'
        else:
            sub.progress = 'width: ' + str(int(100 - (100 * (((sub.start_time +
                DT.timedelta(days=sub.duration) - timezone.now()).days) / sub.duration)))) + '%' # noqa

    context['active_subs_len'] = len(context['active_subs'])

    context['active_worth'] = 0
    for sub in context['active_subs']:
        context['active_worth'] += sub.price

    context['all_worth'] = 0
    for sub in Subscription.objects.all():
        context['all_worth'] += sub.price

    context['most_pop_cat'] = max(Tag.objects.all(), key=attrgetter('occurance')) # noqa E501

    context['highest_rated_sub'] = max(context['active_subs'], key=attrgetter('personal_rating')) # noqa E501

    return render(request, 'ManagerApp/summary.html', context)


# View of a particular plan
def plan(request, *args, **kwargs):
    context = dict()

    plan_id = kwargs['id']
    try:
        plan = SubscriptionPlan.objects.get(pk=plan_id)
    except SubscriptionPlan.DoesNotExist:
        raise Http404("Subscription Plan does not exist!")

    context['plan'] = plan
    context['subs'] = Subscription.objects.filter(plan=plan)
    context['subs_len'] = len(context['subs'])

    summed_price = 0
    for sub in context['subs']:
        summed_price += sub.price
    context['totally_spent'] = summed_price

    return render(request, 'ManagerApp/plan.html', context)


# View of the Plans Tab
def plan_management(request):
    context = dict()

    context['plans'] = SubscriptionPlan.objects.order_by('name')
    context['subscriptions'] = Subscription.objects.order_by('-start_time')

    for sub in context['subscriptions']:
        sub.status = is_active(sub)

    return render(request, 'ManagerApp/plan_management.html', context)


# View of the MISC tab (mainly settings)
def miscellaneous(request):
    context = dict()
    return render(request, 'ManagerApp/miscellaneous.html', context)


# Auxilliary
def miscellaneous_success_all(request):
    context = dict()
    Subscription.objects.all().delete()
    Tag.objects.all().delete()
    SubscriptionPlan.objects.all().delete()
    return render(request, 'ManagerApp/misc_reset_success.html', context)


# Auxilliary
def miscellaneous_success_subs(request):
    context = dict()
    Subscription.objects.all().delete()
    return render(request, 'ManagerApp/misc_reset_success.html', context)


# Auxilliary
def miscellaneous_success_stats(request):
    context = dict()
    Tag.objects.all().delete()
    return render(request, 'ManagerApp/misc_reset_success.html', context)


# ------------------------------------------------------------------------------
# Methods below are only for a better visual experience
# They do not add anything new to the logic
# ------------------------------------------------------------------------------


def add_subscription_success(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            new_sub = Subscription()
            new_sub.service_name = request.POST['service_name']
            new_sub.price = form.cleaned_data['price']
            new_sub.duration = form.cleaned_data['duration']
            new_sub.start_time = request.POST['start_time']
            new_sub.link = request.POST['link']
            new_sub.notes = request.POST['notes']
            new_sub.plan = form.cleaned_data['plan']
            new_sub.tags = request.POST['tags']
            rating = form.cleaned_data['personal_rating']
            new_sub.personal_rating = rating if rating >= 0 and rating <= 100 else 0 # noqa E501
            new_sub.save()

            tags = map(lambda s: s.lower(), new_sub.tags.split())
            for tag in tags:
                try:
                    found_tag = Tag.objects.all().get(name=tag)
                    found_tag.occurance += 1
                    found_tag.save()
                except Tag.DoesNotExist:
                    new_tag = Tag()
                    new_tag.name = tag
                    new_tag.occurance = 1
                    new_tag.save()

            return redirect('add_subscription_success')
        else:
            return redirect('add_subscription_failure')

    else:
        form = SubscriptionForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_subscription_success.html', context) # noqa E501


def add_subscription_failure(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            new_sub = Subscription()
            new_sub.service_name = request.POST['service_name']
            new_sub.price = form.cleaned_data['price']
            new_sub.duration = form.cleaned_data['duration']
            new_sub.start_time = request.POST['start_time']
            new_sub.link = request.POST['link']
            new_sub.notes = request.POST['notes']
            new_sub.plan = form.cleaned_data['plan']
            new_sub.tags = request.POST['tags']
            rating = form.cleaned_data['personal_rating']
            new_sub.personal_rating = rating if rating >= 0 and rating <= 100 else 0 # noqa E501
            new_sub.save()

            tags = map(lambda s: s.lower(), new_sub.tags.split())
            for tag in tags:
                try:
                    found_tag = Tag.objects.all().get(name=tag)
                    found_tag.occurance += 1
                    found_tag.save()
                except Tag.DoesNotExist:
                    new_tag = Tag()
                    new_tag.name = tag
                    new_tag.occurance = 1
                    new_tag.save()

            return redirect('add_subscription_success')
        else:
            return redirect('add_subscription_failure')

    else:
        form = SubscriptionForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_subscription_failure.html', context) # noqa E501


def add_plan_success(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)

        if form.is_valid():
            new_plan = SubscriptionPlan()
            new_plan.name = request.POST['name']
            new_plan.planned_budget = form.cleaned_data['planned_budget']
            new_plan.planned_amount = form.cleaned_data['planned_amount']
            new_plan.save()
            return redirect('add_plan_success')
        else:
            return redirect('add_plan_failure')

    else:
        form = SubscriptionPlanForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_plan_success.html', context)


def add_plan_failure(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)

        if form.is_valid():
            new_plan = SubscriptionPlan()
            new_plan.name = request.POST['name']
            new_plan.planned_budget = form.cleaned_data['planned_budget']
            new_plan.planned_amount = form.cleaned_data['planned_amount']
            new_plan.save()
            return redirect('add_plan_success')
        else:
            return redirect('add_plan_failure')

    else:
        form = SubscriptionPlanForm()
        context = {'form': form}
        return render(request, 'ManagerApp/add_plan_failure.html', context)
