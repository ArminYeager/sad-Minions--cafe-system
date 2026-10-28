const express = require("express");
const cors = require("cors");
const path = require("path");
const { Order, OrderItem } = require("./models/orderModel");
const { MenuItem } = require("./models/menuModel");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Seed Data
let branches = [
  {
    branch_id: 1,
    name: "สาขา 1 (สาขาหลัก - ม.บูรพา)",
    address: "169 ถ.ลงหาดบางแสน ต.แสนสุข อ.เมือง ชลบุรี",
  },
  {
    branch_id: 2,
    name: "สาขา 2 (สาขาที่ 2 - แหลมทอง)",
    address: "ถ.สุขุมวิท ต.เสม็ด อ.เมือง ชลบุรี",
  },
];

let categories = [
  { category_id: 1, name: "กาแฟ (Coffee)" },
  { category_id: 2, name: "ชา (Tea)" },
  { category_id: 3, name: "เบเกอรี่ (Bakery)" },
];

let employees = [
  { employee_id: 1, branch_id: 1, name: "สมชาย พนักงานขาย", role: "Cashier" },
  { employee_id: 2, branch_id: 2, name: "สมหญิง ผู้จัดการ", role: "Manager" },
];

const INITIAL_MENU = [
  // Branch 1
  {
    menu_id: 1,
    branch_id: 1,
    category_id: 1,
    name: "Latte (ลาเต้ร้อน/เย็น)",
    price: 45.0,
    stock_quantity: 12,
    icon: "☕",
  },
  {
    menu_id: 2,
    branch_id: 1,
    category_id: 1,
    name: "Espresso (เอสเปรสโซ่)",
    price: 35.0,
    stock_quantity: 8,
    icon: "☕",
  },
  {
    menu_id: 3,
    branch_id: 1,
    category_id: 1,
    name: "Cappuccino (คาปูชิโน่)",
    price: 50.0,
    stock_quantity: 15,
    icon: "☕",
  },
  {
    menu_id: 4,
    branch_id: 1,
    category_id: 1,
    name: "Americano (อเมริกาโน่)",
    price: 40.0,
    stock_quantity: 20,
    icon: "☕",
  },
  {
    menu_id: 5,
    branch_id: 1,
    category_id: 2,
    name: "Matcha Green Tea (ชาเขียวมัทฉะ)",
    price: 50.0,
    stock_quantity: 10,
    icon: "🍵",
  },
  {
    menu_id: 6,
    branch_id: 1,
    category_id: 2,
    name: "Thai Milk Tea (ชาไทยเย็น)",
    price: 40.0,
    stock_quantity: 14,
    icon: "🧋",
  },
  {
    menu_id: 7,
    branch_id: 1,
    category_id: 2,
    name: "Lemon Tea (ชามะนาวเย็น)",
    price: 45.0,
    stock_quantity: 0,
    icon: "🍋",
  }, // Out of stock for FR-11 test
  {
    menu_id: 8,
    branch_id: 1,
    category_id: 3,
    name: "Butter Croissant (ครัวซองต์เนยสด)",
    price: 55.0,
    stock_quantity: 9,
    icon: "🥐",
  },
  {
    menu_id: 9,
    branch_id: 1,
    category_id: 3,
    name: "Chocolate Brownie (บราวนี่)",
    price: 45.0,
    stock_quantity: 16,
    icon: "🍫",
  },

  // Branch 2
  {
    menu_id: 10,
    branch_id: 2,
    category_id: 1,
    name: "Latte (ลาเต้ร้อน/เย็น)",
    price: 45.0,
    stock_quantity: 22,
    icon: "☕",
  },
  {
    menu_id: 11,
    branch_id: 2,
    category_id: 1,
    name: "Espresso (เอสเปรสโซ่)",
    price: 35.0,
    stock_quantity: 15,
    icon: "☕",
  },
  {
    menu_id: 12,
    branch_id: 2,
    category_id: 1,
    name: "Americano (อเมริกาโน่)",
    price: 40.0,
    stock_quantity: 25,
    icon: "☕",
  },
  {
    menu_id: 13,
    branch_id: 2,
    category_id: 2,
    name: "Thai Milk Tea (ชาไทยเย็น)",
    price: 40.0,
    stock_quantity: 18,
    icon: "🧋",
  },
  {
    menu_id: 14,
    branch_id: 2,
    category_id: 3,
    name: "Butter Croissant (ครัวซองต์)",
    price: 55.0,
    stock_quantity: 5,
    icon: "🥐",
  },
];

