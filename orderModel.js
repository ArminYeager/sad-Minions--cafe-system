class Order {
    constructor(order_id, branch_id, employee_id, payment_method, created_at) {
        // Field ตรงกับ Column ใน ER Diagram และ Database Schema
        this.order_id = order_id;
        this.branch_id = branch_id;
        this.employee_id = employee_id;
        this.payment_method = payment_method;
        this.created_at = created_at;
    }
    
    // หมายเหตุ: total_amount ไม่ถูกจัดเก็บในตาราง orders เพราะเป็นค่าที่คำนวณได้ (derived value) 
    // ตามหลัก 3NF จึงไม่มี field นี้
}

class OrderItem {
    constructor(order_item_id, order_id, menu_id, quantity, unit_price) {
        // Field ตรงกับ Column ใน ER Diagram และ Database Schema
        this.order_item_id = order_item_id;
        this.order_id = order_id;
        this.menu_id = menu_id;
        this.quantity = quantity;
        this.unit_price = unit_price;
    }

    // Method คำนวณที่ไม่ใช่ field ใน Database Schema
    getSubtotal() {
        return this.quantity * this.unit_price;
    }
}

module.exports = { Order, OrderItem };
