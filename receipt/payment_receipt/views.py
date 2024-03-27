import pdfkit
import qrcode
import os

from django.utils.timezone import localtime
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from datetime import datetime

from .models import Item


class CashMachineAPIView(APIView):
    def post(self, request, *args, **kwargs):
        items_ids = request.data.get('items', [])
        items = Item.objects.filter(id__in=items_ids)

        items_count = {}
        for item in items:
            if item.id in items_count:
                items_count[item.id]['quantity'] += 1
                items_count[item.id]['total_price'] += item.price
            else:
                items_count[item.id] = {
                    'title': item.title,
                    'quantity': 1,
                    'price': item.price,
                    'total_price': item.price
                }

        time_now = datetime.now()
        total = sum([item['total_price'] for item in items_count.values()])
        context = {
            'items': [
                (
                    item['title'],
                    item['quantity'],
                    item['price'],
                    item['total_price']
                ) for item in items_count.values()
            ],
            'total': total,
            'created_at': time_now.strftime('%d.%m.%Y %H:%M')
        }

        html = render_to_string('receipt_template.html', context)
        pdf = pdfkit.from_string(html, False)

        file_name = f'receipt_{localtime().strftime("%Y%m%d%H%M%S")}.pdf'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as f:
            f.write(pdf)

        qr = qrcode.make(request.build_absolute_uri(f'/media/{file_name}'))
        qr_path = f'qr_{file_name}.png'
        qr.save(os.path.join(settings.MEDIA_ROOT, qr_path))

        return HttpResponse(f'QR код сохранен как /media/{qr_path}')
