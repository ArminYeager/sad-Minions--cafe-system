# รายงานผลการตรวจสอบคุณภาพและความปลอดภัยของซอฟต์แวร์ (Code Quality & Security Review)
## สัปดาห์ที่ 14: การตรวจสอบคุณภาพโค้ดเทียบ Checklist และแก้ไขช่องโหว่ความปลอดภัย

**กลุ่มที่ 14:** Minions Cafe  
**วันที่ตรวจสอบ:** 25 ตุลาคม 2568  
**ผู้ตรวจสอบ:** กลุ่ม 14 Minions Cafe  
**ขอบเขต:** โค้ด Backend Routes, Controllers, และ Models ของระบบร้านกาแฟ Minions Cafe

---

## 1. วัตถุประสงค์ (Objectives)

ตรวจสอบคุณภาพซอฟต์แวร์แบบย้อนกลับ (Retrofit Review) จากโค้ดจริงที่พัฒนามาตลอดเทอม เพื่อค้นหาช่องโหว่ความปลอดภัยและจุดบกพร่องตาม **Code Review Checklist 5 ข้อ** สำหรับระบบ CRUD ขนาดเล็ก ได้แก่:
1. Input Validation
2. Insecure Direct Object Reference (IDOR)
3. SQL Injection Prevention
4. Error Handling Consistency
5. Race Condition in Read-Modify-Write Operations

---

## 2. ผลการตรวจสอบ Endpoint เทียบ Checklist

| Endpoint | HTTP Method | 1. Input Validation | 2. IDOR Prevention | 3. SQL Injection | 4. Error Handling | 5. Race Condition | สรุปผล |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `/api/menu` | `GET` | ผ่าน | ผ่าน (`branch_id`) | ผ่าน (`?`) | ผ่าน | ไม่เกี่ยวข้อง | ผ่าน |
| `/api/menu` | `POST` | ผ่าน | ผ่าน | ผ่าน (`?`) | ผ่าน | ไม่เกี่ยวข้อง | ผ่าน |
| `/api/menu/:id` | `PUT` | ผ่าน | **ไม่ผ่าน (เดิม)** | ผ่าน (`?`) | ผ่าน | ไม่เกี่ยวข้อง | **มีความเสี่ยง** |
| `/api/orders` | `POST` | ผ่าน | ผ่าน (`branch_id`) | ผ่าน (`?`) | ผ่าน | **ไม่ผ่าน (เดิม)** | **มีความเสี่ยงสูง** |
| `/api/reports/sales` | `GET` | ผ่าน | ผ่าน (`branch_id`) | ผ่าน (`?`) | ผ่าน | ไม่เกี่ยวข้อง | ผ่าน |

---

## 3. รายละเอียดจุดที่พบความเสี่ยง (Identified Vulnerabilities & Risks)

### ความเสี่ยงที่ 1: Race Condition ในการตัดสต็อกสินค้า (`POST /api/orders`)
- **ระดับความรุนแรง:** **Critical**
- **ลักษณะปัญหา:** ในโค้ดดั้งเดิม กระบวนการตรวจสอบสต็อก (`SELECT stock_quantity FROM menu_item`) และการตัดสต็อก (`UPDATE menu_item SET stock_quantity = stock_quantity - ?`) ทำงานแยกคำสั่งกันโดยไม่มี Database Transaction และไม่ได้ใช้ Row-level Lock
- **สถานการณ์ที่เกิดปัญหาจริง:** หากมีพนักงาน 2 คน (หรือ 2 สาขา) ยืนยันออเดอร์เมนูเดียวกันในเสี้ยววินาทีเดียวกัน ขณะที่สต็อกเหลือ 1 หน่วย คำสั่ง `SELECT` ของทั้งสองคนจะอ่านได้สต็อก 1 เท่ากัน และทั้งคู่จะผ่านเงื่อนไขไปทำการ `UPDATE` ส่งผลให้สต็อกกลายเป็น 0 - 1 = -1 (สต็อกติดลบ) ทำให้ข้อมูลสินค้าผิดพลาดทันที

### ความเสี่ยงที่ 2: Insecure Direct Object Reference (IDOR) ในการแก้ไขเมนู (`PUT /api/menu/:id`)
- **ระดับความรุนแรง:** **High**
- **ลักษณะปัญหา:** คำสั่งแก้ไขข้อมูลเมนูค้นหาด้วย `WHERE menu_id = ?` เพียงอย่างเดียว โดยไม่ได้ตรวจสอบว่าเมนูดังกล่าวเป็นของ `branch_id` ที่ผู้ใช้มีสิทธิ์จัดการหรือไม่
- **สถานการณ์ที่เกิดปัญหาจริง:** ผู้จัดการสาขาที่ 1 สามารถส่ง Request แก้ไขราคาสินค้าหรือสต็อกของสาขาที่ 2 ได้ หากเดาหรือส่ง `menu_id` ของสาขาอื่นเข้ามา

---

## 4. การแก้ไขที่ทำจริงในสัปดาห์นี้ (Implemented Fix)

ทีมงานได้เลือกแก้ไขความเสี่ยงระดับ **Critical** เรื่อง **Race Condition ในกระบวนการสั่งซื้อและตัดสต็อก** โดยการนำ **Database Transaction** ร่วมกับคำสั่ง **`SELECT ... FOR UPDATE`** มาประยุกต์ใช้ใน `orderController.js`:

### เปรียบเทียบโค้ด ก่อน และ หลัง แก้ไข:

#### โค้ดเดิม (มีความเสี่ยง Race Condition):
```javascript
// โค้ดเดิม: ไม่ปลอดภัยเนื่องจากไม่มี Transaction และไม่มีการล็อกแถว
async function createOrder(req, res) {
    const { branchId, employeeId, paymentMethod, items } = req.body;
    
    // 1. เช็คสต็อกทีละรายการ
    for (const item of items) {
        const [rows] = await db.query(
            'SELECT stock_quantity FROM menu_item WHERE menu_id = ?', 
            [item.menuId]
        );
        if (rows[0].stock_quantity < item.quantity) {
            return res.status(400).json({ error: 'สต็อกสินค้าไม่เพียงพอ' });
        }
    }

    // 2. บันทึกคำสั่งซื้อ
    const [orderResult] = await db.query(
        'INSERT INTO orders (branch_id, employee_id, payment_method) VALUES (?, ?, ?)',
        [branchId, employeeId, paymentMethod]
    );

    // 3. ตัดสต็อก
    for (const item of items) {
        await db.query(
            'UPDATE menu_item SET stock_quantity = stock_quantity - ? WHERE menu_id = ?',
            [item.quantity, item.menuId]
        );
    }

    res.status(201).json({ success: true, orderId: orderResult.insertId });
}
```

#### โค้ดใหม่ (ปลอดภัยด้วย Transaction และ `SELECT ... FOR UPDATE`):
```javascript
// โค้ดใหม่: ปลอดภัยด้วย Transaction ป้องกัน Race Condition และความไม่สอดคล้องของข้อมูล
async function createOrder(req, res) {
    const { branchId, employeeId, paymentMethod, items } = req.body;
    const connection = await db.getConnection();

    try {
        await connection.beginTransaction(); // เริ่ม Transaction

        // 1. ล็อกแถวและตรวจสอบสต็อกพร้อมกันด้วย FOR UPDATE
        for (const item of items) {
            const [rows] = await connection.query(
                'SELECT stock_quantity, price FROM menu_item WHERE menu_id = ? AND branch_id = ? FOR UPDATE',
                [item.menuId, branchId]
            );

            if (rows.length === 0 || rows[0].stock_quantity < item.quantity) {
                await connection.rollback(); // คืนสถานะหากสต็อกไม่พอ
                connection.release();
                return res.status(400).json({ 
                    error: `สินค้า ID ${item.menuId} สต็อกไม่เพียงพอ` 
                });
            }
            item.unitPrice = rows[0].price;
        }

        // 2. บันทึก Orders
        const [orderResult] = await connection.query(
            'INSERT INTO orders (branch_id, employee_id, payment_method) VALUES (?, ?, ?)',
            [branchId, employeeId, paymentMethod]
        );
        const orderId = orderResult.insertId;

        // 3. บันทึก Order Items และ ตัดสต็อก
        for (const item of items) {
            await connection.query(
                'INSERT INTO order_item (order_id, menu_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                [orderId, item.menuId, item.quantity, item.unitPrice]
            );

            await connection.query(
                'UPDATE menu_item SET stock_quantity = stock_quantity - ? WHERE menu_id = ?',
                [item.quantity, item.menuId]
            );

            await connection.query(
                'INSERT INTO stock_movement (menu_id, quantity_change) VALUES (?, ?)',
                [item.menuId, -item.quantity]
            );
        }

        await connection.commit(); // ยืนยันการเปลี่ยนแปลงทั้งหมดสมบูรณ์
        connection.release();

        res.status(201).json({ 
            success: true, 
            orderId: orderId,
            message: 'สร้างออเดอร์และตัดสต็อกสำเร็จ' 
        });
    } catch (err) {
        await connection.rollback(); // Rollback หากเกิดข้อผิดพลาดใดๆ
        connection.release();
        res.status(500).json({ error: 'เกิดข้อผิดพลาดในการประมวลผลคำสั่งซื้อ' });
    }
}
```

---

## 5. แผนการปรับปรุงความเสี่ยงที่เหลือ (Remaining Risks & Action Plan)

| ความเสี่ยง | ระดับความรุนแรง | แนวทางแก้ไขที่วางแผนไว้ |
|---|:---:|---|
| ป้องกัน IDOR ใน `PUT /api/menu/:id` | High | ปรับคำสั่ง SQL ให้ผูกกับสาขาเสมอ: `UPDATE menu_item SET ... WHERE menu_id = ? AND branch_id = ?` และส่ง Error 403 Forbidden หากแก้ไขข้ามสาขา |
| เพิ่ม Rate Limiting สำหรับการเข้าใช้งาน API | Medium | ติดตั้งมิดเดิลแวร์ `express-rate-limit` เพื่อป้องกันการโจมตีแบบ DoS หรือการยิงคำสั่งซื้อซ้ำซ้อนจากสคริปต์อัตโนมัติ |
| Audit Logging สำหรับการปรับปรุงสต็อกฉุกเฉิน | Low | เพิ่มการจัดเก็บผู้ใช้ (`employee_id`) ลงในตาราง `stock_movement` เพื่อให้ตรวจสอบย้อนหลังได้ว่าพนักงานคนใดเป็นผู้แก้ไขสต็อก |
