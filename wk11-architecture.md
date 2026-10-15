# สถาปัตยกรรมระบบ Minions Cafe (4+1 Architectural View Model)
## สัปดาห์ที่ 11: การออกแบบระบบ — สถาปัตยกรรมและการแบ่ง Component (4+1 View)

**กลุ่มที่ 14:** Minions Cafe  
**สมาชิกกลุ่ม:**
1. 67160002 นางสาวชาลิสา ศรีหงษ์
2. 67160042 นางสาวมนทกานต์ ปาลี
3. 67160178 นางสาวจตุพร ธรรมฤทธิ์
4. 67160190 นางสาวบุษชยาภา คะสุดใจ
5. 67160292 นางสาวชนิดาภา ชาภักดี

---

## 1. Physical View: โครงสร้างทางกายภาพและการติดตั้งระบบ (Deployment Topology)

Physical View แสดงฮาร์ดแวร์/โหนด (Node) สภาพแวดล้อมในการรัน (Execution Environment) และช่องทางการเชื่อมต่อระหว่างโหนดที่ระบบ Minions Cafe ใช้งานจริงในปัจจุบัน

![Physical View Diagram](wk11-physical-view.png)

### คำอธิบายประกอบ Physical View:
1. **Node ทางกายภาพจริง:** ปัจจุบันระบบ Minions Cafe พัฒนาและรันอยู่บน **เครื่องคอมพิวเตอร์พัฒนาเครื่องเดียว (Single Development Machine / `localhost`)** โดยไม่มีการแยกเซิร์ฟเวอร์ต่างหากออกไปนอกเครื่อง
2. **การแยก Process/Execution Environment:**
   * **Client Device:** ใช้งานผ่าน Web Browser ส่งคำขอไปยัง Web Application
   * **Application Node:** รัน Node.js Runtime process เดี่ยว ให้บริการ API และ Web Server ที่พอร์ต `3000`
   * **Database Node:** รัน MySQL Server daemon เป็น background service ในเครื่องเดียวกัน ที่พอร์ต `3306` เข้าถึงผ่าน Database Connection Pool (`mysql2/promise`)
3. **การรองรับหลายสาขา (Multi-branch Scope):** สอดคล้องกับข้อกำหนดใน `wk11.md` หัวข้อ 1.3 ระบบ Minions Cafe รองรับแนวคิดหลายสาขาในระดับฐานข้อมูลเชิงตรรกะผ่านคอลัมน์ `branch_id` (ตาราง `branch`, `employee`, `menu_item`, `orders`) โดยไม่ต้องมี Database Server แยกประจำสาขาจริง และไม่มีการทำ Data Replication ข้ามสาขา ใช้เซิร์ฟเวอร์ฐานข้อมูลเดี่ยวชุดนี้ชุดเดียว

---

## 2. Development View: การแบ่ง Component และ Module ของ Source Code

Development View แสดงการจัดโครงสร้างโค้ดภายใน Repository จริงของ Minions Cafe ตามหลักการแยกความรับผิดชอบ (Separation of Concerns) แบบ Layered Architecture ภายใน Monolith

![Development View Diagram](wk11-development-view.png)

