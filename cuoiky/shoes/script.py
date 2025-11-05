import os
import django
import sys


sys.path.append(r"D:\doan\cuoiky")

# Cấu hình Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cuoiky.settings")
django.setup()

import csv
from shoes.models import SanPham,Danhmuc,NhaCungCap,Size,SizeSanPham
from decimal import Decimal

with open(r'D:\doan\dulieu\nmt_sanphamsize.csv', newline='', encoding='utf-8-sig') as csvfile:

   reader = csv.DictReader(csvfile)
   for row in reader:
    sp = SanPham.objects.get(ma_sp=row['SANPHAM'])
    size = Size.objects.get(id=row['SIZE'])
       
    SizeSanPham.objects.create(
        sanpham=sp,
        size=size,
        so_luong=row['SOLUONG'],
    )

print("Hoàn tất import")