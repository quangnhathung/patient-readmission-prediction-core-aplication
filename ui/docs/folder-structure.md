# Cấu trúc thư mục

```
ui/
├── index.html                        # Điểm vào ứng dụng
├── README.md                         # Tài liệu dự án
│
├── assets/
│   ├── css/
│   │   ├── reset.css                 # Reset / normalize CSS
│   │   ├── variables.css             # CSS custom properties (token thiết kế)
│   │   ├── layout.css                # Bố cục ứng dụng (sidebar, navbar, main)
│   │   ├── components.css            # Style component tái sử dụng
│   │   └── app.css                   # Style trang cụ thể và tiện ích
│   │
│   ├── js/
│   │   ├── app.js                    # Khởi tạo ứng dụng
│   │   ├── config.js                 # Base URL API và cấu hình ứng dụng
│   │   ├── router.js                 # Định tuyến phía client
│   │   │
│   │   ├── api/
│   │   │   ├── httpClient.js         # HTTP client tổng quát
│   │   │   ├── predictionApi.js      # API endpoint dự đoán
│   │   │   └── healthApi.js          # API endpoint kiểm tra sức khỏe
│   │   │
│   │   ├── dto/
│   │   │   ├── PredictionRequestDto.js   # DTO request dự đoán
│   │   │   ├── PredictionResponseDto.js  # DTO response dự đoán
│   │   │   └── HealthResponseDto.js      # DTO response sức khỏe
│   │   │
│   │   ├── models/
│   │   │   ├── PatientModel.js       # Domain model bệnh nhân
│   │   │   └── PredictionModel.js    # Domain model trạng thái dự đoán
│   │   │
│   │   ├── services/
│   │   │   ├── predictionService.js  # Logic nghiệp vụ dự đoán
│   │   │   └── healthService.js      # Logic nghiệp vụ kiểm tra sức khỏe
│   │   │
│   │   ├── views/
│   │   │   ├── dashboardView.js      # Trang tổng quan
│   │   │   ├── predictionView.js     # Trang dự đoán
│   │   │   └── healthView.js         # Trang sức khỏe hệ thống
│   │   │
│   │   ├── components/
│   │   │   ├── navbar.js             # Thanh điều hướng trên cùng
│   │   │   ├── sidebar.js            # Thanh điều hướng bên
│   │   │   ├── predictionForm.js     # Form dữ liệu bệnh nhân
│   │   │   ├── predictionResult.js   # Hiển thị kết quả dự đoán
│   │   │   ├── loading.js            # Lớp phủ loading
│   │   │   └── toast.js              # Thông báo toast
│   │   │
│   │   └── utils/
│   │       ├── validators.js         # Validation form
│   │       ├── formatters.js         # Định dạng hiển thị
│   │       ├── constants.js          # Hằng số và enum ứng dụng
│   │       └── helpers.js            # DOM và tiện ích
│   │
│   └── images/
│
└── docs/
    ├── ui-architecture.md            # Tài liệu kiến trúc
    ├── api-integration.md            # Hướng dẫn tích hợp API
    └── folder-structure.md           # Tham khảo cấu trúc thư mục
```

## Số lượng file

Tổng cộng: 30 files (không bao gồm thư mục images)