### คำอธิบายและการตรวจสอบความสอดคล้องกับ Repository จริง (ตามหัวข้อ 3.4):
1. **ความสอดคล้องของ Domain Class:** ใน repository จริงของกลุ่ม มีไฟล์ `orderModel.js` ที่นิยาม `class Order` และ `class OrderItem` (พร้อม method `getSubtotal()`) และ `menuModel.js` ที่นิยาม `class MenuItem` ตามข้อกำหนดของสัปดาห์ที่ 6 โดยตรง
2. **ความสอดคล้องของ Data-access Functions:** ฟังก์ชันการเข้าถึงฐานข้อมูลใน Data-access Model สอดคล้องตรงกับ Sequence Diagram ใน `wk09-sequence-diagram.mmd` ได้แก่ `findManyForStockCheck()`, `create()`, `addItem()`, และ `deductStock()`
3. **การเชื่อมต่อฐานข้อมูล:** ไฟล์ config เชื่อมต่อฐานข้อมูลผ่าน `mysql2/promise` connection pool สอดคล้องกับที่ระบุไว้ใน `wk05-ai-disclosure.md` และใช้ Schema ตาม `wk07-schema.sql`
4. **ข้อจำกัดที่สะท้อนตามความเป็นจริง (Known Limitation):** ในกระบวนการ `createOrder` โค้ดปัจจุบันยังไม่มี Database Transaction (`START TRANSACTION` / `COMMIT` / `ROLLBACK`) ครอบคลุมระหว่างการบันทึก `orders`, `order_item` และการตัดสต็อกใน `menu_item` สถาปัตยกรรมจึงสื่อสารการทำงานแบบคำสั่งต่อคำสั่งผ่าน connection pool อย่างตรงไปตรงมา ไม่ได้แสดงว่ามี Distributed Transaction หรือ Transaction Management ที่ปลอดภัยเกินจริง

---

## 3. สรุปสถาปัตยกรรมของระบบ Minions Cafe

ระบบร้าน Minions Cafe (กลุ่ม 14) เลือกใช้สถาปัตยกรรมแบบ **Monolithic Architecture ที่จัดโครงสร้างภายในแบบ Layered Architecture (Monolithic + Layered)** เนื่องจากความเหมาะสมอย่างยิ่งต่อบริบทของโครงงาน:

1. **ขนาดของทีมและระยะเวลาพัฒนา:** ทีมพัฒนามีสมาชิก 5 คน และมีระยะเวลาดำเนินการในรายวิชาเพียง 1 ภาคการศึกษา (14 สัปดาห์เรียนจริง) การใช้ Monolithic ช่วยลดความซับซ้อนในการตั้งค่า Infrastructure, การกำหนด Service Contract, การจัดการ Network Partitioning, และ CI/CD Pipeline หลายชุด ทำให้ทีมสามารถมุ่งเน้นไปที่การตอบสนองความต้องการของผู้ใช้ (Requirements & User Stories) ได้อย่างรวดเร็ว
2. **ขอบเขตของระบบ (System Scope):** ฟังก์ชันการทำงานของ Minions Cafe อยู่ในขอบเขต 4 ฟังก์ชันหลัก ได้แก่ ระบบรับออเดอร์หน้าร้าน (POS), ระบบจัดการเมนู, ระบบตัดสต็อกสินค้า, และระบบรายงานยอดขาย ซึ่งข้อมูลทุกส่วนมีความสัมพันธ์เชื่อมโยงกันอย่างใกล้ชิด (Cohesive Domain) ภายในฐานข้อมูลเดียว การรวมโค้ดไว้ใน Codebase เดียวและ Deploy เป็น Node.js Process เดี่ยวที่ `localhost:3000` จึงมีประสิทธิภาพสูงและง่ายต่อการดูแลรักษา
3. **ประโยชน์จากการแบ่ง Layer (Separation of Concerns):** แม้จะ Deploy เป็นชิ้นเดียว (Monolith) แต่โค้ดภายในถูกแบ่งชั้นอย่างชัดเจนออกเป็น **Presentation Layer**, **Routes Layer**, **Controllers Layer**, **Domain/Data-access Models Layer**, และ **Config Layer** ส่งผลให้สมาชิกในทีม 5 คนสามารถแบ่งงานกันทำคู่ขนานได้อย่างราบรื่น เช่น สมาชิกคนหนึ่งพัฒนาหน้าตา UI ขณะที่อีกคนปรับปรุงฟังก์ชันคำนวณใน Model และอีกคนจัดการ Controller โดยไม่เกิดผลกระทบข้างเคียงต่อกัน และพร้อมที่จะ Refactor หรือปรับเปลี่ยนเป็น Service แยกในอนาคตหากปริมาณธุรกรรมขยายตัว

---

