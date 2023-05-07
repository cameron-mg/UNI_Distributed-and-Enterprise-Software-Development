from django_cron import CronJobBase, Schedule
from models import Transaction
import datetime


def generate_monthly_statements():
    today = datetime.date.today()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)
    transactions = Transaction.objects.filter(datetime__month=last_month.month, datetime__year=last_month.year)
    print(transactions)


