# ระบบบริหารจัดการร้าน Minions Cafe (Coffee Shop POS & Management System)

> โครงงานรายวิชา 88734065 การวิเคราะห์และออกแบบระบบ (System Analysis and Design)  
> ภาคการศึกษาปลาย ปีการศึกษา 2568 คณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา

---

## 👥 ข้อมูลกลุ่มและสมาชิก (กลุ่มที่ 14)

| ลำดับ |  รหัสนิสิต   | ชื่อ - สกุล            | บทบาทหน้าที่หลัก                                           |
| :---: | :----------: | ---------------------- | ---------------------------------------------------------- |
|   1   | **67160002** | นางสาวชาลิสา ศรีหงษ์   | Project Manager, System Analyst (wk01, wk02, wk15)         |
|   2   | **67160042** | นางสาวมนทกานต์ ปาลี    | System Analyst & Requirements Engineer (wk03, wk10, wk13)  |
|   3   | **67160178** | นางสาวจตุพร ธรรมฤทธิ์  | Software Designer & UML Modeler (wk04, wk06, wk09)         |
|   4   | **67160190** | นางสาวบุษชยาภา คะสุดใจ | Database Designer & Backend Developer (wk07, wk11, wk14)   |
|   5   | **67160392** | นางสาวชนิดาภา ชาภักดี  | UI/UX Designer & Frontend Developer (wk10, wk12, Demo App) |

---

## 📖 สารบัญเอกสารโครงงานทั้งหมด (Project Documentation Links)

ผู้ตรวจสามารถคลิกลิงก์ด้านล่างเพื่อเข้าสู่เอกสารและไดอะแกรมแต่ละส่วนในโฟลเดอร์ `docs/` ได้ทันที:

### 📑 รายงานรวมเล่มโครงงาน (CLO4, CLO5, CLO6, CLO7)

- 📄 **[รายงานรวมเล่มฉบับสมบูรณ์ (PDF)](docs/project-report.pdf)** _(ส่งตามเกณฑ์สัปดาห์ที่ 15)_
- 📝 **[รายงานรวมเล่มฉบับสมบูรณ์ (Word .docx)](docs/project-report.docx)**
- 📋 **[รายงานรวมเล่มฉบับสมบูรณ์ (Markdown)](docs/project-report.md)**

### 📚 เอกสารส่งมอบรายสัปดาห์ (Weekly Deliverables wk01 - wk14)

1. **สัปดาห์ที่ 1:** [Team Charter & Information System Analysis](docs/wk01-team-charter.md)
2. **สัปดาห์ที่ 2:** [Feasibility Report & BPMN (As-Is / To-Be)](docs/wk02-feasibility-report.md)
   - ภาพประกอบ: [As-Is Process](docs/images/As-Is.jpg) | [To-Be Process](docs/images/to-be.png)
3. **สัปดาห์ที่ 3:** [Requirements Analysis Document & Interview](docs/wk03-requirements.md) _(พร้อมบันทึกประวัติปรับปรุง FR-11 จาก Prototype)_
4. **สัปดาห์ที่ 4:** [User Stories & Use Case Diagram](docs/wk04-user-stories.md)
   - ภาพประกอบ: [Use Case Diagram](docs/images/usecase-diagram.jpg)
5. **สัปดาห์ที่ 6:** การออกแบบเชิงวัตถุ (OOAD)
   - ไดอะแกรม: [Class Diagram](docs/wk06-class-diagram.png) | [Object Diagram](docs/wk06-object-diagram.png)
6. **สัปดาห์ที่ 7:** การออกแบบฐานข้อมูล (Database Design)
   - ไดอะแกรม: [ER Diagram](docs/wk07-er-diagram.png)
   - สคริปต์ SQL: [Database Schema DDL](docs/wk07-schema.sql)
7. **สัปดาห์ที่ 9:** การออกแบบกระบวนการและพฤติกรรมระบบ
   - ไดอะแกรม: [Sequence Diagram (Order to Stock)](docs/wk09-sequence-diagram.png)
8. **สัปดาห์ที่ 10:** การออกแบบ Input/Output, UI และ Wireframe
   - เอกสาร: [Input / Output Design](docs/wk10-input-output-design.md) | [Wireframe Design](docs/wk10-wireframe.md)
   - ภาพประกอบ: [Input/Output Sample](docs/images/wk10-input-output.png) | [Wireframe Mid-Fi](docs/images/wk10-wireframe.png)
   - 🌟 **[Software Requirements Specification (SRS ฉบับสมบูรณ์)](docs/wk10-srs.md)** _(หลักฐานสำคัญประเมิน CLO5)_
9. **สัปดาห์ที่ 11:** [System Architecture (4+1 Architectural View Model)](docs/wk11-architecture.md)
   - ไดอะแกรม: [Physical View](docs/images/wk11-physical-view.png) | [Development View](docs/images/wk11-development-view.png)
10. **สัปดาห์ที่ 12:** [Usability Testing Report (Task-Based & Think-Aloud)](docs/wk12-usability-testing.md)
11. **สัปดาห์ที่ 14:** [Code Quality & Security Review Report](docs/wk14-quality-review.md) _(แก้ไข Race Condition ด้วย Transaction & FOR UPDATE)_

