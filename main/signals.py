from crum import get_current_user
from django.apps import apps
from django.db.models.signals import post_save, post_delete

from .models import AuditLog


# Attach signal handlers to all models
def connect_signals():
	all_models = apps.get_models()
	
	for model in all_models:
		if model.__name__ == "AuditLog":  # Prevent recursion
			continue
		
		post_save.connect(log_save, sender=model, dispatch_uid=f"{model.__name__}_save")
		post_delete.connect(log_delete, sender=model, dispatch_uid=f"{model.__name__}_delete")


def log_save(sender, instance, created, **kwargs):
	user = get_current_user()
	
	# Only log if a real user is present (human interaction)
	if user is None or not user.is_authenticated:
		return
	
	action = "created" if created else "updated"
	AuditLog.objects.create(
		user=user,
		action=action,
		model_name=sender.__name__,
		object_id=instance.pk
	)


def log_delete(sender, instance, **kwargs):
	user = get_current_user()
	
	if user is None or not user.is_authenticated:
		return
	
	AuditLog.objects.create(
		user=user,
		action="deleted",
		model_name=sender.__name__,
		object_id=instance.pk
	)
