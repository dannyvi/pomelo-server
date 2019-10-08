from django.db import models
import string
import datetime
import random


def upload_to(instance, filename):
    """Give the uploaded file a unique file name."""
    pref_len = 10
    prefix = ''.join(random.sample(string.ascii_letters + string.digits, pref_len))
    timestamp = str(int(datetime.datetime.now().timestamp()*1000000))
    return ''.join([prefix, timestamp, filename])


class Image(models.Model):
    """All image files are uploaded here and return to a charstring url."""
    url = models.ImageField(upload_to=upload_to)
