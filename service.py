import firebase_admin
from firebase_admin import credentials, db
import threading
import time
from datetime import datetime

# Sử dụng thông tin cấu hình để kết nối Firebase
cred = credentials.Certificate("F:/HTCC/ServiceHTCC/taonghile.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://taonghile-default-rtdb.firebaseio.com"
})

def extract_value(data):
    """
    Hàm để trích xuất giá trị từ dict hoặc trả về chính giá trị đó nếu không phải là dict.
    """
    if isinstance(data, dict):
        # Nếu là dict, lấy giá trị đầu tiên (giả định có một cấp con)
        return list(data.values())[0]
    return data

def read_and_update_data():
    while True:
        # Đọc dữ liệu từ Firebase
        paO_ref = db.reference('SET/Pa0')
        O_Pa_ref = db.reference('MONITOR/O_Pa')
        RCM_ref = db.reference('CONTROL/RCM/data')

        paO = paO_ref.get()
        O_Pa = O_Pa_ref.get()

        # Kiểm tra nếu dữ liệu là None
        if paO is None or O_Pa is None:
            print("One of the values is None, skipping this cycle.")
        else:
            # Chuyển đổi giá trị sang kiểu số nếu cần thiết
            try:
                paO = extract_value(paO)
                O_Pa = extract_value(O_Pa)

                paO = float(paO)
                O_Pa = float(O_Pa)

                # Thực hiện logic
                if paO > O_Pa:
                    RCM_ref.set("1")
                    print("Set 1")
                else:
                    RCM_ref.set("2")
                    print("Set 2")
            except ValueError as e:
                print(f"Error converting values to float: {e}")

        # Đợi 5 giây trước khi tiếp tục
        time.sleep(5)

def log_fire_data():
    while True:
        # Lấy timestamp hiện tại
        timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')
        timestamp2 = datetime.now().isoformat()
        
        # Đọc dữ liệu từ Firebase
        data_ref = db.reference('MONITOR')
        data = data_ref.get()
        
        # Kiểm tra điều kiện và ghi log vào Firebase
        if data and data.get('O_CT', {}).get('data') == "1":
            db.reference(f'LOG/{timestamp}').set({
                'timestamp': timestamp2,
                'fire': "Có cháy"
            })
            print("Có cháy")
        elif data and data.get('O_Baochay', {}).get('data') == "1":
            db.reference(f'LOG/{timestamp}').set({
                'timestamp': timestamp2,
                'fire': "Cảnh báo cháy"
            })
            print("Cảnh báo cháy")
        
        # Đợi 15 phút
        time.sleep(60)

def main():
    # Tạo và bắt đầu các thread cho read_and_update_data và log_fire_data
    thread1 = threading.Thread(target=read_and_update_data)
    thread2 = threading.Thread(target=log_fire_data)
    
    thread1.daemon = True
    thread2.daemon = True
    
    thread1.start()
    thread2.start()

    # Giữ cho chương trình chạy
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    print("start")
    main()
