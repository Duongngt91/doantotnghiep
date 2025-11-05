from django.shortcuts import render,redirect,get_object_or_404
from shoes.models import Danhmuc,SanPham,HinhAnhSanPham,Size,SizeSanPham,Nguoidung,NhaCungCap,GioHang,Chitietgiohang,Hoadon,Chitiethoadon
from .form import dangkyform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
# Create your views here.

def gioithieu(request):
    return render(request,'ss/gioithieu.html')

def index(request):

    hang = NhaCungCap.objects.all()
    giamgia = SanPham.objects.filter(giam_gia__isnull=False)
    return render(request,'ss/index.html',{'hang':hang,'giamgia':giamgia})

def chitiethang(request, ncc_id):
    hang = NhaCungCap.objects.get(id=ncc_id)
    danhmuc_list = Danhmuc.objects.filter(sanphams__nhacungcap=hang).distinct()

    context = {
        'hang':hang,
        'danhmuc':danhmuc_list,
    }
    return render(request,'ss/chitiethang.html',context)

def chitietdanhmuc(request,dm_id,id_ncc):
    hang = NhaCungCap.objects.get(id=id_ncc)
    dm =Danhmuc.objects.get(id=dm_id)
    sp = SanPham.objects.filter(nhacungcap=hang,danhmuc=dm)

    context = {
        'hang':hang,
        'dm':dm,
        'sp':sp,
    }

    return render(request, 'ss/chitietdanhmuc.html/',context )

def chitiet(request, masp ):
    ctsp = SanPham.objects.get(ma_sp=masp)
    size_sl = SizeSanPham.objects.filter(sanpham=ctsp)

    context = {

        'ctsp':ctsp,
        'soluong':size_sl,
    }
    return render(request,'ss/chitietsanpham.html',context)

def sanphamadidas(request):
    ncca = NhaCungCap.objects.get(ten_ncc='ADIDAS')
    spa = SanPham.objects.filter(nhacungcap=2)

    context = {
        "ncca" : ncca,
        "spa" : spa,
    }
    return render(request,'ss/sanphamadidas.html',context)

def sanphamnike(request):
    danhmuc = Danhmuc.objects.all()
    nccn = NhaCungCap.objects.get(ten_ncc='NIKE')
    spn = SanPham.objects.filter(nhacungcap=1)

    context = {
        "dm":danhmuc,
        "nccn" : nccn,
        "spn" : spn,
    }
    return render(request,'ss/sanphamnike.html',context)

def sanphamjordan(request):
    nccj = NhaCungCap.objects.get(ten_ncc='JORDAN')
    spj = SanPham.objects.filter(nhacungcap=3)

    context = {
        "nccj" : nccj,
        "spj" : spj,
    }
    return render(request,'ss/sanphamjordan.html',context)

def sanphampuma(request):
    nccp = NhaCungCap.objects.get(ten_ncc='PUMA')
    spp = SanPham.objects.filter(nhacungcap=4)
  
    context = {
        "nccp" : nccp,
        "spp" : spp,
    }
    return render(request,'ss/sanphampuma.html',context)

# def xemthem (request,madm):
#     xt = Danhmuc.objects.get(ma_dm=madm)
#     sp = SanPham.objects.filter(danhmuc=xt)

#     context = {
#         'xt': xt,
#         'sp': sp,
#     }
#     return render(request,'ss/xemthem.html',context)

def dangky(request ):
    if request.method == 'POST': 
        form = dangkyform(request.POST )
        if form.is_valid():
            form.save()
            return redirect('dn')
        else:
            return render(request,'ss/dangky.html',{'form':form})
    else:
        form = dangkyform()
    return render(request,'ss/dangky.html',{'form':form})