## 4. คำถามท้ายบท (Review Questions)

### ข้อ 1: เหตุใด 4+1 View Model จึงต้องมีมุมมองมากกว่าหนึ่งด้านในการอธิบายสถาปัตยกรรมซอฟต์แวร์?
**คำตอบ:**  
เพราะระบบซอฟต์แวร์มีความซับซ้อนและมีผู้มีส่วนได้ส่วนเสีย (Stakeholders) หลายกลุ่ม ซึ่งแต่ละกลุ่มมีความสนใจ เป้าหมาย และความต้องการข้อมูลที่แตกต่างกันอย่างสิ้นเชิง การใช้มุมมองเดียวไม่สามารถตอบสนองทุกฝ่ายได้:
* **ผู้บริหารโครงการ / ลูกค้า / ผู้ใช้งาน:** สนใจ **Scenarios (+1)** และ Use Case เพื่อให้มั่นใจว่าระบบทำงานตรงตามความต้องการทางธุรกิจ
* **นักวิเคราะห์ระบบและนักพัฒนา:** สนใจ **Logical View** (Class / Object Diagram) เพื่อเข้าใจโครงสร้าง Entity, ขอบเขตหน้าที่, และความสัมพันธ์เชิงตรรกะในระบบ
* **นักพัฒนาระบบและผู้ตรวจสอบโค้ด:** สนใจ **Development View** (Component Diagram) เพื่อทราบการแบ่งไฟล์, โฟลเดอร์, Layer, Library และความขึ้นต่อกันของ Source Code ใน Repository
* **ผู้ดูแลระบบ / System Integrator:** สนใจ **Process View** (Sequence / Activity Diagram) เพื่อดูลำดับขั้นตอนการทำงาน, Concurrency, Performance และการสื่อสารระหว่าง Process
* **วิศวกรระบบและฝ่าย DevOps:** สนใจ **Physical View** (Deployment Diagram) เพื่อดูสเปกเซิร์ฟเวอร์, Topology เครือข่าย, IP, พอร์ต และการติดตั้งใช้งานจริง  
การมี 5 มุมมองตาม 4+1 View Model จึงช่วยให้ทุกคนมองเห็นภาพระบบที่ตรงกับบทบาทของตนเองได้อย่างครบถ้วนและไม่สับสน

---

### ข้อ 2: การจับคู่เอกสารในสัปดาห์ก่อนหน้าเข้ากับมุมมองทั้ง 5 ด้านของ 4+1 View Model
**คำตอบ:**  
สามารถจับคู่ Artifacts ที่จัดทำไปแล้วในโครงงาน Minions Cafe ได้ดังนี้:

| มุมมอง (View) | เอกสาร/แผนภาพที่จัดทำในโครงงาน | สัปดาห์ | คำอธิบายความสอดคล้อง |
|---|---|:---:|---|
| **Scenarios (+1)** | Use Case Diagram & Descriptions (`usecase-diagram.jpg`, `wk04-user-stories.md`) | Wk 4 | แสดงความต้องการและพฤติกรรมหลักของระบบ เช่น การสั่งซื้อ การจัดการเมนู ซึ่งเป็นศูนย์กลางที่ร้อยเรียงอีก 4 มุมมองเข้าด้วยกัน |
| **Logical View** | Class Diagram & Object Diagram (`class.mmd`, `object.mmd`, `wk06-class-diagram.png`) | Wk 6 | แสดง Class โครงสร้างเชิงตรรกะ เช่น `Order`, `OrderItem`, `MenuItem` ความสัมพันธ์ และ Method คำนวณ |
| **Process View** | Sequence Diagram (`wk09-sequence-diagram.mmd`, `wk10-input-output-design.md`) | Wk 9, 10 | แสดงลำดับการส่ง Message ข้าม Object ตามแกนเวลา ใน Flow การสั่งซื้อ (`POST /api/orders`) และการออกรายงาน |
| **Development View** | โครงสร้างโฟลเดอร์/Component Decomposition (`src/routes`, `src/controllers`, `src/models`, `orderModel.js`, `menuModel.js`) | Wk 5, 11 | แสดงการจัดหมวดหมู่โมดูลโค้ดใน Repository และความขึ้นต่อกันของแต่ละ Layer |
| **Physical View** | Deployment Diagram แสดง Client Device, Node.js App Server, และ MySQL Database Server | Wk 11 | แสดงฮาร์ดแวร์จริง โฮสต์ พอร์ต (localhost:3000, localhost:3306) และเครือข่ายที่ติดตั้งใช้งานจริง |

