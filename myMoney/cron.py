from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1  # Set to the desired frequency (in minutes)
	
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'my_app.my_cron_job'  # Unique code
	
	def do(self):
		print("Running my cron job!")
