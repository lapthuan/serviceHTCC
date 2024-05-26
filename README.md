# Hệ thống Đọc và Cập Nhật Dữ liệu Firebase

## Giới thiệu

Đây là một hệ thống Python để đọc và cập nhật dữ liệu từ Firebase Realtime Database. Hệ thống sẽ kiểm tra và so sánh các giá trị từ các nút cụ thể trong cơ sở dữ liệu và cập nhật giá trị của một nút khác dựa trên kết quả so sánh đó. Hệ thống này chạy liên tục mỗi 5 giây.

## Cấu hình

### Các bước chuẩn bị

1. **Cài đặt thư viện cần thiết**:
   - Sử dụng `pip` để cài đặt thư viện `firebase-admin`:
     ```bash
     pip install firebase-admin
     ```

2. **Tạo và tải tệp JSON chứa thông tin xác thực**:
   - Truy cập [Firebase Console](https://console.firebase.google.com/).
   - Vào phần "Project settings" -> "Service accounts".
   - Tạo một tài khoản dịch vụ và tải tệp JSON chứa thông tin xác thực về máy tính của bạn.

3. **Cập nhật cấu hình Firebase**:
   - Thay thế đường dẫn tới tệp JSON và URL của cơ sở dữ liệu Firebase trong mã nguồn.

## Mã nguồn

Dưới đây là mã nguồn hoàn chỉnh:

```python
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

                paO = float(paO)
                O_Pa = float(O_Pa)

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
```

## Chạy chương trình

Để chạy chương trình, hãy mở terminal hoặc command prompt và chạy:

```bash
python path/to/your/script.py
```

## Chức năng

- **Kết nối Firebase**: Kết nối đến Firebase Realtime Database sử dụng thông tin xác thực từ tệp JSON.
- **Đọc dữ liệu**: Đọc dữ liệu từ các nút `SET/Pa0` và `MONITOR/O_Pa`.
- **So sánh và cập nhật**: So sánh giá trị của `Pa0` và `O_Pa`, nếu `Pa0` lớn hơn `O_Pa` thì cập nhật `CONTROL/RCM` là 1, ngược lại là 2.
- **Lặp lại mỗi 5 giây**: Hệ thống chạy vòng lặp kiểm tra và cập nhật mỗi 5 giây.

## Lưu ý

- Đảm bảo rằng bạn đã cấu hình quyền truy cập Firebase Realtime Database phù hợp trong Firebase Console.
- Kiểm tra và cập nhật đường dẫn tới tệp JSON và URL của cơ sở dữ liệu cho đúng với cấu hình của bạn.
- Kiểm tra rằng các nút `SET/Pa0`, `MONITOR/O_Pa`, và `CONTROL/RCM` tồn tại trong cơ sở dữ liệu của bạn.

## Troubleshooting

- **Lỗi không tìm thấy tệp JSON**: Đảm bảo rằng đường dẫn tới tệp JSON chính xác.
- **Lỗi kết nối cơ sở dữ liệu**: Kiểm tra URL của cơ sở dữ liệu và đảm bảo rằng cơ sở dữ liệu của bạn đang hoạt động.
- **Lỗi kiểu dữ liệu**: Kiểm tra giá trị của các nút trong cơ sở dữ liệu để đảm bảo rằng chúng có thể được chuyển đổi sang kiểu số.