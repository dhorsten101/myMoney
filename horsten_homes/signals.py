from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from horsten_homes.models import MonthlyExpense, Door


def _recalc_for_door(door: Door):
	try:
		if door and door.property_group_id:
			door.property_group.recalc_totals()
	except Exception:
		pass


@receiver(post_save, sender=MonthlyExpense)
def on_expense_saved(sender, instance: MonthlyExpense, created, **kwargs):
	if instance.door_id:
		_recalc_for_door(instance.door)


@receiver(post_delete, sender=MonthlyExpense)
def on_expense_deleted(sender, instance: MonthlyExpense, **kwargs):
	if instance.door_id:
		_recalc_for_door(instance.door)