def dangnhap(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Chào {username}")
                return redirect("tc")
            else:
                messages.error(request,"Bạn nhập sai thông tin đăng nhập!")
        else:
            messages.error(request,f"Chưa nhập đủ thông tin!")
        
    else:
        form = AuthenticationForm()
    return render(request,"ss/dangnhap.html",{'form':form})

def dangxuat(request):
    dx=logout(request )
    return redirect('tc')

def timkiem(request):
    tukhoa = request.GET.get('q').strip()
    kq = []

    if tukhoa:
        kq= SanPham.objects.filter(ten_sp__icontains = tukhoa)

    return render(request, 'ss/timkiem.html',{'tukhoa':tukhoa,'kq':kq})

def themsp (request):
    if request.method == "POST":
        ten = request.POST.get('t')
        gia = request.POST.get('g')
        giamgia = request.POST.get('gg')
        hang = request.POST.get('h')
        danhmuc= request.POST.get('d')

        try: 
            ncc = NhaCungCap.objects.get(ten_ncc=hang)
        except:
            ncc = NhaCungCap.objects.create(ten_ncc=hang)

        try:
            dm = Danhmuc.objects.get(ten_dm=danhmuc)
        except:
            dm = Danhmuc.objects.create(ten_dm=danhmuc)

        sp = SanPham.objects.create(
            ten_sp=ten,
            gia=Decimal(gia),
            giam_gia=Decimal(giamgia)
            if giamgia
            else None,
            nhacungcap=ncc,
        )
        
        sp.danhmuc.add(dm)
        messages.success(request,f'Đã thêm mới sản phẩm {sp}')

    
    return render(request, 'ss/themsanpham.html',{'ncc_list':NhaCungCap.objects.all(),
                                                  'dm_list':Danhmuc.objects.all(),})


def xoasp(request,masp):
    sp = get_object_or_404(SanPham, ma_sp=masp)

    if request.method == 'POST':
        sp.delete()
        messages.success(request,f'Đã xóa {sp.ten_sp}')
        return redirect('tc')
    else:
        messages.error(request,'Không thể xóa')
        return redirect('ct')

        
def themvaogio(request):
    if request.method == 'POST':
        user = request.user
        masp = request.POST.get('masp')
        size_id = request.POST.get('size_id')
        soluong = int(request.POST.get('sl',1))

        if not size_id:
            messages.error(request,"Vui lòng chọn Size cho sản phẩm!!")
            return redirect('tc')

        sanpham = get_object_or_404(SanPham, ma_sp=masp)
        sizesp = get_object_or_404(SizeSanPham, id=size_id)

        giohang , created = GioHang.objects.get_or_create (nguoi_dung=user)


        chitiet, created = Chitietgiohang.objects.get_or_create(
            gio_hang = giohang,
            size_sanpham = sizesp,
            defaults = {
                'so_luong': soluong,
                'don_gia':sizesp.gia_tuy_chinh or sizesp.sanpham.gia_ban
            }
        )

        if not created:
            chitiet.so_luong += soluong
            if chitiet.don_gia is None:
                chitiet.don_gia = sizesp.gia_tuy_chinh
            chitiet.save()

        return redirect('gh')
    return redirect('tc')


def giohang(request):

   user =request.user
   giohang,created = GioHang.objects.get_or_create(nguoi_dung=user)
   items = giohang.chitiet.all()
   tong_tien = giohang.tonggiohang()

   return render(request, 'ss/giohang.html',{'items':items,'tong_tien':tong_tien})


def xoagiohang(request,item_id):
    item = Chitietgiohang.objects.get(id=item_id)

    if request.method == 'POST':
        item.delete()
        messages.success(request,f'Đã xóa khỏi giỏ hàng')
        return redirect('gh')
    else:
        messages.error(request,"Không thể xóa khỏi giỏ hàng!!")
        return redirect('gh')


def thanhtoan(request):
    user = request.user
    giohang = GioHang.objects.get(nguoi_dung=user)
    
    if not  giohang or not giohang.chitiet.exists():
        messages.warning(request,'Giỏ hàng bạn đang trống.Hãy chọn sản phẩm phù hợp với mình nhé')
        return redirect('tc')
    
    if request.method == 'POST':
        diachi = request.POST.get('dia_chi')
        phuongthuc = request.POST.get('phuong_thuc','cod')
        phiship = Decimal(30000)
        tongtien = giohang.tonggiohang()

        hoadon = Hoadon.objects.create(
            nguoidung=user,
            dia_chi=diachi,
            phuong_thuc=phuongthuc,
            phi_ship=phiship,
            tong_tien = tongtien,
            
        )

        for item in giohang.chitiet.all():
            Chitiethoadon.objects.create(
                hoa_don = hoadon,
                size_sanpham = item.size_sanpham,
                so_luong = item.so_luong,
                don_gia = item.don_gia,
            )

        giohang.chitiet.all().delete()

        messages.success(request,f'Đặt hàng thành công! Mã đơn #{hoadon.id}')
        return redirect('dh')
    
    tiensanpham = giohang.tonggiohang()
    phigiaohang = Decimal(30000)
    tongcong = tiensanpham + phigiaohang

    return render(request,'ss/thanhtoan.html',{'giohang':giohang,
                                               'tiensp':tiensanpham,
                                               'phigh':phigiaohang,
                                               'tongcong':tongcong})


def donhang(request):
    user = request.user
    hoadon = Hoadon.objects.filter(nguoidung=user).order_by('-ngay_tao')
    cthd = Chitiethoadon.objects.filter(hoa_don__in=hoadon).select_related('size_sanpham__sanpham')

    context = {
        'list_hd':hoadon,
        'ct':cthd,
        'pending': hoadon.filter(trang_thai='pending'),
        'confirmed':hoadon.filter(trang_thai='confirmed'),
        'shipping': hoadon.filter(trang_thai='shipping'),
        'delivered': hoadon.filter(trang_thai='delivered'),
        'cancelled': hoadon.filter(trang_thai='cancelled'),
    }
    return render(request,'ss/donhang.html',context)


def huydon(request,order_id):
    huy = Hoadon.objects.get(id=order_id,trang_thai='pending' )
    if request.method == 'POST' or request.method == 'GET':
        huy.trang_thai = 'cancelled'
        huy.save()
        messages.success(request,f'Đã hủy đơn hàng')
        return redirect('dh')
    
    

@staff_member_required
def quantri(request):
    tong_don = Hoadon.objects.count()
    don_cho = Hoadon.objects.filter(trang_thai='pending').count()
    da_xac_nhan = Hoadon.objects.filter(trang_thai='confirmed').count()
    dang_giao = Hoadon.objects.filter(trang_thai='shipping').count()
    hoan_tat = Hoadon.objects.filter(trang_thai='delivered').count()
    doanh_thu =Hoadon.objects.filter(trang_thai='delivered').aggregate(
    tong=Sum('tong_tien')) or 0

    ds_don = Hoadon.objects.select_related('nguoidung').order_by('ngay_tao').prefetch_related('cthd__size_sanpham__sanpham')
    context = {
        'td':tong_don,
        'dxn':da_xac_nhan,
        'dc':don_cho,
        'dg':dang_giao,
        'ht':hoan_tat,
        'dt':doanh_thu['tong'] or 0,
        'ds':ds_don
    }
    return render(request,'ss/quantri.html',context)

def capnhattrangthai(request, order_id):
    hoadon = Hoadon.objects.get(id=order_id)
    status = request.POST.get('trang_thai')

    if status in dict(Hoadon.trangthai_choices).keys():
        hoadon.trang_thai = status
        hoadon.save()
    else:
        messages.error(request,'Trạng thái không hợp lệ')
    
    return redirect('qt')