---

### ข้อ 3: เปรียบเทียบข้อดีและข้อเสียของ Monolithic Architecture เทียบกับ Microservices Architecture สำหรับโครงงานขนาดเล็กใน 1 ภาคการศึกษา
**คำตอบ:**  

| เกณฑ์การเปรียบเทียบ | Monolithic Architecture | Microservices Architecture |
|---|---|---|
| **ความซับซ้อนในการพัฒนา** | **ต่ำมาก:** โค้ดทั้งหมดอยู่ใน Repository เดียว เรียกใช้ฟังก์ชันผ่าน In-memory Function Call ได้โดยตรง Debug และ Trace โค้ดง่าย | **สูงมาก:** ต้องออกแบบ Service Boundary, REST/gRPC API ข้าม Service, จัดการ Network Failure, และ Data Serialization |
| **การทดสอบและการทดลองรัน** | **ง่ายและรวดเร็ว:** รันคำสั่งเดียว (`npm start`) สามารถทดสอบ End-to-End ได้ครบทุกฟังก์ชันบนเครื่องเดี่ยว | **ซับซ้อน:** ต้องจำลองสภาพแวดล้อม รันหลาย Container/Service พร้อมกัน (Docker Compose) และทำ Integration Test ยุ่งยาก |
| **ความซับซ้อนในการ Deploy** | **ง่ายมาก:** Build และ Deploy โหนดเดียว ไม่ต้องมี Service Discovery, API Gateway หรือ Distributed Tracing | **สูงมาก:** ต้องจัดการ Container Orchestration (Kubernetes/ECS), จัดการ CI/CD Pipeline หลายชุด และตรวจสอบ Health Check ข้ามโหนด |
| **ความสอดคล้องของข้อมูล** | **จัดการได้ง่าย:** สามารถใช้ Database Transaction (ACID) และ Foreign Key ภายในฐานข้อมูลเดียวเพื่อรักษาความถูกต้องของสต็อกและยอดเงิน | **จัดการยากมาก:** เกิดฐานข้อมูลแยก (Database-per-Service) ต้องใช้ Eventual Consistency, Saga Pattern หรือ 2-Phase Commit ซึ่งเกินจำเป็น |
| **ความเหมาะสมกับโครงงาน 1 เทอม** | **เหมาะสมสูงสุด (Best Fit):** ทีมขนาด 3-5 คนมีเวลาจำกัด มุ่งเน้นการส่งมอบคุณค่าทางธุรกิจ (Business Value) ได้ครบถ้วนทันกำหนด | **ไม่เหมาะสมอย่างยิ่ง:** เวลาส่วนใหญ่จะหมดไปกับการแก้ปัญหาเชิงโครงสร้างพื้นฐาน (Overhead) มากกว่าการพัฒนาฟีเจอร์ของระบบ |

---

