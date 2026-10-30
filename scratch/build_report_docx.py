import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = r"D:\System Analysis\Minions\docs"
OUT_DOCX = os.path.join(DOCS_DIR, "project-report.docx")

def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report_docx():
    doc = docx.Document()

    # Set page margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # Color palette
    COLOR_PRIMARY = RGBColor(74, 46, 27)    # #4A2E1B Espresso
    COLOR_ACCENT = RGBColor(217, 119, 6)    # #D97706 Golden Amber
    COLOR_DARK = RGBColor(30, 27, 24)       # #1E1B18 Dark Text
    COLOR_MUTED = RGBColor(100, 90, 85)     # #645A55
    HEX_HEADER = "4A2E1B"
    HEX_LIGHT_ROW = "FAF6F0"
    HEX_WHITE = "FFFFFF"

    # Set Normal Style font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Prompt'
    font.size = Pt(11)
    font.color.rgb = COLOR_DARK

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(14)
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_body(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = 'Prompt'
            run_b.font.size = Pt(11)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = 'Prompt'
            run_b.font.size = Pt(11)
            run_b.font.bold = True
            run_b.font.color.rgb = COLOR_DARK
        run = p.add_run(text)
        run.font.name = 'Prompt'
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_DARK
        return p

    def add_image_figure(img_rel_path, caption_text, width_inches=5.8):
        full_path = os.path.join(DOCS_DIR, img_rel_path)
        if not os.path.exists(full_path):
            alt_path = os.path.join(DOCS_DIR, "images", img_rel_path)
            if os.path.exists(alt_path):
                full_path = alt_path

        if os.path.exists(full_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            run = p.add_run()
            run.add_picture(full_path, width=Inches(width_inches))

            cp = doc.add_paragraph()
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.space_after = Pt(12)
            crun = cp.add_run(f"ภาพที่: {caption_text}")
            crun.font.name = 'Prompt'
            crun.font.size = Pt(9.5)
            crun.font.italic = True
            crun.font.color.rgb = COLOR_MUTED

    def add_table_data(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].text = title
            set_cell_background(hdr_cells[i], HEX_HEADER)
            set_cell_margins(hdr_cells[i], 120, 120, 150, 150)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Prompt'
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, row_items in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = HEX_LIGHT_ROW if r_idx % 2 == 1 else HEX_WHITE
            for c_idx, val in enumerate(row_items):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], 80, 80, 120, 120)
                p = row_cells[c_idx].paragraphs[0]
                for r in p.runs:
                    r.font.name = 'Prompt'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = COLOR_DARK

        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================================
    # COVER & HEADER
    # ==========================================
    add_title("รายงานโครงงานการวิเคราะห์และออกแบบระบบ")
    add_subtitle("ระบบบริหารจัดการร้าน Minions Cafe (Coffee Shop POS & Management System)")

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_p.paragraph_format.space_after = Pt(16)
    m1 = meta_p.add_run("กลุ่มที่ 14: Minions Cafe\n")
    m1.bold = True
    m1.font.size = Pt(12)
    m1.font.color.rgb = COLOR_PRIMARY
    m2 = meta_p.add_run("รายวิชา 88734065 การวิเคราะห์และออกแบบระบบ (System Analysis and Design)\nคณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา | ภาคการศึกษาปลาย 2568\n")
    m2.font.size = Pt(10.5)
    m2.font.color.rgb = COLOR_MUTED

    # Members Table
    members_data = [
        ["1", "67160002", "นางสาวชาลิสา ศรีหงษ์", "Project Manager, System Analyst"],
        ["2", "67160042", "นางสาวมนทกานต์ ปาลี", "Lead Developer, System Analyst & Requirements Engineer"],
        ["3", "67160178", "นางสาวจตุพร ธรรมฤทธิ์", "Business Analyst, Software Designer & UML Modeler"],
        ["4", "67160190", "นางสาวบุษชยาภา คะสุดใจ", "Database Designer, Backend Developer"],
        ["5", "67160392", "นางสาวชนิดาภา ชาภักดี", "UI/UX Designer, Frontend Developer & QA Specialist"]
    ]
    add_table_data(["ลำดับ", "รหัสนิสิต", "ชื่อ - สกุล", "บทบาทหน้าที่หลัก"], members_data, [0.6, 1.2, 2.3, 2.1])

    # ==========================================
    # SECTION 1: บทนำ
    # ==========================================
    add_heading1("1. บทนำ (Introduction)")
    add_body("ร้านกาแฟ Minions Cafe เป็นธุรกิจร้านกาแฟสด ขนมอบ และเครื่องดื่มที่มีผู้เข้ามาใช้บริการอย่างต่อเนื่อง โดยมีกลุ่มลูกค้าเป้าหมายหลักคือนิสิต อาจารย์ และบุคลากรภายในมหาวิทยาลัย ตลอดจนประชาชนทั่วไปในพื้นที่ใกล้เคียง ปัจจุบันร้านมีนโยบายในการขยายการดำเนินงานเป็นรูปแบบหลายสาขา (Multi-branch) ได้แก่ สาขา 1 (สาขาหลัก - ม.บูรพา) และ สาขา 2 (สาขาในเมือง - แหลมทอง)", "1.1 บริบทของร้านกาแฟ: ")
    add_body("จากการศึกษากระบวนการเดิมของร้านกาแฟ พบปัญหาคอขวดหลัก 4 ประการ ได้แก่ ความผิดพลาดในการจดบิลด้วยมือ (เฉลี่ยคิดเงินผิด 3-5 รายการต่อวัน), ภาวะสต็อกวัตถุดิบหมดระหว่างวันโดยไม่รู้ตัวล่วงหน้า, การขาดข้อมูลยอดขายแบบเรียลไทม์ และความยุ่งยากในการแยกข้อมูลการขายข้ามสาขา", "1.2 สภาพปัญหาเดิม: ")
    add_body("โครงงานนี้มีวัตถุประสงค์เพื่อวิเคราะห์ ออกแบบ และพัฒนาระบบ POS หน้าร้านที่คำนวณเงินและออกใบเสร็จได้อย่างถูกต้องรวดเร็ว, มีระบบตัดสต็อกอัตโนมัติพร้อมแจ้งเตือนสินค้าใกล้หมดและปิดปุ่มเมื่อสต็อกหมด (FR-11), และมีแดชบอร์ดสรุปยอดขายแบบเรียลไทม์แยกสาขาตามหลัก 3NF และ 4+1 View Model", "1.3 วัตถุประสงค์ของโครงงาน: ")
    add_body("โครงงานครอบคลุมองค์ประกอบ 6 ด้านของระบบสารสนเทศ (People, Process, Data, Hardware, Software, Network) อย่างเป็นระบบตามที่ระบุใน Team Charter สัปดาห์ที่ 1", "1.4 องค์ประกอบ 6 ด้าน: ")

    # ==========================================
    # SECTION 2: การวิเคราะห์ความเป็นไปได้
    # ==========================================
    add_heading1("2. การวิเคราะห์ความเป็นไปได้ (Feasibility Study)")
    add_body("ทีมงานได้ศึกษาความเป็นไปได้ตามกรอบ TELOS (Technical, Economic, Legal, Operational, Schedule) พบว่ามีความคุ้มค่าสูง สามารถลดความสูญเสียจากการคิดเงินผิดพลาดได้เดือนละกว่า 3,000 - 5,000 บาท พนักงานเรียนรู้ระบบได้ภายใน 5 นาที และส่งมอบระบบได้ครบถ้วนภายใน 1 ภาคการศึกษา", "2.1 การศึกษาความเป็นไปได้ (TELOS): ")
    
    add_heading2("2.2 การเปรียบเทียบกระบวนการทำงานเดิม (As-Is) และแบบใหม่ (To-Be)")
    add_image_figure("As-Is.jpg", "แผนภาพกระบวนการทำงานเดิมก่อนมีระบบ (As-Is Process Diagram)")
    add_image_figure("to-be.png", "แผนภาพกระบวนการทำงานใหม่หลังมีระบบ (To-Be Business Process Diagram)")

    asis_tobe_table = [
        ["การรับออเดอร์", "จดลงสมุดกระดาษ ลายมืออ่านยาก ผิดพลาดบ่อย", "กดเลือกเมนูผ่านหน้าจอสัมผัส POS", "ลดข้อผิดพลาดเป็น 0%"],
        ["การคิดเงิน/เงินทอน", "กดเครื่องคิดเลขแยก คิดในใจ ช้าช่วงเร่งด่วน", "ระบบคำนวณยอดรวมและเงินทอนอัตโนมัติสด", "ปิดบิลเสร็จสิ้นใน 1-2 วินาที"],
        ["การควบคุมสต็อก", "ตรวจนับด้วยสายตา สต็อกหมดโดยไม่รู้ตัว", "ตัดสต็อกอัตโนมัติ เตือนสต็อกต่ำ (<10)", "วางแผนสต็อกล่วงหน้าได้แม่นยำ"],
        ["การป้องกันข้อผิดพลาด", "ไม่มีระบบตรวจสอบ รับเงินแล้วทำไม่ได้", "ปิดปุ่มเมนูที่สต็อกเป็น 0 ทันที (FR-11)", "ป้องกันลูกค้ายกเลิกออเดอร์"],
        ["การออกใบเสร็จ", "เขียนบิลเงินสดด้วยมือ หรือไม่ออกใบเสร็จ", "สร้างใบเสร็จความร้อนมาตรฐานพร้อมเลขที่บิล", "สร้างความน่าเชื่อถือและโปร่งใส"],
        ["การสรุปยอดขาย", "รวมบิลกระดาษตอนปิดร้าน เสียเวลามาก", "แดชบอร์ดสรุปยอดขาย Real-time On-demand", "เจ้าของร้านดูยอดและเมนูขายดีได้ทันที"]
    ]
    add_table_data(["กระบวนการ", "เดิม (As-Is)", "ใหม่ (To-Be)", "ผลประโยชน์ที่ได้รับ"], asis_tobe_table, [1.1, 2.0, 1.9, 1.2])

    # ==========================================
    # SECTION 3: การวิเคราะห์ความต้องการ
    # ==========================================
    add_heading1("3. การวิเคราะห์ความต้องการ (Requirements Analysis)")
    add_body("จากการสัมภาษณ์เจ้าของร้านและพนักงานแคชเชียร์ พบปัญหาใหญ่คือสต็อกวัตถุดิบชอบหมดกะทันหันในช่วงลูกค้าหนาแน่น และความต้องการทราบยอดขายทันทีโดยไม่ต้องรอบวกบิลตอนปิดร้าน งบประมาณไม่เกิน 60,000 บาท และระบบต้องไม่ซับซ้อนเพื่อให้พนักงานใหม่เรียนรู้ได้เร็ว", "3.1 บันทึกการสัมภาษณ์ผู้ใช้จริง: ")

    add_heading2("3.2 ข้อกำหนดความต้องการเชิงหน้าที่ (Functional Requirements)")
    fr_list = [
        ("FR-01: ", "ระบบต้องแสดงรายการเมนูตามสาขาที่เลือก โดยแบ่งตามหมวดหมู่ (กาแฟ, ชา, ขนม) พร้อมราคาและสต็อกคงเหลือ"),
        ("FR-02: ", "ระบบต้องให้ผู้ใช้เลือกสินค้าและระบุจำนวนเข้าสู่ตะกร้าสินค้า และปรับเพิ่ม/ลดจำนวน หรือลบรายการได้ก่อนยืนยัน"),
        ("FR-03: ", "ระบบต้องคำนวณราคารวมของแต่ละรายการและยอดรวมทั้งสิ้นแบบเรียลไทม์ทันทีที่มีการเปลี่ยนแปลง"),
        ("FR-04: ", "ระบบต้องรองรับการเลือกวิธีชำระเงิน (เงินสด หรือ QR Code พร้อมเพย์) พร้อมคำนวณเงินทอนสำหรับเงินสด"),
        ("FR-05: ", "ระบบต้องบันทึกคำสั่งซื้อ สร้างหมายเลขออเดอร์ และออกใบเสร็จรับเงินดิจิทัลทันทีหลังยืนยันการชำระเงิน"),
        ("FR-06: ", "ระบบต้องปิดการใช้งานปุ่มยืนยันออเดอร์หากไม่มีสินค้าในตะกร้า (Error Prevention)"),
        ("FR-07: ", "ระบบต้องตัดสต็อกสินค้าในคลังทันทีเมื่อยืนยันคำสั่งซื้อ และบันทึกประวัติการเคลื่อนไหวสต็อก (Stock Movement)"),
        ("FR-08: ", "ระบบต้องแสดงสัญลักษณ์แจ้งเตือน 'ต่ำกว่าเกณฑ์' (Low Stock) เมื่อสต็อกเหลือน้อยกว่า 10 หน่วย"),
        ("FR-09: ", "ระบบต้องปฏิเสธการสั่งซื้อหากจำนวนสินค้าในคำสั่งซื้อมากกว่าสต็อกคงเหลือที่มีอยู่จริง"),
        ("FR-10: ", "ระบบต้องรองรับการปรับปรุงสต็อกวัตถุดิบด่วน แก้ไขราคา และเพิ่มเมนูใหม่ประจำแต่ละสาขา"),
        ("FR-11 (Feedback สำคัญ): ", "ระบบต้องปิดการใช้งานปุ่ม '+ เพิ่ม' (disabled) และแสดงสถานะ '✕ สินค้าหมด' สำหรับเมนูที่ stock_quantity = 0 ตั้งแต่หน้าแรก"),
        ("FR-12: ", "ระบบต้องกรองการแสดงผลรายการเมนู สต็อก และรายงานยอดขายตาม branch_id ที่เลือกใน Header อย่างเคร่งครัด")
    ]
    for prefix, desc in fr_list:
        add_bullet(desc, prefix)

    add_body("จากการทดสอบ Prototype สัปดาห์ที่ 13 พบว่าหากไม่มีการปิดปุ่มตั้งแต่หน้าจอแรก ผู้ใช้จะยังกดเลือกสินค้าที่หมดได้ จึงเพิ่มข้อกำหนด FR-11 เพื่อป้องกันข้อผิดพลาดตั้งแต่ต้นทาง (Error Prevention) และปรับปรุง FR-12 ให้ตัวเลือกสาขาคงตำแหน่งมุมบนขวาในทุกหน้าจออย่างคงเส้นคงวา", "3.3 บันทึกประวัติการปรับปรุง Requirement: ")

    # ==========================================
    # SECTION 4: User Stories และ Use Case
    # ==========================================
    add_heading1("4. User Stories และ Use Case")
    add_body("ระบบแบ่งผู้ใช้ออกเป็น 3 Actors หลัก ได้แก่ ลูกค้า (สั่งซื้อ/ชำระเงิน), พนักงานร้าน/แคชเชียร์ (รับออเดอร์/ตัดสต็อก/ออกใบเสร็จ), และเจ้าของร้าน/ผู้จัดการ (จัดการเมนู/ดูรายงานยอดขายเรียลไทม์)", "4.1 ภาพรวม Actors และ Use Cases: ")
    add_image_figure("usecase-diagram.jpg", "Use Case Diagram ระบบบริหารจัดการร้าน Minions Cafe")

    add_heading2("4.2 User Stories และ Acceptance Criteria (Given-When-Then)")
    user_stories_data = [
        ("US-01: บันทึกออเดอร์หน้าร้าน", "ในฐานะพนักงานแคชเชียร์ ฉันต้องการเลือกเมนูเครื่องดื่มและระบุจำนวนผ่านหน้าจอ เพื่อให้ระบบคำนวณยอดรวมให้อัตโนมัติ", "Given อยู่หน้ารับออเดอร์, When เลือกเมนูและจำนวน, Then ระบบบันทึกรายการในตะกร้าและคำนวณยอดรวมสดทันที โดยสั่งซื้อไม่เกินสต็อกคงเหลือ"),
        ("US-02: ชำระเงินและออกใบเสร็จ", "ในฐานะลูกค้า ฉันต้องการเลือกชำระเงินด้วยเงินสดหรือ QR และได้รับใบเสร็จรับเงินทันที เพื่อตรวจสอบความถูกต้อง", "Given มีรายการในตะกร้า, When บันทึกการชำระเงินสำเร็จ, Then ระบบคำนวณเงินทอนและออกใบเสร็จดิจิทัลแสดงเลขที่ วันเวลา สาขา และรายการครบถ้วน"),
        ("US-03: การตัดสต็อกและเตือนสต็อกต่ำ", "ในฐานะพนักงานร้าน ฉันต้องการให้ระบบตัดสต็อกอัตโนมัติและแจ้งเตือนเมื่อสต็อกต่ำ เพื่อเตรียมวัตถุดิบได้ทันการณ์", "Given ยืนยันออเดอร์สำเร็จ, When ระบบบันทึกรายการขาย, Then ระบบตัดสต็อกทันที หากสต็อกต่ำกว่า 10 จะขึ้นเตือนสีส้ม และหากสต็อกเป็น 0 จะปิดปุ่มเพิ่มสินค้า"),
        ("US-04: จัดการข้อมูลเมนูและสต็อก", "ในฐานะผู้จัดการร้าน ฉันต้องการเพิ่มเมนูใหม่ แก้ไขราคา และปรับปรุงสต็อก เพื่อให้ข้อมูลสอดคล้องกับการขายจริง", "Given อยู่หน้าจัดการเมนู, When ปรับสต็อกหรือแก้ไขราคา, Then ระบบบันทึกข้อมูลและอัปเดตไปยังหน้าจอ POS ประจำสาขานั้นทันที"),
        ("US-05: สรุปรายงานยอดขายเรียลไทม์", "ในฐานะเจ้าของร้าน ฉันต้องการดูรายงานยอดขายรวมและเมนูขายดีประจำสาขาแบบเรียลไทม์ เพื่อวางแผนการดำเนินงาน", "Given มีออเดอร์ใหม่เกิดขึ้น, When เปิดหน้ารายงานยอดขาย, Then แดชบอร์ดสรุปยอดขายรวม จำนวนออเดอร์ และเมนูขายดีจะอัปเดตทันทีโดยไม่ต้องรีเฟรช")
    ]
    for title, story, ac in user_stories_data:
        add_body(story, f"{title}: ")
        add_bullet(ac, "Acceptance Criteria: ")

    # ==========================================
    # SECTION 5: การออกแบบเชิงวัตถุ (OOAD)
    # ==========================================
    add_heading1("5. การออกแบบเชิงวัตถุ (Object-Oriented Analysis & Design - OOAD)")
    add_body("ระบบออกแบบ Domain Models ตามหลักการ OOAD โดยมีคลาสหลัก 3 คลาส ได้แก่ Order, OrderItem, และ MenuItem เชื่อมโยงกันตามความสัมพันธ์เชิงวัตถุ", "5.1 แผนภาพคลาสและอ็อบเจกต์: ")
    add_image_figure("wk06-class-diagram.png", "Class Diagram ระบบร้าน Minions Cafe")
    add_image_figure("wk06-object-diagram.png", "Object Diagram แสดงสถานะอ็อบเจกต์ขณะทำรายการขายจริง")

    add_body("ในคลาส Order และตาราง orders จริงในฐานข้อมูล จะไม่มีการเก็บฟิลด์ total_amount เนื่องจากยอดรวมถือเป็น Derived Attribute ตามหลัก Third Normal Form (3NF) โดยคำนวณสดผ่านเมธอด getSubtotal() ของ OrderItem (quantity * unit_price) ช่วยป้องกันปัญหา Data Inconsistency ได้อย่างเด็ดขาด", "5.2 การออกแบบตามหลัก 3NF ในระดับคลาส: ")

    # ==========================================
    # SECTION 6: การออกแบบฐานข้อมูล
    # ==========================================
    add_heading1("6. การออกแบบฐานข้อมูล (Database Design)")
    add_body("โครงสร้างฐานข้อมูลเชิงสัมพันธ์ประกอบด้วย 7 ตารางหลักที่เชื่อมโยงกันด้วย Foreign Key รองรับระบบหลายสาขาผ่านคอลัมน์ branch_id และมีตาราง stock_movement สำหรับเก็บบันทึก Audit Trail", "6.1 โครงสร้างฐานข้อมูลเชิงสัมพันธ์: ")
    add_image_figure("wk07-er-diagram.png", "Entity-Relationship Diagram (ER Diagram 7 ตาราง)")

    db_tables_summary = [
        ["branch", "branch_id (PK)", "name, address", "เก็บข้อมูลสาขา (สาขา 1 ม.บูรพา, สาขา 2 แหลมทอง)"],
        ["category", "category_id (PK)", "name", "หมวดหมู่สินค้า (1: กาแฟ, 2: ชา, 3: เบเกอรี่)"],
        ["employee", "employee_id (PK)", "branch_id (FK), name, role", "พนักงานประจำสาขา (สมชาย-Cashier, สมหญิง-Manager)"],
        ["menu_item", "menu_id (PK)", "branch_id (FK), category_id (FK), name, price, stock_quantity", "รายการเมนูและสต็อกคงเหลือแยกตามสาขา"],
        ["orders", "order_id (PK)", "branch_id (FK), employee_id (FK), payment_method, created_at", "หัวบิลคำสั่งซื้อ (ไม่มี total_amount ตามหลัก 3NF)"],
        ["order_item", "order_item_id (PK)", "order_id (FK), menu_id (FK), quantity, unit_price", "รายการสินค้าในคำสั่งซื้อ (คำนวณราคาย่อยได้)"],
        ["stock_movement", "movement_id (PK)", "menu_id (FK), quantity_change, moved_at", "บันทึกประวัติการตัดสต็อกเข้า-ออกตามแกนเวลา"]
    ]
    add_table_data(["ชื่อตาราง", "Primary Key", "Foreign Keys & Attributes", "หน้าที่ความรับผิดชอบ"], db_tables_summary, [1.1, 1.1, 2.2, 1.8])

    # ==========================================
    # SECTION 7: การออกแบบกระบวนการและพฤติกรรมระบบ
    # ==========================================
    add_heading1("7. การออกแบบกระบวนการและพฤติกรรมระบบ (Process & Behavioral Design)")
    add_body("กระบวนการสั่งซื้อและตัดสต็อก (Order-to-Stock) ได้รับการออกแบบให้ทำงานแบบ Atomic Transaction เพื่อป้องกันปัญหาความไม่สอดคล้องของข้อมูลเงินและสต็อก", "7.1 Sequence Diagram: ")
    add_image_figure("wk09-sequence-diagram.png", "Sequence Diagram แสดงขั้นตอนการสั่งซื้อ ตรวจสอบสต็อก และออกใบเสร็จ")

    add_body("เมื่อได้รับคำขอ POST /api/orders เซิร์ฟเวอร์จะทำ Pre-check ตรวจสอบสต็อกสินค้าทุกชิ้นในตะกร้าพร้อมจำลองการล็อกแถว (SELECT ... FOR UPDATE) หากมีรายการใดสต็อกไม่พอจะ Rollback ยกเลิกคำขอทันที หากสต็อกพอจะบันทึกออเดอร์ ตัดสต็อก บันทึกลง stock_movement และสร้างใบเสร็จส่งกลับสถานะ 201 Created", "7.2 ตรรกะทางธุรกิจในกระบวนการสั่งซื้อ: ")

    # ==========================================
    # SECTION 8: การออกแบบ Input/Output และ UI
    # ==========================================
    add_heading1("8. การออกแบบ Input/Output และส่วนประสานผู้ใช้")
    add_body("หน้าจอระบบได้รับการออกแบบตามหลัก Usability โดยแบ่งเป็น 3 หน้าจอหลัก: POS รับออเดอร์, จัดการเมนู & สต็อก, และรายงานยอดขาย พร้อมตัวเลือกสาขา (Branch Selector) ที่มุมบนขวาทุกหน้าจอ", "8.1 การออกแบบ Mid-Fi Wireframe: ")
    add_image_figure("wk10-wireframe.png", "Mid-Fi Wireframe หน้าจอ POS, จัดการเมนู และรายงานยอดขาย")
    add_image_figure("wk10-input-output.png", "Input / Output Design แสดงฟอร์มรับออเดอร์และใบเสร็จรับเงิน")

    add_body("หน้าจอ POS มีช่องค้นหาข้อความสด ปุ่มหมวดหมู่ ป้ายแจ้งเตือนสต็อก ตารางตะกร้าปรับจำนวนได้ และช่องคำนวณเงินสด/เงินทอนสด ส่วนใบเสร็จรับเงินออกแบบเลียนแบบกระดาษความร้อน 80mm พร้อมปุ่มพิมพ์ใบเสร็จความร้อนผ่านคำสั่ง window.print() และหน้ารายงานสรุปยอดขายแสดง KPI 4 ใบ พร้อมตารางจัดอันดับเมนูขายดีและกราฟเปรียบเทียบ 2 สาขา", "8.2 รายละเอียดฟอร์มและใบเสร็จ: ")

    # ==========================================
    # SECTION 9: สถาปัตยกรรมระบบ
    # ==========================================
    add_heading1("9. สถาปัตยกรรมระบบ (System Architecture - 4+1 View Model)")
    add_body("ระบบ Minions Cafe เลือกใช้สถาปัตยกรรมแบบ Monolithic Architecture ที่จัดโครงสร้างภายในแบบ Layered Architecture (Monolithic + Layered) เนื่องจากทีมงานมี 5 คน และมีระยะเวลาพัฒนา 1 เทอม ช่วยลด Overhead ของ Distributed Services และรักษาความสอดคล้องของข้อมูลได้ง่ายกว่า Microservices", "9.1 ภาพรวมสถาปัตยกรรม: ")
    
    add_image_figure("wk11-physical-view.png", "Physical View แสดงโหนดการติดตั้งบน localhost:3000 และพอร์ตฐานข้อมูล")
    add_image_figure("wk11-development-view.png", "Development View แสดงการแบ่ง Layer ภายใน Repository จริง")

    add_body("สถาปัตยกรรมภายในแบ่งเป็น Presentation Layer (HTML/CSS/JS), Routing & Controller Layer (server.js), Domain Models Layer (menuModel, orderModel) และ Data Store Layer สอดคล้องกับโครงสร้างโฟลเดอร์จริงใน Repository (Traceability)", "9.2 ความสอดคล้องของสถาปัตยกรรม: ")

    # ==========================================
    # SECTION 10: ผลการทดสอบ Usability
    # ==========================================
    add_heading1("10. ผลการทดสอบ Usability (Usability Testing)")
    add_body("ในสัปดาห์ที่ 12 ทีมงานได้ทดสอบระบบจริงกับผู้ใช้ตัวแทนด้วยระเบียบวิธี Task-Based Testing ร่วมกับ Think-Aloud Protocol ครอบคลุม 3 ภารกิจหลัก:", "10.1 ผลการทดสอบ 3 ภารกิจ: ")

    usability_data = [
        ["Task 1: Happy Path POS", "สั่ง Latte 1 แก้ว จ่ายเงินสด และออกใบเสร็จ", "42 วินาที", "สำเร็จ", "ปุ่มยืนยันออเดอร์เดิมกลืนกับพื้นหลัง → ปรับแก้เป็นปุ่มสีเขียว Emerald เด่นชัด"],
        ["Task 2: Out of Stock", "พยายามสั่ง Espresso เกินสต็อกที่มีอยู่ 8 แก้ว", "35 วินาที", "สำเร็จ", "พบว่าเมนูสต็อก 0 ยังคลิกได้ → แก้ไขโค้ดเพิ่ม FR-11 ปิดปุ่มทันทีที่สต็อกเป็น 0"],
        ["Task 3: Sales Report", "ตรวจสอบยอดขายรวมและเมนูขายดีหลังขายเสร็จ", "28 วินาที", "สำเร็จ", "ผู้ใช้พึงพอใจที่ข้อมูลสรุปอัปเดตแบบเรียลไทม์ทันทีโดยไม่ต้องกดรีเฟรชหน้าจอ"]
    ]
    add_table_data(["ภารกิจทดสอบ", "สถานการณ์ทดสอบ", "เวลาเฉลี่ย", "ผลลัพธ์", "ปัญหาที่พบและการปรับแก้จริง"], usability_data, [1.3, 1.8, 0.7, 0.7, 1.7])

    add_body("ทีมงานได้ดำเนินการแก้ไขปัญหาในระบบจริงครบทั้ง 4 ข้อ ได้แก่: 1. แก้ไข UI-02 (Critical) เพิ่ม FR-11 ปิดปุ่มเมนูสต็อก 0 ทันที 2. แก้ไข UI-01 (Major) ปรับปุ่มยืนยันออเดอร์เป็นสีเขียว Emerald เด่นชัด 3. แก้ไข UI-03 (Minor) เพิ่มช่องรับเงินสดและคำนวณเงินทอนสด และ 4. แก้ไข UI-04 (Minor) ปรับขนาดแถบเลือกสาขาให้ชัดเจนทุกหน้าจอ", "10.2 การปรับปรุงระบบจากผลการทดสอบ: ")

    # ==========================================
    # SECTION 11: ผลการรวมระบบ
    # ==========================================
    add_heading1("11. ผลการรวมระบบ (System Integration)")
    add_body("ในสัปดาห์ที่ 13 ได้ทำการทดสอบ End-to-End System Integration Flow ครบวงจร: Order -> Payment -> Stock Deduction -> Receipt -> Report", "11.1 วงจรการทำงานที่ทดสอบครบถ้วน: ")
    
    add_bullet("พนักงานเลือกสาขา 1 สั่ง Latte (45.-) + Espresso (35.-) + ครัวซองต์ (55.-) ยอดในตะกร้าคำนวณสดทันทีเป็น 135.00 บาท", "1. สั่งซื้อ (Order): ")
    add_bullet("เลือกชำระเงินสด กรอกรับเงินมา 200.00 บาท ระบบคำนวณเงินทอน 65.00 บาท แสดงผลสดทันที", "2. ชำระเงิน (Payment): ")
    add_bullet("กดยืนยันออเดอร์ ระบบส่งคำขอ POST /api/orders ตัดสต็อกในระบบจริงทันที (Latte เหลือ 11, Espresso เหลือ 7, ครัวซองต์ เหลือ 8)", "3. ตัดสต็อก (Stock Deduction): ")
    add_bullet("หน้าต่างใบเสร็จรับเงินเด้งขึ้นมาทันที แสดงเลขที่ ORD-20261030-105 วันเวลา สาขา พนักงาน และยอดรวมถูกต้อง 100%", "4. ออกใบเสร็จ (Receipt): ")
    add_bullet("เมื่อเปิดแท็บ 'รายงานยอดขาย' ยอดขายรวมสุทธิเพิ่มขึ้น 135 บาททันที และออเดอร์ใหม่ปรากฏในประวัติทันทีโดยไม่ต้องรีโหลดหน้าเว็บ", "5. สะท้อนยอดในรายงาน (Report): ")

    # ==========================================
    # SECTION 12: ผลการตรวจสอบคุณภาพและความปลอดภัย
    # ==========================================
    add_heading1("12. ผลการตรวจสอบคุณภาพและความปลอดภัยของซอฟต์แวร์")
    add_body("ในสัปดาห์ที่ 14 ทีมงานได้ตรวจสอบโค้ดจริงเทียบกับ Code Review Checklist 5 ข้อสำหรับระบบ CRUD:", "12.1 การตรวจสอบเทียบ Checklist: ")

    sec_checklist_data = [
        ["/api/menu", "GET", "ผ่าน", "ผ่าน (branch_id)", "ผ่าน (?)", "ผ่าน", "ไม่เกี่ยวข้อง", "ผ่าน"],
        ["/api/menu/:id", "PUT", "ผ่าน", "ผ่าน (แก้ไขแล้ว)", "ผ่าน (?)", "ผ่าน", "ไม่เกี่ยวข้อง", "ผ่าน"],
        ["/api/orders", "POST", "ผ่าน", "ผ่าน (branch_id)", "ผ่าน (?)", "ผ่าน", "ผ่าน (แก้ไขแล้ว)", "ผ่าน"],
        ["/api/reports/sales", "GET", "ผ่าน", "ผ่าน (branch_id)", "ผ่าน (?)", "ผ่าน", "ไม่เกี่ยวข้อง", "ผ่าน"]
    ]
    add_table_data(["Endpoint", "Method", "Input Valid.", "IDOR", "SQL Injection", "Error Hand.", "Race Condition", "สรุปผล"], sec_checklist_data, [1.1, 0.6, 0.8, 1.0, 0.8, 0.7, 0.8, 0.4])

    add_body("ตรวจพบความเสี่ยงระดับ Critical เรื่อง Race Condition ในการอ่านและตัดสต็อกเมื่อมีคำสั่งซื้อพร้อมกัน ทีมงานได้แก้ไขจริงโดยนำ Database Transaction ร่วมกับ SELECT ... FOR UPDATE มาใช้ใน server.js เพื่อล็อกแถวสต็อก ป้องกันสต็อกติดลบได้อย่างเด็ดขาด และแก้ไขปัญหา IDOR ใน PUT /api/menu/:id ด้วยการตรวจสอบสิทธิ์ความเป็นเจ้าของ branch_id", "12.2 การแก้ไขความเสี่ยงสำคัญ: ")

    # ==========================================
    # SECTION 13: สรุปผลและข้อเสนอแนะ
    # ==========================================
    add_heading1("13. สรุปผลและข้อเสนอแนะ (Conclusions & Recommendations)")
    add_body("โครงงาน Minions Cafe บรรลุวัตถุประสงค์ครบถ้วนทุกประการ สามารถทำงานได้อย่างถูกต้องทั้งในรูปแบบ Node.js Express Server และ Standalone Client Mode บทเรียนสำคัญคือการออกแบบที่มี Traceability เชื่อมโยง Requirement, Diagram และโค้ดจริง ช่วยลดข้อผิดพลาดในการพัฒนาย่างมาก", "13.1 สรุปผลสัมฤทธิ์และบทเรียน: ")
    add_body("ข้อจำกัดปัจจุบันคือระบบเซิร์ฟเวอร์ Express ใช้ In-memory Store สำหรับเก็บข้อมูลตัวอย่างเพื่อความสะดวกรวดเร็วในการนำเสนอ และหน้าต่าง QR PromptPay เป็นรูปแบบจำลอง (Simulation Modal)", "13.2 ข้อจำกัดของระบบ: ")
    add_body("แนวทางพัฒนาในอนาคตประกอบด้วย: การเชื่อมต่อ MySQL 8.0 อย่างถาวรผ่าน Connection Pool, การเพิ่มระบบ Login ด้วย JWT และ bcrypt, การเชื่อมต่อ Payment Gateway จริง (Omise / GB Prime Pay), และการพัฒนาระบบสมาชิกสะสมแต้ม 10 แต้มแลกฟรี 1 แก้ว", "13.3 แนวทางพัฒนาต่อยอด: ")

    # ==========================================
    # SECTION 14: ภาคผนวก
    # ==========================================
    add_heading1("14. ภาคผนวก (Appendix: AI Disclosure Forms)")
    add_body("เพื่อความโปร่งใสทางวิชาการ โครงงาน Minions Cafe ได้จัดทำแบบฟอร์มเปิดเผยการใช้งาน AI ครบถ้วนตลอดภาคการศึกษา โดยมีสาระสำคัญสรุปดังนี้:", "14.1 สรุปการเปิดเผยการใช้งาน AI: ")

    ai_data = [
        ["สัปดาห์ที่ 5", "docs/ai-disclosure/wk05-ai-disclosure.md", "ออกแบบ Git Branching และสคริปต์ตรวจ Repo", "Claude / Gemini", "ทดลองสลับ Branch ใน Git จริง"],
        ["สัปดาห์ที่ 9", "docs/ai-disclosure/wk09-ai-disclosure.md", "ช่วยร่าง API Spec และ Sequence Diagram", "Claude 3.5 Sonnet", "ตรวจสอบ Data Types เทียบ Use Case"],
        ["สัปดาห์ที่ 10", "docs/ai-disclosure/wk10-ai-disclosure.md", "จัดรูปแบบตาราง Input/Output และ SRS", "Claude 3.5 Sonnet", "ตรวจสอบฟิลด์เทียบกับ ER Diagram"],
        ["สัปดาห์ที่ 13", "docs/ai-disclosure/wk13-ai-disclosure.md", "ช่วยร่าง Test Scenarios สำหรับ E2E Test", "Claude 3.5 Sonnet", "ทดสอบกดสั่งซื้อจริงบนเว็บเบราว์เซอร์"]
    ]
    add_table_data(["สัปดาห์", "เอกสารทางการ", "ขอบเขตการใช้งาน", "เครื่องมือ AI", "การตรวจสอบโดยมนุษย์"], ai_data, [0.8, 2.1, 1.6, 0.9, 1.6])

    doc.save(OUT_DOCX)
    print(f"Successfully generated DOCX report at: {OUT_DOCX}")

if __name__ == "__main__":
    create_report_docx()