let menuItems = JSON.parse(JSON.stringify(INITIAL_MENU));

// Historical Seed Orders matching WK10 Report Specification
let orders = [
  {
    order_id: 101,
    branch_id: 1,
    employee_id: 1,
    payment_method: "Cash",
    created_at: "2026-10-25 09:15:00",
    total_amount: 80.0,
  },
  {
    order_id: 102,
    branch_id: 1,
    employee_id: 1,
    payment_method: "QR",
    created_at: "2026-10-25 10:30:00",
    total_amount: 140.0,
  },
  {
    order_id: 103,
    branch_id: 1,
    employee_id: 1,
    payment_method: "Cash",
    created_at: "2026-10-26 11:20:00",
    total_amount: 95.0,
  },
  {
    order_id: 104,
    branch_id: 2,
    employee_id: 2,
    payment_method: "Cash",
    created_at: "2026-10-26 13:45:00",
    total_amount: 90.0,
  },
];

let orderItems = [
  {
    order_item_id: 1,
    order_id: 101,
    menu_id: 1,
    quantity: 1,
    unit_price: 45.0,
  },
  {
    order_item_id: 2,
    order_id: 101,
    menu_id: 2,
    quantity: 1,
    unit_price: 35.0,
  },
  {
    order_item_id: 3,
    order_id: 102,
    menu_id: 1,
    quantity: 2,
    unit_price: 45.0,
  },
  {
    order_item_id: 4,
    order_id: 102,
    menu_id: 3,
    quantity: 1,
    unit_price: 50.0,
  },
  {
    order_item_id: 5,
    order_id: 103,
    menu_id: 3,
    quantity: 1,
    unit_price: 50.0,
  },
  {
    order_item_id: 6,
    order_id: 103,
    menu_id: 9,
    quantity: 1,
    unit_price: 45.0,
  },
  {
    order_item_id: 7,
    order_id: 104,
    menu_id: 10,
    quantity: 2,
    unit_price: 45.0,
  },
];

let stockMovements = [];

// Helper: Get next order id
let nextOrderId = 105;
let nextOrderItemId = 8;
let nextMenuId = 15;

// API Routes

// 1. GET /api/branches
app.get("/api/branches", (req, res) => {
  res.json(branches);
});

// 2. GET /api/categories
app.get("/api/categories", (req, res) => {
  res.json(categories);
});

// 3. GET /api/menu
// Query parameters: branch_id (required/recommended), category_id (optional), search (optional)
app.get("/api/menu", (req, res) => {
  const branchId = parseInt(req.query.branchId || req.query.branch_id || "1");
  const categoryId = req.query.categoryId || req.query.category_id;
  const search = req.query.search ? req.query.search.toLowerCase() : "";

  let result = menuItems.filter((m) => m.branch_id === branchId);

  if (categoryId && categoryId !== "all") {
    result = result.filter((m) => m.category_id === parseInt(categoryId));
  }

  if (search) {
    result = result.filter((m) => m.name.toLowerCase().includes(search));
  }

  // Map to camelCase response matching API contract (wk09, wk13)
  const formatted = result.map((item) => ({
    menuId: item.menu_id,
    branchId: item.branch_id,
    categoryId: item.category_id,
    name: item.name,
    price: item.price,
    stockQuantity: item.stock_quantity,
    icon: item.icon,
    isLowStock: item.stock_quantity > 0 && item.stock_quantity < 10,
    isOutOfStock: item.stock_quantity <= 0,
  }));

  res.json(formatted);
});

