/* ==========================================================================
   MINIONS CAFE POS - CLIENT LOGIC & STATE MANAGEMENT
   Supports both Backend API and Standalone Browser execution
   ========================================================================== */

// Initial Seed Data (Matches wk07 Schema and wk10 Specification)
const DEFAULT_MENU = [
  // Branch 1
  {
    menuId: 1,
    branchId: 1,
    categoryId: 1,
    name: "Latte (ลาเต้ร้อน/เย็น)",
    price: 45.0,
    stockQuantity: 12,
    icon: "☕",
  },
  {
    menuId: 2,
    branchId: 1,
    categoryId: 1,
    name: "Espresso (เอสเปรสโซ่)",
    price: 35.0,
    stockQuantity: 8,
    icon: "☕",
  },
  {
    menuId: 3,
    branchId: 1,
    categoryId: 1,
    name: "Cappuccino (คาปูชิโน่)",
    price: 50.0,
    stockQuantity: 15,
    icon: "☕",
  },
  {
    menuId: 4,
    branchId: 1,
    categoryId: 1,
    name: "Americano (อเมริกาโน่)",
    price: 40.0,
    stockQuantity: 20,
    icon: "☕",
  },
  {
    menuId: 5,
    branchId: 1,
    categoryId: 2,
    name: "Matcha Green Tea (ชาเขียว)",
    price: 50.0,
    stockQuantity: 10,
    icon: "🍵",
  },
  {
    menuId: 6,
    branchId: 1,
    categoryId: 2,
    name: "Thai Milk Tea (ชาไทยเย็น)",
    price: 40.0,
    stockQuantity: 14,
    icon: "🧋",
  },
  {
    menuId: 7,
    branchId: 1,
    categoryId: 2,
    name: "Lemon Tea (ชามะนาวเย็น)",
    price: 45.0,
    stockQuantity: 0,
    icon: "🍋",
  }, // Stock = 0 for FR-11
  {
    menuId: 8,
    branchId: 1,
    categoryId: 3,
    name: "Butter Croissant (ครัวซองต์)",
    price: 55.0,
    stockQuantity: 9,
    icon: "🥐",
  },
  {
    menuId: 9,
    branchId: 1,
    categoryId: 3,
    name: "Chocolate Brownie (บราวนี่)",
    price: 45.0,
    stockQuantity: 16,
    icon: "🍫",
  },

  // Branch 2
  {
    menuId: 10,
    branchId: 2,
    categoryId: 1,
    name: "Latte (ลาเต้ร้อน/เย็น)",
    price: 45.0,
    stockQuantity: 22,
    icon: "☕",
  },
  {
    menuId: 11,
    branchId: 2,
    categoryId: 1,
    name: "Espresso (เอสเปรสโซ่)",
    price: 35.0,
    stockQuantity: 15,
    icon: "☕",
  },
  {
    menuId: 12,
    branchId: 2,
    categoryId: 1,
    name: "Americano (อเมริกาโน่)",
    price: 40.0,
    stockQuantity: 25,
    icon: "☕",
  },
  {
    menuId: 13,
    branchId: 2,
    categoryId: 2,
    name: "Thai Milk Tea (ชาไทยเย็น)",
    price: 40.0,
    stockQuantity: 18,
    icon: "🧋",
  },
  {
    menuId: 14,
    branchId: 2,
    categoryId: 3,
    name: "Butter Croissant (ครัวซองต์)",
    price: 55.0,
    stockQuantity: 5,
    icon: "🥐",
  },
];

const DEFAULT_ORDERS = [
  {
    orderId: 101,
    branchId: 1,
    employeeId: 1,
    paymentMethod: "Cash",
    createdAt: "2026-10-25 09:15:00",
    totalAmount: 80.0,
    items: [
      {
        menuId: 1,
        name: "Latte (ลาเต้ร้อน/เย็น)",
        quantity: 1,
        unitPrice: 45.0,
      },
      {
        menuId: 2,
        name: "Espresso (เอสเปรสโซ่)",
        quantity: 1,
        unitPrice: 35.0,
      },
    ],
  },
  {
    orderId: 102,
    branchId: 1,
    employeeId: 1,
    paymentMethod: "QR",
    createdAt: "2026-10-25 10:30:00",
    totalAmount: 140.0,
    items: [
      {
        menuId: 1,
        name: "Latte (ลาเต้ร้อน/เย็น)",
        quantity: 2,
        unitPrice: 45.0,
      },
      {
        menuId: 3,
        name: "Cappuccino (คาปูชิโน่)",
        quantity: 1,
        unitPrice: 50.0,
      },
    ],
  },
  {
    orderId: 103,
    branchId: 1,
    employeeId: 1,
    paymentMethod: "Cash",
    createdAt: "2026-10-26 11:20:00",
    totalAmount: 95.0,
    items: [
      {
        menuId: 3,
        name: "Cappuccino (คาปูชิโน่)",
        quantity: 1,
        unitPrice: 50.0,
      },
      {
        menuId: 9,
        name: "Chocolate Brownie (บราวนี่)",
        quantity: 1,
        unitPrice: 45.0,
      },
    ],
  },
  {
    orderId: 104,
    branchId: 2,
    employeeId: 2,
    paymentMethod: "Cash",
    createdAt: "2026-10-26 13:45:00",
    totalAmount: 90.0,
    items: [
      {
        menuId: 10,
        name: "Latte (ลาเต้ร้อน/เย็น)",
        quantity: 2,
        unitPrice: 45.0,
      },
    ],
  },
];

