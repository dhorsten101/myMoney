from django.db import migrations


class Migration(migrations.Migration):

	dependencies = [
		('invoicing', '0020_property_rentalproperty_property_group'),
	]

	operations = [
		# Core model rename
		migrations.RenameModel(
			old_name='RentalProperty',
			new_name='Door',
		),
		# Related models renames
		migrations.RenameModel(
			old_name='RentalPropertyImage',
			new_name='DoorImage',
		),
		migrations.RenameModel(
			old_name='RentalPropertyPipeline',
			new_name='DoorPipeline',
		),
		migrations.RenameModel(
			old_name='RentalPropertyPipelineImage',
			new_name='DoorPipelineImage',
		),
		# Field renames to maintain data
		migrations.RenameField(
			model_name='invoice',
			old_name='rental_property',
			new_name='door',
		),
		migrations.RenameField(
			model_name='monthlyexpense',
			old_name='property',
			new_name='door',
		),
		migrations.RenameField(
			model_name='doorimage',
			old_name='property',
			new_name='door',
		),
	]


