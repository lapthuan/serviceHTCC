import firebase_admin
from firebase_admin import credentials, db
import time

# Sử dụng thông tin cấu hình để kết nối Firebase
cred = credentials.Certificate("D:/ServiceHTCC/taonghile-firebase-adminsdk-nyc00-359859f282.json")
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
        RCM_ref = db.reference('CONTROL/RCM')

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

                # Thực hiện logic
                if paO > O_Pa:
                    RCM_ref.set(1)
                    print("Set 1")
                else:
                    RCM_ref.set(2)
                    print("Set 2")
            except ValueError as e:
                print(f"Error converting values to float: {e}")

        # Đợi 5 giây trước khi tiếp tục
        time.sleep(5)

if __name__ == "__main__":
    print("Start")
    read_and_update_data()