// App State
let state = {
  branchId: 1,
  activeCategory: "all",
  searchQuery: "",
  cart: [],
  paymentMethod: "Cash",
  cashReceived: null,
  menu: JSON.parse(JSON.stringify(DEFAULT_MENU)),
  orders: JSON.parse(JSON.stringify(DEFAULT_ORDERS)),
  nextOrderId: 105,
  isOnlineServer: false,
};

// Check if Backend API is available
async function checkBackendApi() {
  try {
    const res = await fetch("/api/menu?branchId=" + state.branchId);
    if (res.ok) {
      state.isOnlineServer = true;
      console.log("Connected to Minions Cafe Express Backend API");
    }
  } catch (e) {
    state.isOnlineServer = false;
    console.log("Running in Standalone Browser Client Mode");
  }
}

// ==========================================================================
// INITIALIZATION
// ==========================================================================
window.addEventListener("DOMContentLoaded", async () => {
  // Load from localStorage if present
  const savedMenu = localStorage.getItem("minions_pos_menu");
  const savedOrders = localStorage.getItem("minions_pos_orders");
  if (savedMenu) state.menu = JSON.parse(savedMenu);
  if (savedOrders) state.orders = JSON.parse(savedOrders);

  await checkBackendApi();
  renderAll();
});

function saveLocalState() {
  localStorage.setItem("minions_pos_menu", JSON.stringify(state.menu));
  localStorage.setItem("minions_pos_orders", JSON.stringify(state.orders));
}

function renderAll() {
  renderMenu();
  renderCart();
  renderMenuManagement();
  renderSalesReport();
}

// ==========================================================================
// NAVIGATION & BRANCH SWITCHING
// ==========================================================================
function switchScreen(screenKey) {
  document
    .querySelectorAll(".screen-view")
    .forEach((s) => s.classList.remove("active"));
  document
    .querySelectorAll(".nav-tab-btn")
    .forEach((b) => b.classList.remove("active"));

  document.getElementById(`screen-${screenKey}`).classList.add("active");
  document.getElementById(`tab-${screenKey}`).classList.add("active");

  if (screenKey === "menu") renderMenuManagement();
  if (screenKey === "report") renderSalesReport();
  if (screenKey === "pos") renderMenu();
}

function onBranchChange() {
  const sel = document.getElementById("branch-select");
  state.branchId = parseInt(sel.value);

  // Update cashier name based on branch
  const cashierEl = document.getElementById("cashier-name");
  if (state.branchId === 1) {
    cashierEl.textContent = "สมชาย (Cashier)";
  } else {
    cashierEl.textContent = "สมหญิง (Manager)";
  }

  // Clear cart on branch switch to prevent branch mismatch (IDOR / Consistency)
  state.cart = [];
  showToast(`สลับข้อมูลเป็นสาขา ${state.branchId} เรียบร้อยแล้ว`, "info");
  renderAll();
}

// ==========================================================================
// POS SCREEN: MENU & CART LOGIC
// ==========================================================================
function filterCategory(catId, btnElement) {
  state.activeCategory = catId;
  document
    .querySelectorAll(".cat-pill")
    .forEach((p) => p.classList.remove("active"));
  btnElement.classList.add("active");
  renderMenu();
}

function onSearchMenu(query) {
  state.searchQuery = query.trim().toLowerCase();
  renderMenu();
}

