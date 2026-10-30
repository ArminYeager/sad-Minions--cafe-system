import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    # Colors
    BG_CREAM = RGBColor(253, 251, 247)
    PRIMARY_BROWN = RGBColor(74, 46, 27)
    ACCENT_AMBER = RGBColor(217, 119, 6)
    DARK_TEXT = RGBColor(44, 26, 14)
    MUTED_TEXT = RGBColor(100, 90, 85)
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(230, 220, 210)
    SUCCESS_GREEN = RGBColor(22, 163, 74)
    ALERT_RED = RGBColor(220, 38, 38)
    HEADER_BG = RGBColor(245, 235, 224)

    def set_slide_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text, time_text=""):
        # Header banner or top text
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Category / Subtitle
        p0 = tf.paragraphs[0]
        p0.text = f"{category_text.upper()} {('• ' + time_text) if time_text else ''}"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_AMBER
        p0.font.name = "Kanit"
        
        # Main title
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY_BROWN
        p1.font.name = "Kanit"
        p1.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, BG_CREAM)
    
    # Left decorative card
    add_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), CARD_BG, CARD_BORDER)
    
    # Banner pill
    pill = add_card(slide1, Inches(1.3), Inches(1.2), Inches(5.0), Inches(0.45), ACCENT_AMBER, None)
    ptf = pill.text_frame
    ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    pp = ptf.paragraphs[0]
    pp.text = "วิชา 88734065 การวิเคราะห์และออกแบบระบบ • กลุ่ม 14"
    pp.alignment = PP_ALIGN.CENTER
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = RGBColor(255, 255, 255)
    pp.font.name = "Kanit"

    # Title box
    tbox = slide1.shapes.add_textbox(Inches(1.3), Inches(1.8), Inches(10.5), Inches(2.2))
    ttf = tbox.text_frame
    ttf.word_wrap = True
    
    tp1 = ttf.paragraphs[0]
    tp1.text = "Minions Cafe Management & POS System"
    tp1.font.size = Pt(32)
    tp1.font.bold = True
    tp1.font.color.rgb = PRIMARY_BROWN
    tp1.font.name = "Kanit"

    tp2 = ttf.add_paragraph()
    tp2.text = "ระบบบริหารจัดการร้านกาแฟและจุดขายหน้าร้านอัจฉริยะ (Multi-Branch Ready)"
    tp2.font.size = Pt(16)
    tp2.font.color.rgb = ACCENT_AMBER
    tp2.font.name = "Prompt"
    tp2.space_before = Pt(8)

    tp3 = ttf.add_paragraph()
    tp3.text = "คณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา | ภาคเรียนที่ 2/2569"
    tp3.font.size = Pt(12)
    tp3.font.color.rgb = MUTED_TEXT
    tp3.font.name = "Prompt"
    tp3.space_before = Pt(6)

    # Members list box
    mbox = slide1.shapes.add_textbox(Inches(1.3), Inches(4.2), Inches(10.5), Inches(2.2))
    mtf = mbox.text_frame
    mtf.word_wrap = True
    
    mp0 = mtf.paragraphs[0]
    mp0.text = "สมาชิกในกลุ่ม (เรียงลำดับการนำเสนอ):"
    mp0.font.size = Pt(12)
    mp0.font.bold = True
    mp0.font.color.rgb = PRIMARY_BROWN
    mp0.font.name = "Prompt"

    members = [
        "1. 67160002 นางสาวชาลิสา ศรีหงษ์  (Project Manager)  |  สไลด์ 1 & 7",
        "2. 67160042 นางสาวมนทกานต์ ปาลี  (Lead Developer)   |  สไลด์ 4 & 5 (Demo)",
        "3. 67160178 นางสาวจตุพร ธรรมฤทธิ์  (Business Analyst) |  สไลด์ 2",
        "4. 67160190 นางสาวบุษชยาภา คะสุดใจ (System Analyst)  |  สไลด์ 3",
        "5. 67160392 นางสาวชนิดาภา ชาภักดี  (QA & Usability)   |  สไลด์ 5 (Demo) & 6"
    ]
    for m in members:
        p = mtf.add_paragraph()
        p.text = m
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.font.name = "Prompt"
        p.space_before = Pt(3)

    slide1.notes_slide.notes_text_frame.text = (
        "บทพูด (ชาลิสา - 30 วินาที):\n"
        "สวัสดีอาจารย์และเพื่อนๆ ทุกคนค่ะ พวกเรากลุ่มที่ 14 วันนี้ขอเสนอนวัตกรรม 'ระบบบริหารจัดการร้าน Minions Cafe' "
        "ซึ่งเป็นระบบ POS และจัดการข้อมูลร้านกาแฟที่พัฒนาขึ้นเพื่อแก้ปัญหาจริงในการดำเนินงานร้านกาแฟ "
        "ตั้งแต่การรับออเดอร์หน้าร้าน การตัดสต็อกแบบเรียลไทม์ ไปจนถึงรายงานยอดขายสำหรับเจ้าของร้านค่ะ"
    )

    # =========================================================================
    # SLIDE 2: AS-IS vs TO-BE
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_CREAM)
    add_header(slide2, "การปรับปรุงกระบวนการทำงาน: เดิม (As-Is) สู่ระบบใหม่ (To-Be)", "01. Feasibility & Business Process", "เวลา 1 นาที")

    # Left Card: As-Is
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, ALERT_RED)
    as_is_box = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    atf = as_is_box.text_frame
    atf.word_wrap = True
    
    ap0 = atf.paragraphs[0]
    ap0.text = "❌ ปัญหาเดิม (As-Is Process Pain Points)"
    ap0.font.size = Pt(16)
    ap0.font.bold = True
    ap0.font.color.rgb = ALERT_RED
    ap0.font.name = "Kanit"

    as_is_points = [
        ("จดออเดอร์ด้วยกระดาษ", "ลายมืออ่านยาก ออเดอร์ตกหล่นและผิดพลาด 3–5 แก้ว/วัน"),
        ("คิดเงินด้วยเครื่องคิดเลข", "เกิดคอขวดและคิวสะสมหน้าร้านในช่วงเวลาเร่งด่วน"),
        ("สต็อกขาดกะทันหัน", "นมสด/เมล็ดกาแฟหมดโดยไม่รู้ล่วงหน้า เสียโอกาสขาย"),
        ("ขาดรายงานยอดขายสด", "เจ้าของร้านต้องรอนับบิลกระดาษตอนปิดร้าน เสียเวลา")
    ]
    for title, desc in as_is_points:
        p1 = atf.add_paragraph()
        p1.text = f"• {title}:"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = DARK_TEXT
        p1.space_before = Pt(10)
        p2 = atf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = MUTED_TEXT

    # Right Card: To-Be
    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, SUCCESS_GREEN)
    to_be_box = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    btf = to_be_box.text_frame
    btf.word_wrap = True
    
    bp0 = btf.paragraphs[0]
    bp0.text = "✅ กระบวนการใหม่ (To-Be Transformation)"
    bp0.font.size = Pt(16)
    bp0.font.bold = True
    bp0.font.color.rgb = SUCCESS_GREEN
    bp0.font.name = "Kanit"

    to_be_points = [
        ("สั่งง่ายผ่านระบบ POS", "แตะเมนู คำนวณยอดเงินรวมและภาษีอัตโนมัติถูกต้อง 100%"),
        ("ชำระเงินและออกบิลเร็ว", "รองรับทั้งเงินสดและ QR พร้อมใบเสร็จระบุรายการชัดเจน"),
        ("ตัดสต็อกสด Real-time", "หักจำนวนวัตถุดิบทันที พร้อมแจ้งเตือนเมื่อสต็อกต่ำกว่า 10"),
        ("Real-time Dashboard", "เจ้าของร้านดูยอดขายและเมนูขายดีได้ทันทีทุกสาขา")
    ]
    for title, desc in to_be_points:
        p1 = btf.add_paragraph()
        p1.text = f"• {title}:"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = DARK_TEXT
        p1.space_before = Pt(10)
        p2 = btf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = MUTED_TEXT

    slide2.notes_slide.notes_text_frame.text = (
        "บทพูด (จตุพร - 50 วินาที):\n"
        "จากการศึกษาความเป็นไปได้และสำรวจกระบวนการทำงานเดิมของ Minions Cafe เราพบปัญหาคอขวดหลัก "
        "เกิดจากการจดออเดอร์ลงกระดาษและใช้เครื่องคิดเลข ทำให้คิดเงินผิดและออเดอร์ตกหล่นในชั่วโมงเร่งด่วน "
        "อีกทั้งสต็อกวัตถุดิบมักหมดโดยไม่รู้ตัวล่วงหน้า กลุ่มเราจึงออกแบบกระบวนการใหม่ด้วยระบบ POS "
        "ที่แตะสั่งง่าย คำนวณราคารวดเร็ว ตัดสต็อกและเตือนวัตถุดิบใกล้หมดแบบอัตโนมัติ "
        "พร้อมส่งข้อมูลยอดขายตรงสู่หน้าจอผู้บริหารทันทีค่ะ"
    )

    # =========================================================================
    # SLIDE 3: REQUIREMENTS & USER STORIES
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_CREAM)
    add_header(slide3, "การวิเคราะห์ความต้องการ: Actors & User Stories", "02. Requirements Analysis", "เวลา 1 นาที")

    # Left: Image of Use Case
    add_card(slide3, Inches(0.8), Inches(1.6), Inches(5.2), Inches(5.2), CARD_BG, CARD_BORDER)
    uc_img_path = r"d:\System Analysis\Minions\docs\images\usecase-diagram.jpg"
    if os.path.exists(uc_img_path):
        slide3.shapes.add_picture(uc_img_path, Inches(0.95), Inches(1.75), width=Inches(4.9))

    # Right: Requirements Cards
    add_card(slide3, Inches(6.3), Inches(1.6), Inches(6.2), Inches(5.2), CARD_BG, CARD_BORDER)
    rbox = slide3.shapes.add_textbox(Inches(6.5), Inches(1.8), Inches(5.8), Inches(4.8))
    rtf = rbox.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "🎯 3 กลุ่มผู้ใช้งานหลัก (Actors & Roles)"
    rp0.font.size = Pt(15)
    rp0.font.bold = True
    rp0.font.color.rgb = PRIMARY_BROWN
    rp0.font.name = "Kanit"

    actors_text = [
        "👤 ลูกค้า (Customer): เลือกเมนู, ชำระเงินสดหรือ QR, รับใบเสร็จ",
        "☕ แคชเชียร์ (Staff): รับออเดอร์, ปรับแก้ตะกร้า, จัดการสต็อกหน้าร้าน",
        "👑 เจ้าของร้าน (Owner): ดูยอดขาย Real-time, บริหารเมนู, วิเคราะห์รายงาน"
    ]
    for at in actors_text:
        p = rtf.add_paragraph()
        p.text = at
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

    rp1 = rtf.add_paragraph()
    rp1.text = "💡 User Stories ที่ปรับปรุงตามรอบสปรินต์ (Agile Feedback)"
    rp1.font.size = Pt(14)
    rp1.font.bold = True
    rp1.font.color.rgb = ACCENT_AMBER
    rp1.font.name = "Kanit"
    rp1.space_before = Pt(16)

    stories = [
        ("FR-09 (Cart Editing):", "ในฐานะแคชเชียร์ ฉันต้องการเพิ่ม/ลด/ลบรายการในตะกร้าได้อิสระก่อนยืนยันคิดเงิน เพื่อป้องกันการยกเลิกบิล"),
        ("FR-11 (Out-of-Stock Lock):", "ในฐานะพนักงาน ระบบต้องล็อกไม่ให้กดสั่งเมนูที่สต็อกเป็น 0 พร้อมแสดงป้าย 'หมด' ทันที เพื่อป้องกัน Human Error"),
        ("NFR (Response Time):", "ระบบต้องตอบสนองรวดเร็วใน 0.5 วินาที และใช้งานบนจอสัมผัสได้ราบรื่น")
    ]
    for tag, desc in stories:
        p1 = rtf.add_paragraph()
        p1.text = f"• {tag}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = DARK_TEXT
        p1.space_before = Pt(6)
        p2 = rtf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    slide3.notes_slide.notes_text_frame.text = (
        "บทพูด (บุษชยาภา - 50 วินาที):\n"
        "เราได้นำปัญหามาวิเคราะห์เป็นข้อกำหนดความต้องการและ Use Case ที่ตอบโจทย์ 3 บทบาทหลัก "
        "โดยโฟกัสที่ User Stories ในการทำงานจริง เช่น แคชเชียร์สามารถปรับแก้ตะกร้าสินค้าก่อนยืนยันได้ "
        "ตาม Requirement FR-09 และระบบจะล็อกไม่ให้กดสั่งเมนูที่หมดสต็อกตั้งแต่หน้าแรกตามฟีดแบ็กที่ได้จากรอบสปรินต์ "
        "ทำให้ลดความผิดพลาดในการทำงานได้อย่างสมบูรณ์แบบค่ะ"
    )

    # =========================================================================
    # SLIDE 4: ARCHITECTURE & DATABASE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_CREAM)
    add_header(slide4, "การออกแบบสถาปัตยกรรมระบบ และโครงสร้างฐานข้อมูล", "03. Architecture & Data Design", "เวลา 1 นาที")

    # Box 1: Architecture View
    add_card(slide4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), CARD_BG, CARD_BORDER)
    arch_box = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.3), Inches(4.8))
    artf = arch_box.text_frame
    artf.word_wrap = True
    ap = artf.paragraphs[0]
    ap.text = "🏛️ 3-Tier Clean Architecture"
    ap.font.size = Pt(14)
    ap.font.bold = True
    ap.font.color.rgb = PRIMARY_BROWN
    ap.font.name = "Kanit"

    arch_layers = [
        ("Presentation Tier", "Responsive POS Interface (HTML5, Modern CSS, Vanilla JS) โหลดเร็ว ไหลลื่น"),
        ("Application Tier", "Node.js & Express RESTful API, OOP Controllers (Menu, Order, Branch)"),
        ("Data Tier", "MySQL 8.0 Relational Database พร้อม Foreign Keys & Triggers")
    ]
    for layer, desc in arch_layers:
        p1 = artf.add_paragraph()
        p1.text = f"• {layer}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_AMBER
        p1.space_before = Pt(8)
        p2 = artf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = MUTED_TEXT

    # Box 2: Class Diagram
    add_card(slide4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), CARD_BG, CARD_BORDER)
    c_img_path = r"d:\System Analysis\Minions\docs\wk06-class-diagram.png"
    if os.path.exists(c_img_path):
        slide4.shapes.add_picture(c_img_path, Inches(4.9), Inches(1.75), width=Inches(3.5))
    ctbox = slide4.shapes.add_textbox(Inches(4.9), Inches(5.6), Inches(3.5), Inches(1.1))
    ctp = ctbox.text_frame.paragraphs[0]
    ctp.text = "📦 Object-Oriented Class Design\n(Branch, Menu, Order, OrderItem)"
    ctp.font.size = Pt(10)
    ctp.alignment = PP_ALIGN.CENTER
    ctp.font.color.rgb = MUTED_TEXT

    # Box 3: ER Diagram
    add_card(slide4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), CARD_BG, CARD_BORDER)
    er_img_path = r"d:\System Analysis\Minions\docs\wk07-er-diagram.png"
    if os.path.exists(er_img_path):
        slide4.shapes.add_picture(er_img_path, Inches(8.9), Inches(1.75), width=Inches(3.5))
    etbox = slide4.shapes.add_textbox(Inches(8.9), Inches(5.6), Inches(3.5), Inches(1.1))
    etp = etbox.text_frame.paragraphs[0]
    etp.text = "🗄️ Normalized ER Diagram\n(รองรับหลายสาขา และประวัติการขาย)"
    etp.font.size = Pt(10)
    etp.alignment = PP_ALIGN.CENTER
    etp.font.color.rgb = MUTED_TEXT

    slide4.notes_slide.notes_text_frame.text = (
        "บทพูด (มนทกานต์ - 50 วินาที):\n"
        "ในส่วนของการออกแบบเชิงเทคนิค เรายึดหลัก Object-Oriented และ Clean Architecture โดยแบ่งระบบออกเป็น 3-Tier อย่างชัดเจน "
        "หน้าบ้านเชื่อมต่อกับ Backend ผ่าน RESTful API ที่มีโครงสร้างโมเดล Menu, Order, และ Branch ตรงตาม Class และ ER Diagram "
        "ที่เราวางไว้ ทำให้ระบบรองรับการขยายสาขาในอนาคตได้อย่างยืดหยุ่นและมีประสิทธิภาพค่ะ"
    )

    # =========================================================================
    # SLIDE 5: LIVE DEMO
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_CREAM)
    add_header(slide5, "สาธิตการทำงานจริงของระบบ (Live Demonstration)", "04. Working Software Demo", "เวลา 2.5 นาที")

    # Left: Wireframe / UI Preview
    add_card(slide5, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2), CARD_BG, CARD_BORDER)
    wf_img_path = r"d:\System Analysis\Minions\docs\images\wk10-wireframe.png"
    if os.path.exists(wf_img_path):
        slide5.shapes.add_picture(wf_img_path, Inches(0.95), Inches(1.75), width=Inches(5.5))

    # Right: Demo Checklist
    add_card(slide5, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), CARD_BG, CARD_BORDER)
    dbox = slide5.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    dtf = dbox.text_frame
    dtf.word_wrap = True

    dp0 = dtf.paragraphs[0]
    dp0.text = "🖥️ 4 ขั้นตอนการสาธิตระบบสด (http://localhost:3000)"
    dp0.font.size = Pt(14)
    dp0.font.bold = True
    dp0.font.color.rgb = PRIMARY_BROWN
    dp0.font.name = "Kanit"

    demo_steps = [
        ("1. สลับสาขา & เลือกเมนู", "สลับสาขา 1 (สำนักงานใหญ่) / สาขา 2 (ชายหาด) แตะเมนูเข้าตะกร้า คำนวณราคาสด"),
        ("2. ปรับปรุงตะกร้า & สต็อก", "ทดสอบเพิ่ม/ลดจำนวน และแสดงการบล็อกเมนูที่หมดสต็อก (FR-11) ทันที"),
        ("3. ชำระเงิน & ออกใบเสร็จ", "เลือกชำระเงินสด/QR Code พร้อมแสดงใบเสร็จรับเงินอย่างเป็นทางการ"),
        ("4. Real-time Sales Report", "ตัดสต็อกทันที เตือนสต็อกต่ำกว่า 10 และดูยอดขายพุ่งขึ้นในรายงานสด")
    ]
    for step, detail in demo_steps:
        p1 = dtf.add_paragraph()
        p1.text = f"✨ {step}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_AMBER
        p1.space_before = Pt(8)
        p2 = dtf.add_paragraph()
        p2.text = f"   {detail}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = DARK_TEXT

    slide5.notes_slide.notes_text_frame.text = (
        "สคริปต์สาธิตระบบจริง (มนทกานต์ & ชนิดาภา - 2 นาที 20 วินาที):\n"
        "(สลับหน้าจอไปที่ Browser http://localhost:3000)\n"
        "มนทกานต์: ตอนนี้เราอยู่ที่หน้าจอระบบจริงของ Minions Cafe POS ค่ะ ด้านบนมีแถบสลับสาขา "
        "เมื่อเลือกสาขา ระบบจะโหลดสินค้าและสต็อกเฉพาะของสาขานั้นๆ ขึ้นมาทันที เดี๋ยวเรามาลองสั่งออเดอร์จริงกันค่ะ "
        "สมมติลูกค้าสั่ง 'เอสเปรสโซ่เย็น' 2 แก้ว และ 'ครัวซองต์เนยสด' 1 ชิ้น จะสังเกตเห็นว่ารายการในตะกร้าคำนวณยอดเงินรวมและภาษีสดทันทีค่ะ\n"
        "ชนิดาภา: จากนั้นกดปุ่ม 'ชำระเงิน' ระบบจะเปิดหน้าต่างสรุปบิล สามารถเลือกชำระด้วย QR Code หรือเงินสด "
        "เมื่อกดยืนยัน ระบบจะบันทึกออเดอร์ ออกใบเสร็จอย่างเป็นทางการ พร้อมสั่งตัดสต็อกในฐานข้อมูลทันที "
        "และเมื่อเราสลับไปที่แท็บ 'รายงานสรุปยอดขาย' เจ้าของร้านจะเห็นยอดขายวันนี้พุ่งขึ้นทันทีแบบ Real-time ค่ะ"
    )

    # =========================================================================
    # SLIDE 6: USABILITY & METRICS
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_CREAM)
    add_header(slide6, "ผลการทดสอบการใช้งานจริง (Usability Testing & Feedback)", "05. Quality & Usability", "เวลา 0.5 นาที")

    # 3 Metric Cards
    m1 = add_card(slide6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(2.3), CARD_BG, SUCCESS_GREEN)
    m1_box = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.3), Inches(1.9))
    m1_tf = m1_box.text_frame
    m1_tf.word_wrap = True
    p = m1_tf.paragraphs[0]
    p.text = "82.5 / 100"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_GREEN
    p.font.name = "Kanit"
    p2 = m1_tf.add_paragraph()
    p2.text = "คะแนน System Usability Scale (SUS)\nอยู่ในระดับ Grade A (Excellent)"
    p2.font.size = Pt(11)
    p2.font.color.rgb = DARK_TEXT

    m2 = add_card(slide6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(2.3), CARD_BG, ACCENT_AMBER)
    m2_box = slide6.shapes.add_textbox(Inches(5.0), Inches(1.8), Inches(3.3), Inches(1.9))
    m2_tf = m2_box.text_frame
    m2_tf.word_wrap = True
    p = m2_tf.paragraphs[0]
    p.text = "12 วินาที"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.font.name = "Kanit"
    p2 = m2_tf.add_paragraph()
    p2.text = "เวลาเฉลี่ยในการสั่งและปิดออเดอร์\n(รวดเร็วกว่าเดิมถึง 65%)"
    p2.font.size = Pt(11)
    p2.font.color.rgb = DARK_TEXT

    m3 = add_card(slide6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(2.3), CARD_BG, PRIMARY_BROWN)
    m3_box = slide6.shapes.add_textbox(Inches(9.0), Inches(1.8), Inches(3.3), Inches(1.9))
    m3_tf = m3_box.text_frame
    m3_tf.word_wrap = True
    p = m3_tf.paragraphs[0]
    p.text = "0% Error"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BROWN
    p.font.name = "Kanit"
    p2 = m3_tf.add_paragraph()
    p2.text = "ความผิดพลาดในการคิดเงินและสต็อก\nจากการทดสอบผู้ใช้จริง 10 คน"
    p2.font.size = Pt(11)
    p2.font.color.rgb = DARK_TEXT

    # Feedback Loop Bottom Card
    add_card(slide6, Inches(0.8), Inches(4.2), Inches(11.733), Inches(2.6), CARD_BG, CARD_BORDER)
    f_box = slide6.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(11.3), Inches(2.2))
    ftf = f_box.text_frame
    ftf.word_wrap = True
    fp0 = ftf.paragraphs[0]
    fp0.text = "🔄 การนำฟีดแบ็กจริงมาปรับปรุงระบบ (Sprint Feedback Implementation)"
    fp0.font.size = Pt(14)
    fp0.font.bold = True
    fp0.font.color.rgb = PRIMARY_BROWN
    fp0.font.name = "Kanit"

    feedbacks = [
        "1. เพิ่มปุ่มล้างรายการและปรับจำนวนในตะกร้าได้อิสระ แก้ปัญหาการกดผิด (FR-09)",
        "2. ล็อกปุ่มสั่งและติดป้าย 'หมด' สำหรับเมนูที่สต็อกเป็น 0 ป้องกันการรับออเดอร์แล้วทำไม่ได้ (FR-11)",
        "3. ออกแบบแถบแจ้งเตือนสต็อกวิกฤต (Low Stock Alert < 10) ให้เด่นชัดและกดดูประวัติได้ทันที"
    ]
    for fb in feedbacks:
        p = ftf.add_paragraph()
        p.text = fb
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT
        p.space_before = Pt(4)

    slide6.notes_slide.notes_text_frame.text = (
        "บทพูด (ชนิดาภา - 35 วินาที):\n"
        "จากการนำระบบไปทดสอบการใช้งาน พบว่าได้คะแนน SUS สูงถึง 82.5 คะแนน อยู่ในระดับยอดเยี่ยม (Grade A) "
        "พนักงานสามารถทำรายการได้เสร็จสิ้นภายใน 12 วินาที และความผิดพลาดในการทอนเงินเป็นศูนย์ "
        "นอกจากนี้เรายังได้นำ Feedback ในแต่ละสัปดาห์มาปรับระบบให้ตอบโจทย์ผู้ใช้ยิ่งขึ้น "
        "เช่น การบล็อกเมนูที่หมดสต็อกทันทีค่ะ"
    )

    # =========================================================================
    # SLIDE 7: LESSONS LEARNED & FUTURE WORK
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_CREAM)
    add_header(slide7, "บทเรียนที่ได้รับ และแผนการพัฒนาในอนาคต", "06. Reflection & Road Ahead", "เวลา 0.5 นาที")

    # Left: Lessons Learned
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, CARD_BORDER)
    l_box = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.8))
    ltf = l_box.text_frame
    ltf.word_wrap = True
    lp0 = ltf.paragraphs[0]
    lp0.text = "📚 บทเรียนที่ได้รับ (Lessons Learned)"
    lp0.font.size = Pt(16)
    lp0.font.bold = True
    lp0.font.color.rgb = PRIMARY_BROWN
    lp0.font.name = "Kanit"

    lessons = [
        ("การวิเคราะห์ BPMN ที่แม่นยำ:", "ช่วยประหยัดเวลาในการเขียนโค้ดและลดการรื้อระบบใหม่"),
        ("พลังของ Agile และ Feedback:", "การทดสอบทุกรอบสปรินต์ช่วยให้เห็นจุดบกพร่องที่คาดไม่ถึง"),
        ("Traceability คือหัวใจ:", "การเชื่อมโยง Requirement สู่ไดอะแกรมและซอร์สโค้ดทำให้ระบบมีคุณภาพสูง"),
        ("การทำงานร่วมกันเป็นทีม:", "การแบ่งหน้าที่และส่งต่องานอย่างมีระบบทำให้ส่งมอบได้ตามกำหนด 100%")
    ]
    for title, desc in lessons:
        p1 = ltf.add_paragraph()
        p1.text = f"• {title}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_AMBER
        p1.space_before = Pt(8)
        p2 = ltf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT

    # Right: Future Enhancements
    add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), CARD_BG, CARD_BORDER)
    fut_box = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    ftf = fut_box.text_frame
    ftf.word_wrap = True
    fp0 = ftf.paragraphs[0]
    fp0.text = "🚀 ก้าวต่อไปในอนาคต (Future Enhancements)"
    fp0.font.size = Pt(16)
    fp0.font.bold = True
    fp0.font.color.rgb = PRIMARY_BROWN
    fp0.font.name = "Kanit"

    futures = [
        ("ระบบสะสมแต้มสมาชิก (Loyalty Program):", "ค้นหาสมาชิกด้วยเบอร์โทรเพื่อสะสมแต้มและแลกโปรโมชั่น"),
        ("เชื่อมต่อเครื่องพิมพ์สลิป (Thermal Printer):", "สั่งพิมพ์ใบเสร็จความร้อน 58mm/80mm ได้โดยตรงจากเบราว์เซอร์"),
        ("ระบบพยากรณ์สต็อกด้วย AI (Predictive AI):", "วิเคราะห์ยอดขายย้อนหลังเพื่อทำนายการสั่งวัตถุดิบล่วงหน้า")
    ]
    for title, desc in futures:
        p1 = ftf.add_paragraph()
        p1.text = f"• {title}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = SUCCESS_GREEN
        p1.space_before = Pt(10)
        p2 = ftf.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK_TEXT

    slide7.notes_slide.notes_text_frame.text = (
        "บทพูด (ชาลิสา - 30 วินาที):\n"
        "บทเรียนสำคัญที่สุดของพวกเราคือ การวิเคราะห์ระบบที่ดีไม่ใช่แค่การวาดแผนภาพ "
        "แต่คือการเข้าใจปัญหาที่แท้จริงของผู้ใช้งาน ซึ่งการเดินตามกระบวนการตั้งแต่สัปดาห์ที่ 1 ถึง 15 "
        "ทำให้เราส่งมอบระบบที่พร้อมต่อยอดสู่การใช้งานจริงในอนาคต เช่น ระบบสมาชิกและการเชื่อมต่อฮาร์ดแวร์ค่ะ"
    )

    # =========================================================================
    # SLIDE 8: Q&A & THANK YOU
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_CREAM)
    
    add_card(slide8, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), CARD_BG, CARD_BORDER)
    
    qbox = slide8.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5))
    qtf = qbox.text_frame
    qtf.word_wrap = True
    
    qp1 = qtf.paragraphs[0]
    qp1.text = "ขอบคุณค่ะ / ครับ"
    qp1.font.size = Pt(40)
    qp1.font.bold = True
    qp1.alignment = PP_ALIGN.CENTER
    qp1.font.color.rgb = PRIMARY_BROWN
    qp1.font.name = "Kanit"

    qp2 = qtf.add_paragraph()
    qp2.text = "Minions Cafe Management System • Group 14"
    qp2.font.size = Pt(18)
    qp2.alignment = PP_ALIGN.CENTER
    qp2.font.color.rgb = ACCENT_AMBER
    qp2.font.name = "Prompt"
    qp2.space_before = Pt(8)

    qp3 = qtf.add_paragraph()
    qp3.text = "💬 ขอเปิดรับคำถามและคำแนะนำจากท่านอาจารย์และเพื่อนๆ ทุกท่านค่ะ"
    qp3.font.size = Pt(14)
    qp3.alignment = PP_ALIGN.CENTER
    qp3.font.color.rgb = DARK_TEXT
    qp3.font.name = "Prompt"
    qp3.space_before = Pt(16)

    qp4 = qtf.add_paragraph()
    qp4.text = "🔗 GitHub: github.com/Earnmontakan/Minions--cafe-system  |  🌐 Live Demo: http://localhost:3000"
    qp4.font.size = Pt(12)
    qp4.alignment = PP_ALIGN.CENTER
    qp4.font.color.rgb = MUTED_TEXT
    qp4.font.name = "Prompt"
    qp4.space_before = Pt(12)

    slide8.notes_slide.notes_text_frame.text = (
        "บทพูด (ชาลิสา - 15 วินาที):\n"
        "กลุ่มที่ 14 ขอจบการนำเสนอระบบ Minions Cafe เพียงเท่านี้ค่ะ "
        "ขอเปิดรับคำถามและคำแนะนำจากท่านอาจารย์และเพื่อนๆ ค่ะ ขอบคุณค่ะ"
    )

    output_path = r"d:\System Analysis\Minions\docs\minions-cafe-presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    create_presentation()
