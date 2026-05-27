# Kiến trúc UI

## Tổng quan

Frontend được xây dựng bằng JavaScript thuần (ES6 modules) theo kiến trúc phân lớp, sạch sẽ dựa trên nguyên lý SOLID. Không sử dụng framework hay thư viện — chỉ HTML5, CSS3 và JavaScript native.

## Các lớp kiến trúc

### 1. API Layer (`assets/js/api/`)

Chịu trách nhiệm giao tiếp HTTP với backend.

- `httpClient.js` — HTTP client tổng quát với:
  - Cấu hình Base URL
  - Chặn request/response
  - Phân tích lỗi và xử lý lỗi chuẩn hóa
  - Theo dõi độ trễ
- `predictionApi.js` — Gọi API dự đoán
- `healthApi.js` — Gọi API kiểm tra sức khỏe

### 2. DTO Layer (`assets/js/dto/`)

Data Transfer Objects cho chuyển đổi dữ liệu an toàn kiểu giữa API và ứng dụng.

- `PredictionRequestDto.js` — Chuyển đổi dữ liệu form thành payload request khớp với schema PatientData backend. Xử lý giá trị mặc định cho các trường thuốc tùy chọn.
- `PredictionResponseDto.js` — Bọc response dự đoán với các thuộc tính tính toán (mức độ rủi ro, timestamp đã định dạng).
- `HealthResponseDto.js` — Bọc response kiểm tra sức khỏe với các thuộc tính tính toán (định dạng uptime).

### 3. Model Layer (`assets/js/models/`)

Domain models đại diện cho các thực thể nghiệp vụ cốt lõi.

- `PatientModel.js` — Thực thể bệnh nhân với thuộc tính camelCase và chuyển đổi sang định dạng DTO
- `PredictionModel.js` — Quản lý trạng thái dự đoán (mô hình đã chọn, ngưỡng, trạng thái loading, trạng thái lỗi)

### 4. Service Layer (`assets/js/services/`)

Điều phối logic nghiệp vụ bằng cách phối hợp giữa API, DTO và Model layers.

- `predictionService.js` — Quy trình dự đoán: xây dựng request, gọi API, xử lý response, quản lý trạng thái
- `healthService.js` — Quy trình kiểm tra sức khỏe với xử lý lỗi cho các tình huống ngoại tuyến

### 5. View Layer (`assets/js/views/`)

Bộ điều khiển cấp trang kết hợp các component và xử lý vòng đời trang.

- `dashboardView.js` — Tổng quan hệ thống với thẻ thống kê, thẻ mô hình, hành động nhanh
- `predictionView.js` — Form và kết quả dự đoán; điều phối luồng gửi form
- `healthView.js` — Giám sát sức khỏe chi tiết với khả năng làm mới

### 6. Component Layer (`assets/js/components/`)

Các component UI tái sử dụng, độc lập.

- `navbar.js` — Thanh điều hướng trên cùng với huy hiệu sức khỏe và liên kết tài liệu API
- `sidebar.js` — Thanh điều hướng bên với chuyển đổi responsive
- `predictionForm.js` — Form dữ liệu bệnh nhân đầy đủ với validation và chọn mô hình
- `predictionResult.js` — Hiển thị kết quả dự đoán với huy hiệu rủi ro và thanh tiến trình
- `loading.js` — Lớp phủ loading toàn màn hình
- `toast.js` — Hệ thống thông báo toast

### 7. Utils Layer (`assets/js/utils/`)

Tiện ích và hằng số dùng chung.

- `validators.js` — Quy tắc validation form
- `formatters.js` — Định dạng hiển thị (xác suất, mức rủi ro, tên mô hình)
- `constants.js` — Hằng số ứng dụng (enum, tùy chọn, đường dẫn)
- `helpers.js` — DOM helpers, làm sạch, định dạng

## Định tuyến

Lớp `Router` xử lý điều hướng trang phía client:

- Ánh xạ tên trang đến các lớp View
- Quản lý vòng đời trang (render khi điều hướng)
- Gửi sự kiện `navigate` tùy chỉnh cho giao tiếp giữa các component

## Luồng dữ liệu

```
Tương tác người dùng
      ↓
Component Layer (form, nút bấm)
      ↓
View Layer (điều phối)
      ↓
Service Layer (logic nghiệp vụ)
      ↓
DTO Layer (chuyển đổi dữ liệu)
      ↓
API Layer (giao tiếp HTTP)
      ↓
Backend API (FastAPI)
```

## Xử lý lỗi

- Lỗi API được bắt trong HTTP client và ném ra dưới dạng `HttpClientError`
- Service layer bắt lỗi và cập nhật trạng thái model
- View layer hiển thị lỗi qua thông báo toast và thông báo lỗi nội dòng
- Lỗi mạng (ngoại tuyến, CORS, v.v.) được xử lý một cách thân thiện với người dùng
