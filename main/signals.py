from crum import get_current_user, get_current_request
from django.apps import apps
from django.db import models
from django.db.models.signals import post_save, post_delete

from .models import AuditLog


def connect_signals():
	all_models = apps.get_models()
	for model in all_models:
		if model.__name__ == "AuditLog":  # Avoid recursion
			continue
		
		post_save.connect(log_save, sender=model, dispatch_uid=f"{model.__name__}_save")
		post_delete.connect(log_delete, sender=model, dispatch_uid=f"{model.__name__}_delete")


def _safe_object_id(instance) -> int:
	"""
	AuditLog.object_id is an integer field, but some Django models (e.g. Session)
	use a string primary key. Never let audit logging crash the request.
	"""
	pk = getattr(instance, "pk", None)
	if pk is None:
		return 0
	if isinstance(pk, int):
		return pk
	try:
		return int(pk)
	except Exception:
		return 0


def log_save(sender, instance, created, **kwargs):
	user = get_current_user()
	request = get_current_request()
	
	if user is None or not user.is_authenticated:
		return
	
	object_repr = str(instance)
	changes = {}
	
	if not created:
		try:
			old_instance = sender.objects.get(pk=instance.pk)
			
			for field in instance._meta.fields:
				field_name = field.name
				
				# Skip fields like auto_now/auto_now_add if desired
				if getattr(field, 'auto_now', False) or getattr(field, 'auto_now_add', False):
					continue
				
				# ForeignKey handling
				if isinstance(field, models.ForeignKey):
					old_value = getattr(old_instance, f"{field_name}_id", None)
					new_value = getattr(instance, f"{field_name}_id", None)
				else:
					old_value = getattr(old_instance, field_name, None)
					new_value = getattr(instance, field_name, None)
				
				if old_value != new_value:
					changes[field_name] = [str(old_value), str(new_value)]
		
		except sender.DoesNotExist:
			pass  # Edge case: previous version not found
	
	AuditLog.objects.create(
		user=user,
		action="created" if created else "updated",
		model_name=sender.__name__,
		object_id=_safe_object_id(instance),
		object_repr=object_repr,
		changes=changes or None,
		remote_ip=request.META.get("REMOTE_ADDR") if request else None,
		user_agent=request.META.get("HTTP_USER_AGENT") if request else None,
		view_name=request.resolver_match.view_name if request and request.resolver_match else None,
		request_method=request.method if request else None,
		referrer=request.META.get("HTTP_REFERER") if request else None,
		session_key=request.session.session_key if request and hasattr(request, "session") else None,
		is_manual_action=True
	)


def log_delete(sender, instance, **kwargs):
	user = get_current_user()
	request = get_current_request()
	
	if user is None or not user.is_authenticated:
		return
	
	AuditLog.objects.create(
		user=user,
		action="deleted",
		model_name=sender.__name__,
		object_id=_safe_object_id(instance),
		object_repr=str(instance),
		remote_ip=getattr(request, "META", {}).get("REMOTE_ADDR") if request else None,
		user_agent=request.META.get("HTTP_USER_AGENT") if request else None,
		view_name=request.resolver_match.view_name if request and request.resolver_match else None,
		request_method=request.method if request else None,
		referrer=request.META.get("HTTP_REFERER") if request else None,
		session_key=request.session.session_key if request and hasattr(request, "session") else None,
		is_manual_action=True
	)
