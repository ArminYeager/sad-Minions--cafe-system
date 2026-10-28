class MenuItem {
    constructor(menu_id, branch_id, category_id, name, price, stock_quantity) {
        // Field ตรงกับ Column ใน ER Diagram และ Database Schema (snake_case)
        this.menu_id = menu_id;
        this.branch_id = branch_id;
        this.category_id = category_id;
        this.name = name;
        this.price = price;
        this.stock_quantity = stock_quantity;
    }
}

module.exports = { MenuItem };
