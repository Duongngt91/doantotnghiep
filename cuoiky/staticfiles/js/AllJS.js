// banner
document.addEventListener('DOMContentLoaded', function () {
  const banners = document.querySelector('.banners');
  const bannerImages = document.querySelectorAll('.banners img');
  const btnLeft = document.querySelector('.banner-btn-left');
  const btnRight = document.querySelector('.banner-btn-right');

  if (banners && bannerImages.length && btnLeft && btnRight) {
    let currentIndex = 0;
    const totalBanners = bannerImages.length;
    const bannerWidth = 1024; // phải khớp CSS width

    function showBanner(index) {
      if (index < 0) {
        currentIndex = totalBanners - 1;
      } else if (index >= totalBanners) {
        currentIndex = 0;
      } else {
        currentIndex = index;
      }

      const offset = -currentIndex * bannerWidth;
      banners.style.transform = `translateX(${offset}px)`;
    }

    // Nút trái
    btnLeft.addEventListener('click', function () {
      showBanner(currentIndex - 1);
    });

    // Nút phải
    btnRight.addEventListener('click', function () {
      showBanner(currentIndex + 1);
    });

    // Tự động chuyển banner mỗi 5 giây
    setInterval(function () {
      showBanner(currentIndex + 1);
    }, 5000);
  }

  // Cart quantity controls: move cart init into DOMContentLoaded to ensure DOM exists
  console.log('AllJS: initializing cart controls (DOMContentLoaded)');

  // Cart logic starts here
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const csrftoken = getCookie('csrftoken');

  async function sendUpdate(ctId, qty) {
    if (!ctId) return;
    try {
      const res = await fetch(`/capnhat_soluong/${ctId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken || ''
        },
        body: JSON.stringify({ quantity: qty })
      });
      if (!res.ok) {
        console.warn('update failed', await res.text());
        return;
      }
      const data = await res.json();
      // update UI from server response (line_total and cart_total are numbers)
      const row = document.querySelector(`.cart-items[data-ctid="${ctId}"]`);
      if (row) {
        const lineEl = row.querySelector('.line-total');
        if (lineEl && data.line_total !== undefined) lineEl.textContent = formatVND(data.line_total);
      }
      if (data.cart_total !== undefined) {
        const subtotalEl = document.getElementById('subtotal');
        const totalEl = document.getElementById('total');
        if (subtotalEl) subtotalEl.textContent = formatVND(data.cart_total);
        if (totalEl) totalEl.textContent = formatVND(data.cart_total);
      }
    } catch (err) {
      console.error('error updating cart quantity', err);
    }
  }
  function formatVND(n) {
    return Math.round(n).toLocaleString('vi-VN', {maximumFractionDigits: 0}) + ' đ';
  }

  function parseNumber(v) {
    if (v === undefined || v === null) return 0;
    if (typeof v === 'number') return v;
    const s = String(v).replace(/[^0-9.-]+/g, '');
    const n = Number(s);
    return isNaN(n) ? 0 : n;
  }

  function updateSummary() {
    let sum = 0;
    document.querySelectorAll('.cart-items').forEach(row => {
      const unit = parseNumber(row.dataset.unitprice);
      const qtyEl = row.querySelector('.qty');
      const qty = parseInt(qtyEl ? qtyEl.textContent : '0') || 0;
      sum += unit * qty;
    });
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');
    if (subtotalEl) subtotalEl.textContent = formatVND(sum);
    if (totalEl) totalEl.textContent = formatVND(sum);
  }

  document.querySelectorAll('.cart-items').forEach(item => {
    const decreaseBtn = item.querySelector('.decrease');
    const increaseBtn = item.querySelector('.increase');
    const quantitySpan = item.querySelector('.qty');
    const qtyInput = item.querySelector('.qty-input');
    const lineTotalEl = item.querySelector('.line-total');

    let quantity = parseInt(quantitySpan ? quantitySpan.textContent : '0') || 0;
    const unitPrice = parseNumber(item.dataset.unitprice);

    console.log('Cart row init:', {unitPrice, quantity});

    function updateLine() {
      const lineTotal = unitPrice * quantity;
      if (lineTotalEl) lineTotalEl.textContent = formatVND(lineTotal);
      if (qtyInput) qtyInput.value = quantity;
      if (quantitySpan) quantitySpan.textContent = quantity;
      updateSummary();
      // persist change to server
      const ctId = item.dataset.ctid;
      if (ctId) sendUpdate(ctId, quantity);
    }

    if (decreaseBtn) decreaseBtn.addEventListener('click', (ev) => {
      ev.preventDefault();
      console.log('decrease clicked for row', item);
        if (quantity > 1) {
          quantity--;
          updateLine();
        }
    });

    if (increaseBtn) increaseBtn.addEventListener('click', (ev) => {
      ev.preventDefault();
      console.log('increase clicked for row', item);
      quantity++;
      updateLine();
    });
  });

  // initialize summary on load
  updateSummary();
  
  // Also add delegated handlers in case buttons are dynamically inserted or event listeners fail
  document.addEventListener('click', function(ev){
    const inc = ev.target.closest('.increase');
    const dec = ev.target.closest('.decrease');
    if (!inc && !dec) return;
    ev.preventDefault();
    const row = ev.target.closest('.cart-items');
    if (!row) return;
    const qtyEl = row.querySelector('.qty');
    const qtyInput = row.querySelector('.qty-input');
    let q = parseInt(qtyEl ? qtyEl.textContent : (qtyInput? qtyInput.value: '0')) || 0;
    if (inc) q++;
    if (dec && q>1) q--;
    if (qtyEl) qtyEl.textContent = q;
    if (qtyInput) qtyInput.value = q;
    // update line total for this row
    const unit = parseNumber(row.dataset.unitprice);
    const lineEl = row.querySelector('.line-total');
    if (lineEl) lineEl.textContent = formatVND(unit * q);
    updateSummary();
    // persist via AJAX
    const ctId = row.dataset.ctid;
    if (ctId) sendUpdate(ctId, q);
    console.log('delegated click updated row, qty=', q, 'unit=', unit);
  });
});

// sidebar
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("collapsed");
}