// 4. POST /api/menu (Add Menu)
app.post("/api/menu", (req, res) => {
  const { branchId, categoryId, name, price, stockQuantity, icon } = req.body;

  if (
    !branchId ||
    !categoryId ||
    !name ||
    price == null ||
    stockQuantity == null
  ) {
    return res.status(400).json({ error: "กรุณากรอกข้อมูลเมนูให้ครบถ้วน" });
  }

  const newItem = {
    menu_id: nextMenuId++,
    branch_id: parseInt(branchId),
    category_id: parseInt(categoryId),
    name: name.trim(),
    price: parseFloat(price),
    stock_quantity: parseInt(stockQuantity),
    icon: icon || "☕",
  };

  menuItems.push(newItem);
  res.status(201).json({
    success: true,
    message: "เพิ่มเมนูสำเร็จ",
    menuItem: {
      menuId: newItem.menu_id,
      branchId: newItem.branch_id,
      name: newItem.name,
      price: newItem.price,
      stockQuantity: newItem.stock_quantity,
    },
  });
});

// 5. PUT /api/menu/:id (Update Menu - with IDOR prevention using branchId)
app.put("/api/menu/:id", (req, res) => {
  const menuId = parseInt(req.params.id);
  const { branchId, price, stockQuantity, name } = req.body;

  const item = menuItems.find((m) => m.menu_id === menuId);
  if (!item) {
    return res.status(404).json({ error: "ไม่พบเมนูที่ระบุ" });
  }

  // IDOR Protection: Must match branchId
  if (branchId && item.branch_id !== parseInt(branchId)) {
    return res
      .status(403)
      .json({
        error:
          "ปฏิเสธการเข้าถึง: ไม่สามารถแก้ไขข้อมูลข้ามสาขาได้ (IDOR Protection)",
      });
  }

  if (name !== undefined) item.name = name;
  if (price !== undefined) item.price = parseFloat(price);
  if (stockQuantity !== undefined)
    item.stock_quantity = parseInt(stockQuantity);

  res.json({
    success: true,
    message: "อัปเดตข้อมูลเมนูสำเร็จ",
    menuItem: {
      menuId: item.menu_id,
      branchId: item.branch_id,
      name: item.name,
      price: item.price,
      stockQuantity: item.stock_quantity,
    },
  });
});