function renderMenu() {
  const grid = document.getElementById("menu-grid");
  grid.innerHTML = "";

  const filtered = state.menu.filter((m) => {
    const matchBranch = m.branchId === state.branchId;
    const matchCat =
      state.activeCategory === "all" ||
      m.categoryId === parseInt(state.activeCategory);
    const matchSearch =
      !state.searchQuery || m.name.toLowerCase().includes(state.searchQuery);
    return matchBranch && matchCat && matchSearch;
  });

  if (filtered.length === 0) {
    grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align:center; padding:50px; color:#9c8e82">
                ☕ ไม่พบรายการเมนูที่ตรงกับเงื่อนไขการค้นหา
            </div>`;
    return;
  }

  filtered.forEach((item) => {
    const isOutOfStock = item.stockQuantity <= 0;
    const isLowStock = item.stockQuantity > 0 && item.stockQuantity < 10;

    let badgeHtml = "";
    if (isOutOfStock) {
      badgeHtml = `<span class="stock-badge out">✕ สินค้าหมด</span>`;
    } else if (isLowStock) {
      badgeHtml = `<span class="stock-badge low">⚠ เหลือ ${item.stockQuantity}</span>`;
    } else {
      badgeHtml = `<span class="stock-badge normal">✓ คงเหลือ ${item.stockQuantity}</span>`;
    }

    const card = document.createElement("div");
    card.className = `menu-card ${isOutOfStock ? "out-of-stock" : ""}`;
    card.innerHTML = `
            <div class="menu-card-header">
                <div class="menu-card-icon">${item.icon || "☕"}</div>
                <div class="menu-card-info">
                    <div class="menu-card-name">${item.name}</div>
                    <div class="menu-card-price">฿${item.price.toFixed(2)}</div>
                </div>
            </div>
            <div class="menu-card-footer">
                ${badgeHtml}
                <button class="btn-add-item" 
                        onclick="addToCart(${item.menuId})" 
                        ${isOutOfStock ? 'disabled title="สินค้าหมด ไม่สามารถเพิ่มได้ (FR-11)"' : 'title="เพิ่มลงตะกร้า"'}>
                    +
                </button>
            </div>
        `;
    grid.appendChild(card);
  });
}

function addToCart(menuId) {
  const menuItem = state.menu.find(
    (m) => m.menuId === menuId && m.branchId === state.branchId,
  );
  if (!menuItem) return;

  if (menuItem.stockQuantity <= 0) {
    showToast(
      `สินค้า "${menuItem.name}" หมดสต็อกแล้ว (FR-11 Error Prevention)`,
      "error",
    );
    return;
  }

  const existing = state.cart.find((c) => c.menuId === menuId);
  if (existing) {
    if (existing.quantity + 1 > menuItem.stockQuantity) {
      showToast(
        `สต็อก "${menuItem.name}" ไม่เพียงพอ (คงเหลือ ${menuItem.stockQuantity} หน่วย)`,
        "error",
      );
      return;
    }
    existing.quantity += 1;
  } else {
    state.cart.push({
      menuId: menuItem.menuId,
      name: menuItem.name,
      price: menuItem.price,
      quantity: 1,
      maxStock: menuItem.stockQuantity,
      icon: menuItem.icon,
    });
  }

  renderCart();
  showToast(`เพิ่ม "${menuItem.name}" ลงในตะกร้าแล้ว`, "success");
}

function updateCartQty(menuId, delta) {
  const item = state.cart.find((c) => c.menuId === menuId);
  if (!item) return;

  const menuItem = state.menu.find((m) => m.menuId === menuId);
  const newQty = item.quantity + delta;

  if (newQty <= 0) {
    state.cart = state.cart.filter((c) => c.menuId !== menuId);
  } else if (newQty > menuItem.stockQuantity) {
    showToast(
      `ไม่สามารถเพิ่มเกินสต็อกคงเหลือ (${menuItem.stockQuantity} หน่วย)`,
      "error",
    );
    return;
  } else {
    item.quantity = newQty;
  }

  renderCart();
}

function removeFromCart(menuId) {
  state.cart = state.cart.filter((c) => c.menuId !== menuId);
  renderCart();
}

function clearCart() {
  if (state.cart.length === 0) return;
  state.cart = [];
  document.getElementById("cash-received-input").value = "";
  document.getElementById("cash-change-display").textContent = "฿0.00";
  renderCart();
  showToast("ล้างรายการในตะกร้าแล้ว", "info");
}

function renderCart() {
  const body = document.getElementById("cart-body");
  const badge = document.getElementById("cart-item-count");
  const subtotalEl = document.getElementById("cart-subtotal");
  const totalEl = document.getElementById("cart-total");
  const confirmBtn = document.getElementById("btn-confirm-order");

  let totalItems = 0;
  let totalAmount = 0;

  if (state.cart.length === 0) {
    body.innerHTML = `
            <div class="empty-cart-msg">
                🛒 ยังไม่มีรายการสินค้าในตะกร้า<br>
                <small>คลิกปุ่ม <b>+</b> ที่เมนูด้านซ้ายเพื่อเพิ่มรายการ</small>
            </div>`;
    confirmBtn.disabled = true;
  } else {
    body.innerHTML = "";
    state.cart.forEach((item) => {
      const itemSubtotal = item.quantity * item.price;
      totalItems += item.quantity;
      totalAmount += itemSubtotal;

      const row = document.createElement("div");
      row.className = "cart-item-row";
      row.innerHTML = `
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">฿${item.price.toFixed(2)} x ${item.quantity}</div>
                </div>
                <div class="stepper">
                    <button class="stepper-btn" onclick="updateCartQty(${item.menuId}, -1)">-</button>
                    <span class="stepper-val">${item.quantity}</span>
                    <button class="stepper-btn" onclick="updateCartQty(${item.menuId}, 1)">+</button>
                </div>
                <div class="cart-item-subtotal">฿${itemSubtotal.toFixed(2)}</div>
                <button class="cart-item-del" onclick="removeFromCart(${item.menuId})" title="ลบรายการ">✕</button>
            `;
      body.appendChild(row);
    });

    confirmBtn.disabled = false;
  }

  badge.textContent = `${totalItems} รายการ`;
  subtotalEl.textContent = `฿${totalAmount.toFixed(2)}`;
  totalEl.textContent = `฿${totalAmount.toFixed(2)}`;

  calculateChange();
}

function selectPaymentMethod(method) {
  state.paymentMethod = method;
  const cashCard = document.getElementById("pay-cash-card");
  const qrCard = document.getElementById("pay-qr-card");
  const cashBox = document.getElementById("cash-calc-box");

  if (method === "Cash") {
    cashCard.classList.add("active");
    qrCard.classList.remove("active");
    document.getElementById("pay-cash").checked = true;
    cashBox.style.display = "grid";
  } else {
    qrCard.classList.add("active");
    cashCard.classList.remove("active");
    document.getElementById("pay-qr").checked = true;
    cashBox.style.display = "none";
  }
}

function calculateChange() {
  if (state.paymentMethod !== "Cash") return;
  const input = document.getElementById("cash-received-input");
  const display = document.getElementById("cash-change-display");

  let totalAmount = state.cart.reduce(
    (sum, item) => sum + item.quantity * item.price,
    0,
  );
  const received = parseFloat(input.value) || 0;

  if (received >= totalAmount && totalAmount > 0) {
    const change = received - totalAmount;
    display.textContent = `฿${change.toFixed(2)}`;
    display.style.color = "var(--success)";
  } else {
    display.textContent = "฿0.00";
    display.style.color = "#7c6f64";
  }
}

// ==========================================================================
// SUBMIT ORDER & RECEIPT GENERATION
// ==========================================================================
async function submitOrder() {
  if (state.cart.length === 0) {
    showToast("กรุณาเลือกรายการสินค้าก่อนยืนยันออเดอร์", "error");
    return;
  }

  const totalAmount = state.cart.reduce(
    (sum, item) => sum + item.quantity * item.price,
    0,
  );

  // If QR Code, trigger PromptPay simulation modal
  if (state.paymentMethod === "QR") {
    document.getElementById("qr-modal-amount").textContent =
      `฿${totalAmount.toFixed(2)}`;
    document.getElementById("qr-modal").classList.add("open");
    return;
  }

  // Cash validation
  const cashInput = document.getElementById("cash-received-input");
  let cashVal = parseFloat(cashInput.value);
  if (isNaN(cashVal) || cashVal < totalAmount) {
    // default to exact amount if user didn't enter or entered lower
    cashVal = totalAmount;
    cashInput.value = totalAmount.toFixed(2);
  }

  finalizeOrderExecution(cashVal, cashVal - totalAmount);
}

function confirmQrPaymentSuccess() {
  closeQrModal();
  const totalAmount = state.cart.reduce(
    (sum, item) => sum + item.quantity * item.price,
    0,
  );
  finalizeOrderExecution(totalAmount, 0);
}

function finalizeOrderExecution(cashReceived, changeDue) {
  const totalAmount = state.cart.reduce(
    (sum, item) => sum + item.quantity * item.price,
    0,
  );
  const now = new Date();
  const nowStr = now.toISOString().replace("T", " ").substring(0, 19);
  const orderId = state.nextOrderId++;

  // Deduct stock in state (atomic execution)
  const orderItemsSnapshot = [];
  for (const item of state.cart) {
    const menuItem = state.menu.find((m) => m.menuId === item.menuId);
    if (menuItem) {
      menuItem.stockQuantity -= item.quantity;
    }
    orderItemsSnapshot.push({
      menuId: item.menuId,
      name: item.name,
      quantity: item.quantity,
      unitPrice: item.price,
      subtotal: item.quantity * item.price,
    });
  }

  // Record order
  const branchName =
    state.branchId === 1 ? "สาขา 1 (ม.บูรพา)" : "สาขา 2 (แหลมทอง)";
  const newOrder = {
    orderId: orderId,
    branchId: state.branchId,
    branchName: branchName,
    employeeName: state.branchId === 1 ? "สมชาย" : "สมหญิง",
    paymentMethod: state.paymentMethod,
    createdAt: nowStr,
    totalAmount: totalAmount,
    cashReceived: cashReceived,
    changeDue: changeDue,
    items: orderItemsSnapshot,
  };
  state.orders.push(newOrder);

  // Persist
  saveLocalState();

  // Show Receipt Modal
  displayReceiptModal(newOrder);

  // Clear cart and re-render
  state.cart = [];
  document.getElementById("cash-received-input").value = "";
  document.getElementById("cash-change-display").textContent = "฿0.00";
  renderMenu();
  renderCart();
  renderMenuManagement();
  renderSalesReport();

  showToast(
    `ยืนยันออเดอร์ ORD-${orderId} สำเร็จ และตัดสต็อกเรียบร้อย!`,
    "success",
  );
}

function displayReceiptModal(order) {
  const pad = (n) => String(n).padStart(2, "0");
  const now = new Date(order.createdAt);
  const dateFormatted = `${pad(now.getDate())}/${pad(now.getMonth() + 1)}/${now.getFullYear()} ${pad(now.getHours())}:${pad(now.getMinutes())}`;

  document.getElementById("rec-branch-name").textContent =
    order.branchName || `สาขา ${order.branchId}`;
  document.getElementById("rec-order-no").textContent =
    `ORD-${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${String(order.orderId).padStart(3, "0")}`;
  document.getElementById("rec-datetime").textContent = dateFormatted;
  document.getElementById("rec-cashier").textContent =
    order.employeeName || "สมชาย";
  document.getElementById("rec-total-amount").textContent =
    `฿${order.totalAmount.toFixed(2)}`;
  document.getElementById("rec-payment-method").textContent =
    order.paymentMethod === "Cash" ? "เงินสด (Cash)" : "QR Code พร้อมเพย์";

  const cashRow = document.getElementById("rec-cash-details-row");
  if (order.paymentMethod === "Cash") {
    cashRow.style.display = "flex";
    document.getElementById("rec-cash-change").textContent =
      `฿${order.cashReceived.toFixed(2)} / ฿${order.changeDue.toFixed(2)}`;
  } else {
    cashRow.style.display = "none";
  }

  const tbody = document.getElementById("rec-items-body");
  tbody.innerHTML = "";
  order.items.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td>${item.name}</td>
            <td style="text-align:center">${item.quantity}</td>
            <td style="text-align:right">฿${item.subtotal.toFixed(2)}</td>
        `;
    tbody.appendChild(tr);
  });

  document.getElementById("receipt-modal").classList.add("open");
}

