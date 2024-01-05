from django.db.models import signals


def my_callback(sender, args, kwargs):
    print(f'Pre init. Sender: {sender}, args: {args}, kwargs: {kwargs}')

signals.pre_init.connect(my_callback, sender=Question)