// 6. POST /api/orders (Create Order & Deduct Stock - with Transaction / Row-locking logic)
app.post("/api/orders", (req, res) => {
  const { branchId, employeeId, paymentMethod, items, cashReceived } = req.body;

  // Validation
  if (!branchId || !items || !Array.isArray(items) || items.length === 0) {
    return res
      .status(400)
      .json({ error: "ข้อมูลคำสั่งซื้อไม่ถูกต้อง หรือไม่มีรายการสินค้า" });
  }

  if (!paymentMethod || !["Cash", "QR"].includes(paymentMethod)) {
    return res
      .status(400)
      .json({ error: "กรุณาเลือกวิธีชำระเงิน (Cash หรือ QR)" });
  }

  // Transaction Simulation: Atomic Check & Deduct
  const parsedBranchId = parseInt(branchId);
  const orderItemsRecord = [];
  let calculatedTotal = 0;

  // Check stock for all items first (Simulating SELECT ... FOR UPDATE)
  for (const item of items) {
    const menuItem = menuItems.find(
      (m) =>
        m.menu_id === parseInt(item.menuId) && m.branch_id === parsedBranchId,
    );

    if (!menuItem) {
      return res
        .status(404)
        .json({ error: `ไม่พบเมนูรหัส ${item.menuId} ในสาขานี้` });
    }

    const requestedQty = parseInt(item.quantity);
    if (requestedQty <= 0) {
      return res.status(400).json({ error: "จำนวนสินค้าต้องมากกว่า 0" });
    }

    if (menuItem.stock_quantity < requestedQty) {
      return res.status(400).json({
        error: `สินค้า "${menuItem.name}" สต็อกไม่เพียงพอ (ต้องการ ${requestedQty}, คงเหลือ ${menuItem.stock_quantity})`,
        menuId: menuItem.menu_id,
        availableStock: menuItem.stock_quantity,
      });
    }

    const subtotal = requestedQty * menuItem.price;
    calculatedTotal += subtotal;

    orderItemsRecord.push({
      menuItem,
      quantity: requestedQty,
      unitPrice: menuItem.price,
      subtotal,
    });
  }

  // Cash validation if paymentMethod is Cash
  let changeDue = 0;
  if (paymentMethod === "Cash" && cashReceived !== undefined) {
    const received = parseFloat(cashReceived);
    if (received < calculatedTotal) {
      return res
        .status(400)
        .json({
          error: `ยอดเงินที่รับมา (฿${received}) น้อยกว่ายอดรวม (฿${calculatedTotal})`,
        });
    }
    changeDue = received - calculatedTotal;
  }

  // Deduct stock and commit transaction
  const orderId = nextOrderId++;
  const now = new Date();
  const createdAtStr = now.toISOString().replace("T", " ").substring(0, 19);

  const newOrder = {
    order_id: orderId,
    branch_id: parsedBranchId,
    employee_id: employeeId || 1,
    payment_method: paymentMethod,
    created_at: createdAtStr,
    total_amount: calculatedTotal,
    cash_received: cashReceived ? parseFloat(cashReceived) : calculatedTotal,
    change_due: changeDue,
  };

  orders.push(newOrder);

  // Add order items & deduct stock
  const createdItems = [];
  for (const rec of orderItemsRecord) {
    rec.menuItem.stock_quantity -= rec.quantity;

    const newOrderItem = {
      order_item_id: nextOrderItemId++,
      order_id: orderId,
      menu_id: rec.menuItem.menu_id,
      quantity: rec.quantity,
      unit_price: rec.unitPrice,
    };
    orderItems.push(newOrderItem);

    stockMovements.push({
      movement_id: stockMovements.length + 1,
      menu_id: rec.menuItem.menu_id,
      quantity_change: -rec.quantity,
      moved_at: createdAtStr,
    });

    createdItems.push({
      menuId: rec.menuItem.menu_id,
      name: rec.menuItem.name,
      quantity: rec.quantity,
      unitPrice: rec.unitPrice,
      subtotal: rec.subtotal,
    });
  }

  const branch = branches.find((b) => b.branch_id === parsedBranchId);
  const employee = employees.find((e) => e.employee_id === (employeeId || 1));

  // Formatted Receipt Output (WK10 Specification)
  const receipt = {
    receiptNo: `ORD-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}-${String(orderId).padStart(3, "0")}`,
    orderId: orderId,
    branchId: parsedBranchId,
    branchName: branch ? branch.name : `สาขา ${parsedBranchId}`,
    branchAddress: branch ? branch.address : "",
    employeeName: employee ? employee.name : "สมชาย (Cashier)",
    createdAt: createdAtStr,
    items: createdItems,
    totalAmount: calculatedTotal,
    paymentMethod: paymentMethod,
    cashReceived: cashReceived ? parseFloat(cashReceived) : calculatedTotal,
    changeDue: changeDue,
  };

  res.status(201).json({
    success: true,
    message: "บันทึกออเดอร์และตัดสต็อกสำเร็จ",
    orderId: orderId,
    receipt: receipt,
  });
});

