from django.db.models.signals import post_save
from django.dispatch import receiver

from powermeter.meters.models import Measure


@receiver(post_save, sender=Measure)
def my_model_add_tags(sender, instance, created, **kwargs):
    # Create the default goal for accounts without a goal.
    if created:
        print(instance)
        # Do staff
        # TODO: CREAR OPERATION RESULT
        # OBTENGO MI ANCESTRO DESDE instance.operation_result
        # OBTENER TAGS DEL ANCESTRO
        pass

