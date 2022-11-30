from django.db import models
from django.db import connections
# Create your models here.
from django.utils import timezone
class Scrapper(models.Model):
    scrapper_id = models.IntegerField(primary_key=True)
    scrapper_jobs_log_id = models.IntegerField()
    external_job_source_id = models.IntegerField()
    start_time = models.DateTimeField(default=True)
    end_time = models.DateTimeField(default=True)
    scrapper_status = models.IntegerField()
    processed_records = models.IntegerField()
    new_records = models.IntegerField()
    skipped_records = models.IntegerField()
    error_records = models.IntegerField()

    class Meta:
        db_table = "scrapper_job_logs"