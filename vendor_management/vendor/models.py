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
        historical_data = HistoricalPerformance.objects.filter(
            vendor=self,
            date__gte=thirty_days_ago
        )

        
        total_records = historical_data.count()
        on_time_delivery_rate = historical_data.filter(on_time_delivery_rate__gte=95).count() / total_records * 100 if total_records > 0 else 0
        quality_rating_avg = historical_data.aggregate(Avg('quality_rating_avg'))['quality_rating_avg__avg'] if total_records > 0 else 0
        average_response_time = historical_data.aggregate(Avg('average_response_time'))['average_response_time__avg'] if total_records > 0 else 0
        fulfillment_rate = historical_data.filter(fulfillment_rate__gte=95).count() / total_records * 100 if total_records > 0 else 0

       
        metrics = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return metrics
    def __str__(self):
        return f"{self.vendor} - {self.date}"