// 7. GET /api/reports/sales (Summary Sales Report - WK10, WK13)
app.get("/api/reports/sales", (req, res) => {
  const branchId = req.query.branchId || req.query.branch_id;
  const fromDate = req.query.from;
  const toDate = req.query.to;

  let filteredOrders = orders;
  if (branchId && branchId !== "all") {
    filteredOrders = filteredOrders.filter(
      (o) => o.branch_id === parseInt(branchId),
    );
  }

  const orderIds = filteredOrders.map((o) => o.order_id);
  const relevantItems = orderItems.filter((oi) =>
    orderIds.includes(oi.order_id),
  );

  // Summary KPIs
  let totalSales = 0;
  let totalQuantity = 0;
  const menuStats = {};

  for (const item of relevantItems) {
    const subtotal = item.quantity * item.unit_price;
    totalSales += subtotal;
    totalQuantity += item.quantity;

    if (!menuStats[item.menu_id]) {
      const menuDef = menuItems.find((m) => m.menu_id === item.menu_id);
      menuStats[item.menu_id] = {
        menuId: item.menu_id,
        name: menuDef ? menuDef.name : `เมนู ${item.menu_id}`,
        icon: menuDef ? menuDef.icon : "☕",
        unitPrice: item.unit_price,
        totalSoldQuantity: 0,
        totalRevenue: 0,
      };
    }
    menuStats[item.menu_id].totalSoldQuantity += item.quantity;
    menuStats[item.menu_id].totalRevenue += subtotal;
  }

  const breakdown = Object.values(menuStats).sort(
    (a, b) => b.totalSoldQuantity - a.totalSoldQuantity,
  );
  const bestSeller = breakdown.length > 0 ? breakdown[0] : null;

  res.json({
    branchId: branchId || "all",
    totalSales: totalSales,
    totalOrders: filteredOrders.length,
    totalQuantitySold: totalQuantity,
    bestSeller: bestSeller
      ? {
          menuId: bestSeller.menuId,
          name: bestSeller.name,
          icon: bestSeller.icon,
          quantitySold: bestSeller.totalSoldQuantity,
          revenue: bestSeller.totalRevenue,
        }
      : null,
    menuBreakdown: breakdown,
    recentOrders: filteredOrders.slice(-10).reverse(),
  });
});

// 8. POST /api/reset (Reset Demo Seed Data)
app.post("/api/reset", (req, res) => {
  menuItems = JSON.parse(JSON.stringify(INITIAL_MENU));
  orders = [
    {
      order_id: 101,
      branch_id: 1,
      employee_id: 1,
      payment_method: "Cash",
      created_at: "2026-10-25 09:15:00",
      total_amount: 80.0,
    },
    {
      order_id: 102,
      branch_id: 1,
      employee_id: 1,
      payment_method: "QR",
      created_at: "2026-10-25 10:30:00",
      total_amount: 140.0,
    },
    {
      order_id: 103,
      branch_id: 1,
      employee_id: 1,
      payment_method: "Cash",
      created_at: "2026-10-26 11:20:00",
      total_amount: 95.0,
    },
    {
      order_id: 104,
      branch_id: 2,
      employee_id: 2,
      payment_method: "Cash",
      created_at: "2026-10-26 13:45:00",
      total_amount: 90.0,
    },
  ];
  orderItems = [
    {
      order_item_id: 1,
      order_id: 101,
      menu_id: 1,
      quantity: 1,
      unit_price: 45.0,
    },
    {
      order_item_id: 2,
      order_id: 101,
      menu_id: 2,
      quantity: 1,
      unit_price: 35.0,
    },
    {
      order_item_id: 3,
      order_id: 102,
      menu_id: 1,
      quantity: 2,
      unit_price: 45.0,
    },
    {
      order_item_id: 4,
      order_id: 102,
      menu_id: 3,
      quantity: 1,
      unit_price: 50.0,
    },
    {
      order_item_id: 5,
      order_id: 103,
      menu_id: 3,
      quantity: 1,
      unit_price: 50.0,
    },
    {
      order_item_id: 6,
      order_id: 103,
      menu_id: 9,
      quantity: 1,
      unit_price: 45.0,
    },
    {
      order_item_id: 7,
      order_id: 104,
      menu_id: 10,
      quantity: 2,
      unit_price: 45.0,
    },
  ];
  stockMovements = [];
  nextOrderId = 105;
  res.json({
    success: true,
    message: "รีเซ็ตข้อมูลตัวอย่างสำหรับการ Demo เรียบร้อยแล้ว",
  });
});

app.listen(PORT, () => {
  console.log(`Minions Cafe POS Server running at http://localhost:${PORT}`);
});
