import tkinter as tk
from tkinter import messagebox
import csv
import os

def check_login(username, password, role):
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Kiểm tra xem dòng có đủ 3 phần tử không
                if len(row) < 3:
                    continue  # Bỏ qua các dòng không hợp lệ
                if row[0] == username and row[1] == password and row[2] == role:
                    return True
        return False
    except FileNotFoundError:
        return False

# Hàm lưu tài khoản vào file CSV
def save_account_to_csv(username, password, role):
    with open('accounts.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role])

# Hàm xử lý đăng ký
def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    role = role_var.get()  # Lấy vai trò từ menu thả xuống
    
    if username and password and confirm_password and role:
        if password == confirm_password:
            save_account_to_csv(username, password, role)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            login_screen()  # Quay lại màn hình đăng nhập sau khi đăng ký thành công
        else:
            messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp!")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

# Hàm xử lý đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Chỉ kiểm tra tài khoản và mật khẩu với hai vai trò
    if check_login(username, password, "Khách hàng") or check_login(username, password, "Nhân viên bán hàng"):
        role = "Khách hàng" if check_login(username, password, "Khách hàng") else "Nhân viên bán hàng"
        messagebox.showinfo("Đăng nhập", f"Đăng nhập thành công với vai trò: {role}")
        
        if role == 'Khách hàng':
            customer_dashboard()  # Chuyển sang giao diện của Khách hàng
        elif role == 'Nhân viên bán hàng':
            salesperson_dashboard()  # Chuyển sang giao diện của Nhân viên bán hàng
    else:
        messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

# Giao diện chính sau khi đăng nhập thành công 
def customer_dashboard():
    clear_screen()
    lbl_customer = tk.Label(window, text="Chào mừng Khách hàng!", font=("Arial", 16))
    lbl_customer.pack(pady=10)
    
    # Nút mua quần áo mùa đông
    btn_winter_clothes = tk.Button(window, text="Mua Quần áo mùa đông", font=("Arial", 14), command=buy_winter_clothes)
    btn_winter_clothes.pack(pady=10)
    
    # Nút mua quần áo mùa hè
    btn_summer_clothes = tk.Button(window, text="Mua Quần áo mùa hè", font=("Arial", 14), command=buy_summer_clothes)
    btn_summer_clothes.pack(pady=10)

# Hàm xử lý khi mua quần áo mùa đông
def buy_winter_clothes():
    messagebox.showinfo("Mua sắm", "Bạn đã chọn mua Quần áo mùa đông!")

# Hàm xử lý khi mua quần áo mùa hè
def buy_summer_clothes():
    messagebox.showinfo("Mua sắm", "Bạn đã chọn mua Quần áo mùa hè!")

# Hàm lưu thông tin đơn hàng vào file CSV
def save_order_to_csv(order_items, username):
    try:
        # Đường dẫn tới file CSV
        file_path = 'orders.csv'
        
        # Mở file CSV và ghi thông tin đơn hàng
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Ghi mỗi sản phẩm trong đơn hàng vào CSV
            for item in order_items:
                writer.writerow([username, item])
        # Hiển thị thông báo thành công
        messagebox.showinfo("Xác Nhận Đơn Hàng", "Đơn hàng đã được lưu!")
    except Exception as e:
        print(f"Lỗi khi lưu đơn hàng: {e}")
        messagebox.showerror("Lỗi", "Không thể lưu đơn hàng.")

# Hàm xác nhận đơn hàng, lưu vào CSV
def confirm_order():
    try:
        # Lấy danh sách các món đã chọn từ Listbox
        selected_items = list(listbox.curselection())
        
        if selected_items:
            # Lấy tên người dùng từ biến toàn cục hoặc truyền vào đúng cách
            username = 'khachhang'  # Cần thay đổi thành giá trị thực của người dùng hiện tại
            
            # Lấy nội dung của các món đã chọn
            order_items = [listbox.get(i) for i in selected_items]
            
            # Lưu đơn hàng vào file CSV
            save_order_to_csv(order_items, username)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một sản phẩm.")
    except Exception as e:
        print(f"Lỗi trong quá trình xác nhận đơn hàng: {e}")

# Hàm hiển thị giao diện đặt hàng quần áo mùa đông
def winter_clothes_order_screen():
    clear_screen()
    global listbox
    lbl_title = tk.Label(window, text="Quần áo mùa đông", font=("Arial", 16))
    lbl_title.pack(pady=10)

    # Danh sách quần áo
    listbox = tk.Listbox(window, width=50, height=5, selectmode=tk.MULTIPLE)
    listbox.insert(1, "Áo khoác mùa đông - 500,000 VND")
    listbox.insert(2, "Quần dài mùa đông - 300,000 VND")
    listbox.pack(pady=10)

    # Nút xác nhận đơn hàng
    btn_confirm = tk.Button(window, text="Xác Nhận Đơn Hàng", width=20, command=confirm_order)
    btn_confirm.pack(pady=5)

    # Nút quay lại
    btn_back = tk.Button(window, text="Quay Lại", width=20, command=customer_dashboard)
    btn_back.pack(pady=5)

# Hàm hiển thị giao diện đặt hàng quần áo mùa hè
def summer_clothes_order_screen():
    clear_screen()
    global listbox
    lbl_title = tk.Label(window, text="Quần áo mùa hè", font=("Arial", 16))
    lbl_title.pack(pady=10)

    # Danh sách quần áo
    listbox = tk.Listbox(window, width=50, height=5, selectmode=tk.MULTIPLE)
    listbox.insert(1, "Áo thun mùa hè - 200,000 VND")
    listbox.insert(2, "Quần short mùa hè - 150,000 VND")
    listbox.pack(pady=10)

    # Nút xác nhận đơn hàng
    btn_confirm = tk.Button(window, text="Xác Nhận Đơn Hàng", width=20, command=confirm_order)
    btn_confirm.pack(pady=5)

    # Nút quay lại
    btn_back = tk.Button(window, text="Quay Lại", width=20, command=customer_dashboard)
    btn_back.pack(pady=5)

# Hàm làm sạch màn hình trước khi hiển thị nội dung mới
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

# Hàm quay lại giao diện chính của khách hàng
def customer_dashboard():
    clear_screen()
    lbl_title = tk.Label(window, text="Chào mừng Khách hàng!", font=("Arial", 16))
    lbl_title.pack(pady=10)

    btn_winter_clothes = tk.Button(window, text="Quần áo mùa đông", width=20, command=winter_clothes_order_screen)
    btn_winter_clothes.pack(pady=5)

    btn_summer_clothes = tk.Button(window, text="Quần áo mùa hè", width=20, command=summer_clothes_order_screen)
    btn_summer_clothes.pack(pady=5)

def salesperson_dashboard():
    clear_screen()

    # Hiển thị dòng chào mừng
    lbl_salesperson = tk.Label(window, text="Nhân viên bán hàng!", font=("Arial", 16))
    lbl_salesperson.pack(pady=10)

    # Thêm nút "Tài khoản khách hàng"
    btn_manage_customers = tk.Button(window, text="Quản lý Tài khoản Khách hàng", width=25, command=add_customer_account)
    btn_manage_customers.pack(pady=10)

    # Thêm tùy chọn Nhập hàng
    btn_import_goods = tk.Button(window, text="Nhập hàng", width=20, command=goods_import_screen)
    btn_import_goods.pack(pady=5)

    # Nút xuất hàng
    btn_export_goods = tk.Button(window, text="Xuất hàng", width=20)
    btn_export_goods.pack(pady=5)

    # Thêm nút "Đăng xuất"
    btn_logout = tk.Button(window, text="Đăng xuất", width=25, command=login_screen)
    btn_logout.pack(pady=10)

def check_login(username, password, role):
    try:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue  # Bỏ qua các dòng không hợp lệ
                if row[0] == username and row[1] == password and row[2] == role:
                    return True
        return False
    except FileNotFoundError:
        return False

# Hàm lưu tài khoản vào file CSV
def save_account_to_csv(username, password, role):
    with open('accounts.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role])

# Hàm xử lý đăng ký
def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    role = role_var.get()
    
    if username and password and confirm_password and role:
        if password == confirm_password:
            save_account_to_csv(username, password, role)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            login_screen()
        else:
            messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp!")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

# Hàm xử lý đăng nhập
def login():
    username = entry_username.get()
    password = entry_password.get()

    if check_login(username, password, "Khách hàng") or check_login(username, password, "Nhân viên bán hàng"):
        role = "Khách hàng" if check_login(username, password, "Khách hàng") else "Nhân viên bán hàng"
        messagebox.showinfo("Đăng nhập", f"Đăng nhập thành công với vai trò: {role}")
        
        if role == 'Khách hàng':
            customer_dashboard()
        elif role == 'Nhân viên bán hàng':
            salesperson_dashboard()
    else:
        messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")

def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

def customer_dashboard():
    clear_screen()
    lbl_title = tk.Label(window, text="Chào mừng Khách hàng!", font=("Arial", 16))
    lbl_title.pack(pady=10)

    btn_winter_clothes = tk.Button(window, text="Quần áo mùa đông", command=winter_clothes_order_screen)
    btn_winter_clothes.pack(pady=5)

    btn_summer_clothes = tk.Button(window, text="Quần áo mùa hè", command=summer_clothes_order_screen)
    btn_summer_clothes.pack(pady=5)

def salesperson_dashboard():
    clear_screen()

    lbl_salesperson = tk.Label(window, text="Nhân viên bán hàng!", font=("Arial", 16))
    lbl_salesperson.pack(pady=10)

    btn_manage_customers = tk.Button(window, text="Quản lý Tài khoản Khách hàng", command=add_customer_account)
    btn_manage_customers.pack(pady=10)

    btn_import_goods = tk.Button(window, text="Nhập hàng", command=goods_import_screen)
    btn_import_goods.pack(pady=5)

    btn_export_goods = tk.Button(window, text="Xuất hàng", command=export_goods_screen)
    btn_export_goods.pack(pady=5)

    btn_logout = tk.Button(window, text="Đăng xuất", command=login_screen)
    btn_logout.pack(pady=10)

# Hàm để quản lý tài khoản khách hàng (chức năng chưa triển khai)
def add_customer_account():
    messagebox.showinfo("Thông báo", "Chức năng quản lý tài khoản khách hàng chưa được triển khai.")

# Nhập hàng
def save_inventory_to_csv(product_name, quantity, price):
    try:
        with open('inventory.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([product_name, quantity, price])
        messagebox.showinfo("Thành công", "Thông tin hàng nhập đã được lưu!")
    except Exception as e:
        print(f"Lỗi khi lưu thông tin hàng nhập: {e}")
        messagebox.showerror("Lỗi", "Không thể lưu thông tin hàng nhập.")

def import_goods():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if product_name and quantity.isdigit() and price.isdigit():
        save_inventory_to_csv(product_name, int(quantity), int(price))
        entry_product_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ và chính xác thông tin!")

def goods_import_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Nhập hàng mới", font=("Arial", 16))
    lbl_title.pack(pady=10)
    
    lbl_product_name = tk.Label(window, text="Tên sản phẩm:")
    lbl_product_name.pack()
    global entry_product_name
    entry_product_name = tk.Entry(window, width=30)
    entry_product_name.pack(pady=5)
    
    lbl_quantity = tk.Label(window, text="Số lượng:")
    lbl_quantity.pack()
    global entry_quantity
    entry_quantity = tk.Entry(window, width=30)
    entry_quantity.pack(pady=5)
    
    lbl_price = tk.Label(window, text="Giá (VNĐ):")
    lbl_price.pack()
    global entry_price
    entry_price = tk.Entry(window, width=30)
    entry_price.pack(pady=5)
    
    btn_import = tk.Button(window, text="Nhập hàng", command=import_goods)
    btn_import.pack(pady=10)

    btn_back = tk.Button(window, text="Quay lại", command=salesperson_dashboard)
    btn_back.pack(pady=5)

# Xuất hàng
def export_product():
    product_code = entry_product_code.get()
    quantity = entry_quantity.get()
    
    if not product_code or not quantity:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return
    
    try:
        with open('exported_products.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_code, quantity])
        messagebox.showinfo("Thành công", f"Đã xuất {quantity} sản phẩm với mã {product_code}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể ghi dữ liệu vào file CSV: {e}")

def export_goods_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Xuất hàng", font=("Arial", 16))
    lbl_title.pack(pady=10)

    lbl_product_code = tk.Label(window, text="Mã sản phẩm:")
    lbl_product_code.pack()
    global entry_product_code
    entry_product_code = tk.Entry(window)
    entry_product_code.pack(pady=5)

    lbl_quantity = tk.Label(window, text="Số lượng:")
    lbl_quantity.pack()
    global entry_quantity
    entry_quantity = tk.Entry(window)
    entry_quantity.pack(pady=5)

    btn_export_product = tk.Button(window, text="Xuất hàng", command=export_product)
    btn_export_product.pack(pady=10)

    btn_back = tk.Button(window, text="Quay lại", command=salesperson_dashboard)
    btn_back.pack(pady=5)

# Chuyển sang màn hình đăng ký
def register_screen():
    clear_screen()
    
    lbl_register = tk.Label(window, text="Đăng ký tài khoản", font=("Arial", 16))
    lbl_register.pack(pady=10)
    
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username, entry_password, entry_confirm_password, role_var
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)
    
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)

    lbl_confirm_password = tk.Label(window, text="Xác nhận mật khẩu:")
    lbl_confirm_password.pack()
    entry_confirm_password = tk.Entry(window, width=30, show='*')
    entry_confirm_password.pack(pady=5)

    lbl_role = tk.Label(window, text="Vai trò:")
    lbl_role.pack()
    role_var = tk.StringVar(value="Khách hàng")  # Vai trò mặc định là "Khách hàng"
    rb_customer = tk.Radiobutton(window, text="Khách hàng", variable=role_var, value="Khách hàng")
    rb_customer.pack()
    rb_salesperson = tk.Radiobutton(window, text="Nhân viên bán hàng", variable=role_var, value="Nhân viên bán hàng")
    rb_salesperson.pack()

    btn_register = tk.Button(window, text="Đăng ký", command=register)
    btn_register.pack(pady=10)

    btn_back = tk.Button(window, text="Quay lại", command=login_screen)
    btn_back.pack(pady=5)

# Màn hình đăng nhập
def login_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Đăng nhập", font=("Arial", 16))
    lbl_title.pack(pady=10)

    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)

    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    global entry_password
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)

    btn_login = tk.Button(window, text="Đăng nhập", command=login)
    btn_login.pack(pady=10)

    btn_register = tk.Button(window, text="Đăng ký", command=register_screen)
    btn_register.pack(pady=5)

