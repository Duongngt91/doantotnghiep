from django.urls import path
from shoes import views 


urlpatterns = [
    path('gioithieu/',views.gioithieu,name='gt'),
    path('',views.index,name='tc'),
    path('chitiethang/<int:ncc_id>/',views.chitiethang,name='cth'),
    path('hang/<int:id_ncc>/danhmuc/<int:dm_id>',views.chitietdanhmuc,name='ctdm'),
    path('dangky/',views.dangky,name='dk'),
    path('dangnhap/',views.dangnhap,name='dn'),
    path('dangxuat/',views.dangxuat,name='dx'),
    path('sanphamadidas/',views.sanphamadidas,name='spa'),
    path('sanphamnike/',views.sanphamnike,name='spn'),
    path('sanphamjordan/',views.sanphamjordan,name='spj'),
    path('sanphampuma/',views.sanphampuma,name='spp'),
    path('chitiet/<str:masp>/',views.chitiet,name='ct'),
    path('timkiem/',views.timkiem,name='tk'),
    path('themmoi/',views.themsp,name='tsp'),
    path('xoasanpham/<str:masp>/',views.xoasp,name='x'),
    # path('xemthem/<str:madm>/',views.xemthem,name='xt'),
    path('themvaogio/',views.themvaogio,name='tvg'),
    path('giohang/',views.giohang,name='gh'),
    path('xoagiohang/<int:item_id>',views.xoagiohang,name='xgh'),
    path('thanhtoan/',views.thanhtoan,name='tt'),
    path('donhang/',views.donhang,name='dh'),
    path('quantri/',views.quantri,name='qt'),
    path('capnhatdonhang/<int:order_id>',views.capnhattrangthai,name='cn'),
    path('huydonhang/<int:order_id>',views.huydon,name='huy'),
]
