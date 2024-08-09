from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, Message

@receiver([post_save, post_delete], sender=Message)
def update_task_flagged_status(sender, instance, **kwargs):
    task = instance.task
    # Correctly access the related Message instances
    if task.messages.filter(is_flagged=True).exists():  # Use 'messages' here
        task.is_flaged = True
    else:
        task.is_flaged = False
    task.save()
