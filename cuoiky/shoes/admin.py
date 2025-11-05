from django.contrib import admin
from shoes.models import HinhAnhSanPham,SanPham,Danhmuc,NhaCungCap,Size,SizeSanPham,GioHang,Nguoidung,Chitietgiohang
# Register your models here.

admin.site.register(SanPham)
admin.site.register(Danhmuc)
admin.site.register(NhaCungCap)
admin.site.register(HinhAnhSanPham)
admin.site.register(Size)
admin.site.register(SizeSanPham)
admin.site.register(GioHang)
admin.site.register(Nguoidung)
admin.site.register(Chitietgiohang)