### ข้อ 4: เพราะเหตุใด Architecture Diagram จึงต้องตรวจสอบความสอดคล้องกับโครงสร้าง repository จริง แทนที่จะวาดตามทฤษฎีเพียงอย่างเดียว?
**คำตอบ:**  
1. **ป้องกันภาวะ "สถาปัตยกรรมลวงตา" (Architectural Drift / Illusion):** หากไดอะแกรมวาดตามทฤษฎีหรือวาดสิ่งที่เป็นแผนในอนาคต (เช่น วาดว่ามี Caching Layer, มี Message Queue, หรือมี microservices แยก) ทั้งที่โค้ดจริงไม่มี ไดอะแกรมนั้นจะกลายเป็นเอกสารเท็จที่ไม่สามารถนำไปใช้อ้างอิงในการบำรุงรักษา หรือตรวจสอบคุณภาพซอฟต์แวร์ได้
2. **ความสามารถในการตรวจสอบย้อนกลับ (Traceability):** สถาปัตยกรรมที่ดีต้องทำหน้าที่เป็นพิมพ์เขียวที่ชี้ทางไปยังโค้ดจริง (Source Code Navigation) วิศวกรซอฟต์แวร์หรือผู้ตรวจประเมินต้องสามารถหยิบกล่องใน Development View ไปเปิดดูไฟล์จริงในโฟลเดอร์ได้ทันที หากชื่อไฟล์ คลาส หรือฟังก์ชันไม่ตรงกัน จะสร้างความเข้าใจผิดและทำให้การ Onboard สมาชิกใหม่หรือการแก้ไขบั๊กทำได้ช้าลง
3. **การประเมินความเสี่ยงและประสิทธิภาพที่ตรงความจริง:** หากวาดไดอะแกรมว่ามีระบบ Transaction ครอบคลุมการตัดสต็อก ทั้งที่โค้ดจริงยังเป็นคิวรีแยกคำสั่ง ผู้ดูแลระบบจะไม่ทราบว่ามีความเสี่ยงเรื่อง Data Inconsistency หรือ Race Condition แอบแฝงอยู่ ทำให้ไม่สามารถวางแผนป้องกันปัญหาได้อย่างถูกต้อง

---

### ข้อ 5: หากขยายเป็น 10 สาขาที่มีเซิร์ฟเวอร์/ฐานข้อมูลของตัวเองจริงในอนาคต สถาปัตยกรรม Monolithic ปัจจุบันจะมีข้อจำกัดใด และควรปรับปรุง Physical View และ Development View อย่างไร?
**คำตอบ:**  
**1. ข้อจำกัดของสถาปัตยกรรมปัจจุบันเมื่อขยายเป็น 10 สาขา:**
* **ปัญหา Single Point of Failure (SPOF) และ Network Dependency:** หากเครื่องเซิร์ฟเวอร์หรือเครือข่ายส่วนกลางขัดข้อง ทั้ง 10 สาขาจะไม่สามารถเปิดบิลหรือคิดเงินหน้าร้านได้ทันที (POS หยุดทำงาน)
* **ปัญหา Latency ในการทำธุรกรรม:** การที่แคชเชียร์ทุกสาขาต้องส่ง HTTP Request มาบันทึกยอดที่เซิร์ฟเวอร์กลาง จะทำให้การออกใบเสร็จล่าช้า โดยเฉพาะช่วงเวลาเร่งด่วน
* **ปัญหาการรวมศูนย์ข้อมูลและการสรุปรายงาน:** หากฐานข้อมูลอยู่ที่สาขาแยกกัน แต่เจ้าของร้านต้องการดูรายงานยอดขายรวมแบบ Real-time ข้าม 10 สาขา จะทำได้ยากหากไม่มีระบบ Data Synchronization

**2. แนวทางการปรับปรุง Physical View:**
* **ปรับเปลี่ยนเป็น Edge-Cloud Topology / Distributed Nodes:**
  * **Branch Node (10 สาขา):** แต่ละสาขามี Local Application Server (เช่น Mini PC / POS Terminal) รัน Node.js และ Local Database (SQLite หรือ Local MySQL) เพื่อให้ขายของแบบ Offline-first ได้แม้เน็ตหลุด
  * **Central Cloud Node:** มี Cloud Server กลาง (เช่น AWS EC2/RDS หรือ DigitalOcean) สำหรับเป็นศูนย์กลางรับข้อมูลยอดขายและจัดการข้อมูลเมนูหลัก
  * **Network Communication:** เพิ่มเส้นทางการซิงค์ข้อมูล (เช่น REST Sync, WebSocket หรือ Message Queue เช่น MQTT/RabbitMQ) ระหว่าง Branch Nodes กับ Central Cloud Node