### 🤖 ภาคผนวก: แบบฟอร์มเปิดเผยการใช้ AI (AI Disclosure Forms)

- [AI Disclosure - สัปดาห์ที่ 5 (Git & Branching)](docs/ai-disclosure/wk05-ai-disclosure.md)
- [AI Disclosure - สัปดาห์ที่ 9 (Sequence Diagram & API)](docs/ai-disclosure/wk09-ai-disclosure.md)
- [AI Disclosure - สัปดาห์ที่ 10 (Input/Output & Wireframe)](docs/ai-disclosure/wk10-ai-disclosure.md)
- [AI Disclosure - สัปดาห์ที่ 13 (System Integration & E2E Testing)](docs/ai-disclosure/wk13-ai-disclosure.md)

---

## 💻 การทดสอบและรันระบบ Live Demo (`code/`)

ระบบเว็บแอปพลิเคชัน Minions Cafe POS ออกแบบมาให้ทำงานได้จริง (Working Prototype) ตามหน้า Wireframe ในสัปดาห์ที่ 10 รองรับทั้งการรันผ่าน Node.js Express Server และการเปิดตรงบนเบราว์เซอร์

### วิธีที่ 1: รันผ่าน Node.js Express Server (แนะนำ)

```bash
# 1. เข้าสู่โฟลเดอร์ code
cd code

# 2. ติดตั้ง Dependencies
npm install

# 3. เริ่มต้น Web Server
npm start
```

เปิดเบราว์เซอร์ไปที่ **`http://localhost:3000`**

### วิธีที่ 2: รันแบบ Standalone Client

สามารถดับเบิลคลิกไฟล์ **`code/index.html`** เพื่อเปิดใช้งานบนเบราว์เซอร์ใดก็ได้ทันที (มีระบบจำลอง State และ LocalStorage ในตัว ทำงานได้สมบูรณ์ 100% แม้ไม่มีฐานข้อมูลภายนอก)

---

## 🎙️ ลำดับขั้นตอนการนำเสนอ Live Demo (5-8 นาที ตามสัปดาห์ที่ 15)

บนหน้าเว็บของระบบ มี **แถบควบคุม Live Demo (แถบสีดำด้านล่างจอ)** ที่ช่วยให้ผู้บรรยายหรือผู้ตรวจสามารถกดทดสอบได้ทีละขั้นตอนอย่างราบรื่น:

1. **ขั้นตอนที่ 1: เปิดหน้าจอ POS แสดงรายการเมนู**
   - แสดงรายการเครื่องดื่มและขนม พร้อมราคาและสต็อกคงเหลือ
   - สาธิต **Branch Selector** มุมบนขวา สลับระหว่าง "สาขา 1 (ม.บูรพา)" และ "สาขา 2 (แหลมทอง)"
2. **ขั้นตอนที่ 2: เลือกเมนู 2-3 รายการ แสดงการคำนวณยอดรวมอัตโนมัติ**
   - คลิกปุ่ม **[2️⃣ สั่ง 2-3 เมนู]** ระบบจะเพิ่ม Latte (45.-) + Espresso (35.-) + Croissant (55.-) เข้าตะกร้า
   - แสดงการคำนวณ Subtotal และยอดรวมสุทธิ **฿135.00** แบบเรียลไทม์ทันที
   - ปรับจำนวนด้วยปุ่ม `[-] 1 [+]` สังเกตยอดเงินเปลี่ยนทันที
3. **ขั้นตอนที่ 3: ยืนยันออเดอร์ แสดงใบเสร็จที่ระบบสร้างขึ้น**
   - เลือกวิธีชำระเงิน "เงินสด" รับเงินมา 200 บาท คำนวณเงินทอน 65 บาท
   - กดยืนยันออเดอร์ ระบบตัดสต็อกสินค้าและแสดง **ใบเสร็จรับเงิน (Official Thermal Receipt)** ตามสเปก WK10
4. **ขั้นตอนที่ 4: เปิดหน้ารายงานยอดขาย แสดงว่าออเดอร์เพิ่งทำปรากฏในรายงานทันที**
   - คลิกแท็บ **[📊 รายงานยอดขาย]** หรือปุ่ม **[4️⃣ ดูรายงานทันที]**
   - สังเกตยอดขายรวม (Total Revenue) และจำนวนออเดอร์อัปเดตทันทีแบบ Real-time Consistency
   - ดูตารางจัดอันดับเมนูขายดี และกราฟเปรียบเทียบยอดขายระหว่าง 2 สาขา
5. **ขั้นตอนที่ 5: สาธิตกรณีสต็อกไม่เพียงพอ (Business Logic สัปดาห์ที่ 9 & FR-11)**
   - คลิกปุ่ม **[5️⃣ ทดสอบสต็อกหมด]** ระบบจะไฮไลต์เมนู **Lemon Tea (สต็อก = 0)**
   - ระบบปิดการใช้งานปุ่ม (Disabled) และขึ้นป้าย "สินค้าหมด" ป้องกันข้อผิดพลาดตั้งแต่หน้าแรกตามข้อกำหนด FR-11
   - หากผู้ใช้พยายามสั่งซื้อเกินจำนวนสต็อกที่มี ระบบจะปฏิเสธและแจ้งเตือนทันที
