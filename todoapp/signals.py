from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from .models import Task, Message
from django.core.exceptions import ValidationError
@receiver([post_save, post_delete], sender=Message)
def update_task_flagged_status(sender, instance, **kwargs):
    task = instance.task
    # Correctly access the related Message instances
    if task.messages.filter(is_flagged=True).exists():  # Use 'messages' here
        task.is_flaged = True
    else:
        task.is_flaged = False
    task.save()


@receiver(pre_save, sender=Task)
def adjust_project_wallet_on_task_creation(sender, instance, **kwargs):
    # If the task is being updated, calculate the difference
    if instance.pk:
        previous_task = Task.objects.get(pk=instance.pk)
        wallet_difference = instance.task_wallet - previous_task.task_wallet
    else:
        wallet_difference = instance.task_wallet

    # Check if the project has enough funds
    if instance.project.project_wallet < wallet_difference:
        raise ValidationError(f"Not enough funds in project wallet to create/update this task. "
                              f"Available: {instance.project.project_wallet}, Required: {wallet_difference}")

    # Deduct or adjust the task_wallet from project_wallet
    instance.project.project_wallet -= wallet_difference
    instance.project.save()


@receiver(post_delete, sender=Task)
def return_wallet_on_task_deletion(sender, instance, **kwargs):
    # Add the task_wallet back to the project_wallet when a task is deleted
    instance.project.project_wallet += instance.task_wallet
    instance.project.save()