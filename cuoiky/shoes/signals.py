from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shoes.models import SanPham,Size,SizeSanPham,Danhmuc


# Receiver (Handler function)

# Là hàm bạn viết để xử lý khi signal phát ra.

# Hàm này nhận vào ít nhất:

# sender: Model nào phát tín hiệu

# instance: object cụ thể vừa bị save/delete

# **kwargs: thông tin thêm (vd: created trong post_save)


# Sender

# Là model hoặc class phát ra tín hiệu.

# Ví dụ: khi bạn save() hoặc delete() một SizeSanPham, thì SizeSanPham chính là sender.


# @receiver([post_save,post_delete] , sender=SizeSanPham)
# def update_sanpham_danhmuc(sender, instance , **kwargs):
#     sp = instance.sanpham
#     size = sp.size_sp.all().values_list('size__size', flat=True)
    

#     dmnam = Danhmuc.objects.get(ten_dm='Giày Nam')
#     dmnu = Danhmuc.objects.get(ten_dm='Giày Nữ')

#     if any (float(s) >=40 for s in size) :
#         sp.danhmuc.add(dmnam)
#     else:
#         sp.danhmuc.remove(dmnam)

#     if any (float(s) < 40 for s in size) :
#         sp.danhmuc.add(dmnu)
#     else:
#         sp.danhmuc.remove(dmnu)
       