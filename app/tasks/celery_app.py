from celery import Celery
from celery.schedules import crontab


CELERY_BEAT_SCHEDULE = {
    'send-email-reminders': {
        'task': 'tasks.send_email_reminder',
        'schedule': crontab(minute=0, hour=8),  # Daily reminder at 8:00 AM
    },
    'generate-weekly-report': {
        'task': 'tasks.generate_weekly_report',
        'schedule': crontab(minute=0, hour=0, day_of_week=1),  # Weekly report on Monday
    },
}


app = Celery(
    'tasks',
    broker='redis://redis:6379/0',  # Redis broker URL
    backend='redis://redis:6379/0',  # Redis backend URL
    include=['app.tasks.reminders', 'app.tasks.reports']  # List of modules containing tasks
)

app.conf.update(
    result_expires=3600,
    timezone='UTC',
    beat_schedule=CELERY_BEAT_SCHEDULE
)