# Hàm lưu thông tin hàng nhập vào file CSV
def save_inventory_to_csv(product_name, quantity, price):
    try:
        with open('inventory.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([product_name, quantity, price])
        messagebox.showinfo("Thành công", "Thông tin hàng nhập đã được lưu!")
    except Exception as e:
        print(f"Lỗi khi lưu thông tin hàng nhập: {e}")
        messagebox.showerror("Lỗi", "Không thể lưu thông tin hàng nhập.")

# Hàm xử lý nhập hàng
def import_goods():
    product_name = entry_product_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if product_name and quantity.isdigit() and price.isdigit():
        save_inventory_to_csv(product_name, int(quantity), int(price))
        # Xóa các ô nhập sau khi lưu thành công
        entry_product_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ và chính xác thông tin!")

# Giao diện nhập hàng
def goods_import_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Nhập hàng mới", font=("Arial", 16))
    lbl_title.pack(pady=10)
    
    # Nhãn và ô nhập cho tên sản phẩm
    lbl_product_name = tk.Label(window, text="Tên sản phẩm:")
    lbl_product_name.pack()
    global entry_product_name
    entry_product_name = tk.Entry(window, width=30)
    entry_product_name.pack(pady=5)
    
    # Nhãn và ô nhập cho số lượng
    lbl_quantity = tk.Label(window, text="Số lượng:")
    lbl_quantity.pack()
    global entry_quantity
    entry_quantity = tk.Entry(window, width=30)
    entry_quantity.pack(pady=5)
    
    # Nhãn và ô nhập cho giá
    lbl_price = tk.Label(window, text="Giá (VNĐ):")
    lbl_price.pack()
    global entry_price
    entry_price = tk.Entry(window, width=30)
    entry_price.pack(pady=5)
    
    # Nút xác nhận nhập hàng
    btn_import = tk.Button(window, text="Nhập hàng", width=20, command=import_goods)
    btn_import.pack(pady=10)

    # Nút quay lại
    btn_back = tk.Button(window, text="Quay lại", width=20, command=salesperson_dashboard)
    btn_back.pack(pady=5)

# Hàm xóa các widget hiện tại trên màn hình
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

def add_customer_account():
    clear_screen()

    # Tiêu đề
    lbl_title = tk.Label(window, text="Thêm tài khoản Khách hàng", font=("Arial", 16))
    lbl_title.pack(pady=10)

    # Nhãn và ô nhập cho tài khoản
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)

    # Nhãn và ô nhập cho mật khẩu
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)

    # Nhãn và ô nhập cho xác nhận mật khẩu
    lbl_confirm_password = tk.Label(window, text="Xác nhận mật khẩu:")
    lbl_confirm_password.pack()
    entry_confirm_password = tk.Entry(window, width=30, show='*')
    entry_confirm_password.pack(pady=5)

    # Nút để thêm tài khoản khách hàng
    btn_add_customer = tk.Button(window, text="Thêm Tài khoản", command=lambda: save_customer_account(entry_username, entry_password, entry_confirm_password))
    btn_add_customer.pack(pady=10)

    # Nút quay lại
    btn_back = tk.Button(window, text="Quay lại", command=salesperson_dashboard)
    btn_back.pack(pady=5)

