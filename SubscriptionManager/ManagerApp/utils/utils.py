from django.utils import timezone
import datetime as DT


def is_active(sub):
    if sub.was_cancelled:
        return False
    else:
        if sub.recurring:
            return True
        else:
            return True if (sub.start_time + DT.timedelta(days=sub.duration)) \
                > timezone.now() and not sub.start_time > timezone.now() else False # noqa E501