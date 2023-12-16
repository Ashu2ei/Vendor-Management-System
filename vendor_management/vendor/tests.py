from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder

class VendorManagementTest(APITestCase):

    def setUp(self):
        # Create test data
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test Street',
            'vendor_code': 'TEST123',
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.po_data = {
            'po_number': 'PO123',
            'vendor': self.vendor,
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-10T12:00:00Z',
            'items': [{'name': 'Item1', 'quantity': 5}],
            'quantity': 5,
            'status': 'pending',
            'issue_date':'2023-01-10T12:00:00Z'
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.po_data)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_list_vendors(self):
    #     url = reverse('vendor-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_retrieve_vendor_details(self):
    #     url = reverse('vendor-detail', args=[self.vendor.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_vendor_details(self):
    #     url = reverse('vendor-detail', args=[self.vendor.id])
    #     updated_data = {'name': 'Updated Vendor'}
    #     response = self.client.put(url, updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_vendor(self):
    #     url = reverse('vendor-detail', args=[self.vendor.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # def test_create_purchase_order(self):
    #     url = reverse('purchaseorder-list')
    #     response = self.client.post(url, self.po_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_list_purchase_orders(self):
    #     url = reverse('purchaseorder-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_retrieve_purchase_order_details(self):
    #     url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_purchase_order_details(self):
    #     url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
    #     updated_data = {'status': 'completed'}
    #     response = self.client.put(url, updated_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_purchase_order(self):
    #     url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_vendor_performance(self):
    #     url = reverse('vendor-performance', args=[self.vendor.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('on_time_delivery_rate', response.data)
    #     self.assertIn('quality_rating_avg', response.data)
    #     self.assertIn('average_response_time', response.data)
    #     self.assertIn('fulfillment_rate', response.data)

    # # Similarly, write test cases for PurchaseOrder and VendorPerformance endpoints