def save_customer_account(entry_username, entry_password, entry_confirm_password):
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    # Kiểm tra xem các ô nhập có rỗng hay không
    if username and password and confirm_password:
        if password == confirm_password:
            # Lưu tài khoản với vai trò "Khách hàng"
            save_account_to_csv(username, password, "Khách hàng")
            messagebox.showinfo("Thành công", "Tài khoản Khách hàng đã được thêm thành công!")
        else:
            messagebox.showwarning("Lỗi", "Mật khẩu xác nhận không khớp!")
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

def save_account_to_csv(username, password, role):
    with open('accounts.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, role])

# Chuyển sang màn hình đăng ký
def register_screen():
    clear_screen()
    
    lbl_register = tk.Label(window, text="Đăng ký tài khoản", font=("Arial", 16))
    lbl_register.pack(pady=10)
    
    # Nhãn cho tài khoản
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username, entry_password, entry_confirm_password, role_var
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)
    
    # Nhãn cho mật khẩu
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)
    
    # Nhãn cho xác nhận mật khẩu
    lbl_confirm_password = tk.Label(window, text="Xác nhận mật khẩu:")
    lbl_confirm_password.pack()
    entry_confirm_password = tk.Entry(window, width=30, show='*')
    entry_confirm_password.pack(pady=5)
    
    # Nhãn cho vai trò
    lbl_role = tk.Label(window, text="Chọn vai trò:")
    lbl_role.pack(pady=5)
    role_var = tk.StringVar()
    role_var.set("Khách hàng")  # Giá trị mặc định
    
    # Thay đổi role menu chỉ còn "Nhân viên bán hàng" và "Khách hàng"
    role_menu = tk.OptionMenu(window, role_var, "Khách hàng", "Nhân viên bán hàng")
    role_menu.pack(pady=5)
    
    btn_register = tk.Button(window, text="Đăng ký", command=register)
    btn_register.pack(pady=5)
    
    btn_back = tk.Button(window, text="Quay lại", command=login_screen)
    btn_back.pack(pady=5)