function closeReceiptModal() {
  document.getElementById("receipt-modal").classList.remove("open");
}

function closeQrModal() {
  document.getElementById("qr-modal").classList.remove("open");
}

function printReceiptArea() {
  window.print();
}

// ==========================================================================
// SCREEN 2: MENU & STOCK MANAGEMENT
// ==========================================================================
function renderMenuManagement() {
  const tbody = document.getElementById("menu-table-body");
  if (!tbody) return;
  tbody.innerHTML = "";

  const branchItems = state.menu.filter((m) => m.branchId === state.branchId);

  branchItems.forEach((item) => {
    let statusTag = "";
    if (item.stockQuantity <= 0) {
      statusTag = `<span class="stock-badge out">✕ สินค้าหมด</span>`;
    } else if (item.stockQuantity < 10) {
      statusTag = `<span class="stock-badge low">⚠ เหลือ ${item.stockQuantity}</span>`;
    } else {
      statusTag = `<span class="stock-badge normal">✓ ปกติ (${item.stockQuantity})</span>`;
    }

    const catNames = { 1: "กาแฟ", 2: "ชา", 3: "เบเกอรี่" };

    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td style="font-weight:600; color:#8c7e72">#${item.menuId}</td>
            <td style="font-size:1.4rem">${item.icon || "☕"}</td>
            <td style="font-weight:600">${item.name}</td>
            <td>${catNames[item.categoryId] || "ทั่วไป"}</td>
            <td style="font-weight:700; color:var(--primary)">฿${item.price.toFixed(2)}</td>
            <td style="font-weight:700">${item.stockQuantity} หน่วย</td>
            <td>${statusTag}</td>
            <td style="text-align: right">
                <button class="table-action-btn" onclick="openStockModal(${item.menuId})">⚡ ปรับสต็อก</button>
                <button class="table-action-btn" onclick="promptEditPrice(${item.menuId})">✏️ แก้ไขราคา</button>
                <button class="table-action-btn" style="color:var(--danger)" onclick="deleteMenuItem(${item.menuId})">🗑 ลบ</button>
            </td>
        `;
    tbody.appendChild(tr);
  });
}

let activeStockMenuId = null;
function openStockModal(menuId) {
  activeStockMenuId = menuId;
  const item = state.menu.find((m) => m.menuId === menuId);
  if (!item) return;

  document.getElementById("stock-modal-item-name").textContent =
    `เมนู: ${item.name} (สต็อกปัจจุบัน: ${item.stockQuantity})`;
  document.getElementById("stock-modal-input").value = item.stockQuantity;
  document.getElementById("stock-modal").classList.add("open");
}

function closeStockModal() {
  document.getElementById("stock-modal").classList.remove("open");
}

function saveStockAdjustment() {
  const input = document.getElementById("stock-modal-input");
  const val = parseInt(input.value);
  if (isNaN(val) || val < 0) {
    showToast("กรุณากรอกตัวเลขสต็อกที่ถูกต้อง (ไม่ต่ำกว่า 0)", "error");
    return;
  }

  const item = state.menu.find((m) => m.menuId === activeStockMenuId);
  if (item) {
    item.stockQuantity = val;
    saveLocalState();
    closeStockModal();
    renderAll();
    showToast(
      `ปรับปรุงสต็อกของ "${item.name}" เป็น ${val} หน่วยสำเร็จ`,
      "success",
    );
  }
}

function promptEditPrice(menuId) {
  const item = state.menu.find((m) => m.menuId === menuId);
  if (!item) return;
  const newPrice = prompt(`แก้ไขราคาของ "${item.name}" (บาท):`, item.price);
  if (newPrice !== null) {
    const p = parseFloat(newPrice);
    if (!isNaN(p) && p > 0) {
      item.price = p;
      saveLocalState();
      renderAll();
      showToast(`ปรับปรุงราคาเป็น ฿${p.toFixed(2)} เรียบร้อย`, "success");
    } else {
      showToast("ราคาต้องเป็นตัวเลขมากกว่า 0", "error");
    }
  }
}

function deleteMenuItem(menuId) {
  const item = state.menu.find((m) => m.menuId === menuId);
  if (!item) return;
  if (confirm(`คุณต้องการลบเมนู "${item.name}" ใช่หรือไม่?`)) {
    state.menu = state.menu.filter((m) => m.menuId !== menuId);
    saveLocalState();
    renderAll();
    showToast("ลบรายการเมนูสำเร็จ", "info");
  }
}

function openAddMenuModal() {
  document.getElementById("add-menu-name").value = "";
  document.getElementById("add-menu-price").value = "";
  document.getElementById("add-menu-stock").value = "";
  document.getElementById("add-menu-modal").classList.add("open");
}

function closeAddMenuModal() {
  document.getElementById("add-menu-modal").classList.remove("open");
}

function submitNewMenu() {
  const name = document.getElementById("add-menu-name").value.trim();
  const catId = parseInt(document.getElementById("add-menu-category").value);
  const icon = document.getElementById("add-menu-icon").value;
  const price = parseFloat(document.getElementById("add-menu-price").value);
  const stock = parseInt(document.getElementById("add-menu-stock").value);

  if (!name || isNaN(price) || isNaN(stock) || price <= 0 || stock < 0) {
    showToast("กรุณากรอกข้อมูลให้ครบถ้วนและถูกต้อง", "error");
    return;
  }

  const nextId = Math.max(...state.menu.map((m) => m.menuId), 10) + 1;
  const newItem = {
    menuId: nextId,
    branchId: state.branchId,
    categoryId: catId,
    name: name,
    price: price,
    stockQuantity: stock,
    icon: icon,
  };

  state.menu.push(newItem);
  saveLocalState();
  closeAddMenuModal();
  renderAll();
  showToast(
    `เพิ่มเมนู "${name}" สำหรับสาขา ${state.branchId} เรียบร้อย`,
    "success",
  );
}

// ==========================================================================
// SCREEN 3: SALES REPORT (REAL-TIME SUMMARY)
// ==========================================================================
function renderSalesReport() {
  const branchOrders = state.orders.filter(
    (o) => o.branchId === state.branchId,
  );
  let totalSales = 0;
  let totalOrders = branchOrders.length;
  let totalCups = 0;
  const itemStats = {};

  branchOrders.forEach((o) => {
    totalSales += o.totalAmount;
    if (o.items && Array.isArray(o.items)) {
      o.items.forEach((it) => {
        totalCups += it.quantity;
        if (!itemStats[it.menuId]) {
          itemStats[it.menuId] = {
            name: it.name,
            unitPrice: it.unitPrice,
            quantitySold: 0,
            totalRevenue: 0,
          };
        }
        itemStats[it.menuId].quantitySold += it.quantity;
        itemStats[it.menuId].totalRevenue += it.quantity * it.unitPrice;
      });
    }
  });

  const breakdownList = Object.values(itemStats).sort(
    (a, b) => b.quantitySold - a.quantitySold,
  );
  const bestSeller = breakdownList.length > 0 ? breakdownList[0] : null;

  // Update KPIs
  document.getElementById("kpi-total-sales").textContent =
    `฿${totalSales.toLocaleString("th-TH", { minimumFractionDigits: 2 })}`;
  document.getElementById("kpi-total-orders").textContent =
    `${totalOrders} รายการ`;
  document.getElementById("kpi-best-seller").textContent = bestSeller
    ? `${bestSeller.name} (${bestSeller.quantitySold} แก้ว)`
    : "ยังไม่มีข้อมูล";
  document.getElementById("kpi-total-cups").textContent = `${totalCups} แก้ว`;

  // Render Breakdown Table
  const breakdownTbody = document.getElementById("report-breakdown-body");
  if (breakdownTbody) {
    breakdownTbody.innerHTML = "";
    if (breakdownList.length === 0) {
      breakdownTbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:#8c7e72; padding:20px">ยังไม่มีข้อมูลยอดขายในสาขานี้</td></tr>`;
    } else {
      breakdownList.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
                    <td style="font-weight:600">${item.name}</td>
                    <td>฿${item.unitPrice.toFixed(2)}</td>
                    <td style="font-weight:700">${item.quantitySold}</td>
                    <td style="font-weight:700; color:var(--primary)">฿${item.totalRevenue.toFixed(2)}</td>
                `;
        breakdownTbody.appendChild(tr);
      });
    }
  }

  // Branch Comparison Calculation
  const b1Sales = state.orders
    .filter((o) => o.branchId === 1)
    .reduce((sum, o) => sum + o.totalAmount, 0);
  const b2Sales = state.orders
    .filter((o) => o.branchId === 2)
    .reduce((sum, o) => sum + o.totalAmount, 0);
  const maxB = Math.max(b1Sales, b2Sales, 1);

  document.getElementById("comp-branch-1-sales").textContent =
    `฿${b1Sales.toFixed(2)}`;
  document.getElementById("comp-branch-2-sales").textContent =
    `฿${b2Sales.toFixed(2)}`;
  document.getElementById("comp-branch-1-bar").style.width =
    `${Math.min(100, (b1Sales / maxB) * 100)}%`;
  document.getElementById("comp-branch-2-bar").style.width =
    `${Math.min(100, (b2Sales / maxB) * 100)}%`;

  // Recent orders list
  const recentList = document.getElementById("recent-orders-list");
  if (recentList) {
    recentList.innerHTML = "";
    const recent = [...branchOrders].reverse().slice(0, 5);
    if (recent.length === 0) {
      recentList.innerHTML = `<div style="color:#8c7e72; font-size:0.85rem">ไม่มีออเดอร์ล่าสุด</div>`;
    } else {
      recent.forEach((ord) => {
        const itemDiv = document.createElement("div");
        itemDiv.style.cssText =
          "display:flex; justify-content:space-between; align-items:center; background:#fdfbf7; padding:8px 12px; border-radius:6px; font-size:0.85rem; border:1px solid #e7dfd5";
        itemDiv.innerHTML = `
                    <div>
                        <b>ORD-${ord.orderId}</b> · <span style="color:#7c6f64">${ord.paymentMethod}</span><br>
                        <small style="color:#94a3b8">${ord.createdAt}</small>
                    </div>
                    <div style="text-align:right">
                        <div style="font-weight:700; color:var(--primary)">฿${ord.totalAmount.toFixed(2)}</div>
                        <button class="table-action-btn" style="font-size:0.75rem; padding:2px 6px" onclick='displayReceiptModal(${JSON.stringify(ord)})'>ดูใบเสร็จ</button>
                    </div>
                `;
        recentList.appendChild(itemDiv);
      });
    }
  }
}

function exportReportCSV() {
  let csv = "Menu,Price,Quantity Sold,Total Revenue\n";
  const branchOrders = state.orders.filter(
    (o) => o.branchId === state.branchId,
  );
  const itemStats = {};

  branchOrders.forEach((o) => {
    if (o.items) {
      o.items.forEach((it) => {
        if (!itemStats[it.name])
          itemStats[it.name] = { price: it.unitPrice, qty: 0, rev: 0 };
        itemStats[it.name].qty += it.quantity;
        itemStats[it.name].rev += it.quantity * it.unitPrice;
      });
    }
  });

  Object.keys(itemStats).forEach((name) => {
    const it = itemStats[name];
    csv += `"${name}",${it.price},${it.qty},${it.rev}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `sales-report-branch-${state.branchId}.csv`;
  a.click();
  showToast("ดาวน์โหลดรายงาน CSV สำเร็จ", "success");
}

// ==========================================================================
// WK15 LIVE DEMO CONTROLLER (5-8 MINUTE STEP-BY-STEP SEQUENCE)
// ==========================================================================
function demoStep(step) {
  if (step === 1) {
    // Step 1: Open POS Screen & Show Menu
    switchScreen("pos");
    showToast(
      "ขั้นตอนที่ 1: เปิดหน้าจอ POS แสดงรายการเมนูและตัวเลือกสาขา",
      "info",
    );
  } else if (step === 2) {
    // Step 2: Auto-select 2-3 items and calculate live total
    switchScreen("pos");
    clearCart();
    addToCart(1); // Latte 45
    addToCart(2); // Espresso 35
    addToCart(8); // Croissant 55
    showToast(
      "ขั้นตอนที่ 2: สั่งซื้อ Latte + Espresso + Croissant คำนวณยอดรวม ฿135.00 สดอัตโนมัติ!",
      "success",
    );
  } else if (step === 3) {
    // Step 3: Confirm Order & Show Generated Receipt
    switchScreen("pos");
    if (state.cart.length === 0) {
      addToCart(1);
      addToCart(2);
    }
    selectPaymentMethod("Cash");
    document.getElementById("cash-received-input").value = "200.00";
    calculateChange();
    submitOrder();
    showToast(
      "ขั้นตอนที่ 3: ยืนยันออเดอร์ ตัดสต็อก และแสดงใบเสร็จรับเงินที่ระบบสร้างขึ้น",
      "success",
    );
  } else if (step === 4) {
    // Step 4: Open Sales Report immediately showing new order
    closeReceiptModal();
    switchScreen("report");
    showToast(
      "ขั้นตอนที่ 4: เปิดหน้ารายงานยอดขาย พบว่ายอดขายรวมและรายการขายอัปเดตทันที!",
      "success",
    );
  } else if (step === 5) {
    // Step 5: Test Out-of-Stock scenario (Business logic verification)
    switchScreen("pos");
    clearCart();
    showToast(
      "ขั้นตอนที่ 5: ทดสอบความปลอดภัย - ลองคลิกเมนู Lemon Tea (สต็อก 0) ระบบจะป้องกันและปิดปุ่มตาม FR-11",
      "error",
    );
    // highlight Lemon Tea card
    const searchInput = document.getElementById("pos-search-input");
    searchInput.value = "Lemon";
    onSearchMenu("Lemon");
  }
}

function demoResetData() {
  state.menu = JSON.parse(JSON.stringify(DEFAULT_MENU));
  state.orders = JSON.parse(JSON.stringify(DEFAULT_ORDERS));
  state.cart = [];
  state.nextOrderId = 105;
  saveLocalState();
  renderAll();
  switchScreen("pos");
  document.getElementById("pos-search-input").value = "";
  onSearchMenu("");
  showToast(
    "🔄 รีเซ็ตข้อมูล Demo กลับสู่ค่าเริ่มต้นเรียบร้อย พร้อมสำหรับการนำเสนอ!",
    "success",
  );
}

// ==========================================================================
// TOAST NOTIFICATION UTILITY
// ==========================================================================
let toastTimer = null;
function showToast(msg, type = "info") {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = `toast-box show ${type}`;

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove("show");
  }, 3500);
}