**3. แนวทางการปรับปรุง Development View:**
* **เพิ่ม Synchronization Module / Service:** ในโค้ดต้องเพิ่ม Component ใหม่ เช่น `syncService.js` ทำหน้าที่ดักจับออเดอร์ที่ขายหน้าร้านแล้วส่งไป Sync กับคลาวด์เมื่อมีอินเทอร์เน็ต
* **เพิ่ม Offline Storage & Queue Layer:** สำหรับพักข้อมูลออเดอร์ไว้ในเครื่องสาขาชั่วคราว
* **แยก Service ตามบทบาท:** โค้ดส่วน POS Client เน้นความเร็วในการบันทึก Local Data ขณะที่ส่วน Reporting & Analytics ย้ายไปรันบน Central Server เพื่อประมวลผลข้อมูลขนาดใหญ่จากทุกสาขา

---

### ข้อ 6: โค้ด `createOrder` ยังไม่มี database transaction ครอบ flow การตัดสต็อก Architecture Diagram ควรสื่อสารข้อจำกัดนี้อย่างไร และทำไมการวาด diagram ให้สมบูรณ์แบบเกินจริงจึงเป็นปัญหา?
**คำตอบ:**  
**1. การสื่อสารข้อจำกัดใน Architecture Diagram:**
* **ใน Development View / Process View:** ไม่ควรเขียนลูกศรหรือสัญลักษณ์ที่ระบุว่า "Atomic Transaction" หรือ "Rollback on Error" แต่ควรเขียนระบุเป็นคำสั่งแยกย่อยที่ชัดเจน เช่น `1: create order -> 2: add items -> 3: deduct stock` และระบุหมายเหตุแนบท้าย (Architecture Note / Known Limitations) อย่างเปิดเผยว่า: *"กระบวนการสั่งซื้อยังทำงานแบบ Non-transactional คำสั่ง `INSERT orders`, `INSERT order_item` และ `UPDATE menu_item stock` ทำงานแยก Connection กัน หากเกิดความล้มเหลวระหว่างขั้นตอนการตัดสต็อก อาจเกิดข้อมูลออเดอร์ตกค้างโดยสต็อกไม่ได้ถูกตัดจริง"*

**2. ปัญหาของการวาด Diagram ให้สมบูรณ์แบบเกินจริงต่อการตัดสินใจ:**
* **สร้างความมั่นใจผิดพลาด (False Sense of Security):** ผู้บริหาร ผู้ตรวจ หรือทีมงานคนอื่นจะเข้าใจว่าระบบมีความปลอดภัยสมบูรณ์ (Production-ready) จึงไม่จัดสรรทรัพยากรหรือเวลามาปรับปรุงจุดบกพร่องนี้
* **นำไปสู่ความเสียหายทางธุรกิจ (Business Risk):** หากระบบถูกนำไปใช้งานจริงในการขายที่มีปริมาณธุรกรรมพร้อมกันสูง (High Concurrency) สต็อกจะเกิดปัญหา Over-selling หรือตัดสต็อกไม่ตรงกับยอดเงิน ทำให้เกิดความเสียหายทางการเงินและกระทบต่อความน่าเชื่อถือของร้าน
* **บิดเบือนการตัดสินใจด้านสถาปัตยกรรม:** หากทีมออกแบบระบบอื่นมาต่อยอด โดยเชื่อว่าฐานข้อมูลมีความสอดคล้องแบบสมบูรณ์ 100% เสมอ ระบบใหม่ที่มาเชื่อมต่ออาจพังทลายทันทีเมื่อพบเจอข้อมูลที่ Inconsistent การบันทึกข้อจำกัดตามจริงจึงเป็นจรรยาบรรณสำคัญของวิศวกรซอฟต์แวร์ในการออกแบบระบบ