# Chuyển sang màn hình đăng nhập
def login_screen():
    clear_screen()
    
    lbl_title = tk.Label(window, text="Hệ thống thu ngân", font=("Arial", 18), fg="blue")
    lbl_title.pack(pady=10)
    lbl_login = tk.Label(window, text="Đăng nhập", font=("Arial", 16))
    lbl_login.pack(pady=10)
    
    # Nhãn cho tài khoản
    lbl_username = tk.Label(window, text="Tài khoản:")
    lbl_username.pack()
    global entry_username, entry_password
    entry_username = tk.Entry(window, width=30)
    entry_username.pack(pady=5)
    
    # Nhãn cho mật khẩu
    lbl_password = tk.Label(window, text="Mật khẩu:")
    lbl_password.pack()
    entry_password = tk.Entry(window, width=30, show='*')
    entry_password.pack(pady=5)
    
    btn_login = tk.Button(window, text="Đăng nhập", command=login)
    btn_login.pack(pady=5)
    
    btn_register = tk.Button(window, text="Đăng ký", command=register_screen)
    btn_register.pack(pady=5)

# Xóa các widget hiện tại trên màn hình
def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

# Tạo cửa sổ giao diện chính
window = tk.Tk()
window.title("Hệ thống quản lý")
window.geometry("400x400")

# Bắt đầu với màn hình đăng nhập
login_screen()

window.mainloop()
