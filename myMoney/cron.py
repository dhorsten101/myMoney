from django_cron import CronJobBase, Schedule

from api.utils import process_dashboard_data


class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 10  # Run every 10 minutes
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'myMoney.my_cron_job'  # Unique identifier
	
	def do(self):
		# Call the shared function for processing
		process_dashboard_data()
		print("Cron job completed: Dashboard data processed!")
