from django.db import models
from django.db.models import Count, Avg
from datetime import datetime, timedelta

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def calculate_performance_metrics(self):
        thirty_days_ago = datetime.now() - timedelta(days=30)
        completed_pos = PurchaseOrder.objects.filter(
            vendor=self,
            status='completed',
            delivery_date__lte=('2023-01-01T12:00:00Z'),
            acknowledgment_date__isnull=False
        )
        total_completed_pos = completed_pos.count()
        on_time_delivery_rate = (total_completed_pos / completed_pos.count()) * 100 if total_completed_pos > 0 else 0

        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] if completed_pos_with_rating.count() > 0 else 0

        acknowledgment_times = completed_pos.values('acknowledgment_date', 'issue_date')
        average_response_time = (
            sum((item['acknowledgment_date'] - item['issue_date']).total_seconds() / 60 for item in acknowledgment_times) /
            len(acknowledgment_times)
        ) if len(acknowledgment_times) > 0 else 0

        successful_fulfillments = completed_pos.filter(issues__isnull=True)
        fulfillment_rate = (successful_fulfillments.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0

        metrics = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return metrics