# Background Removal Service

Một ứng dụng web để loại bỏ background từ hình ảnh với 2 phương thức:

1. **AI Removal**: Sử dụng AI để tự động loại bỏ background
2. **Color Removal**: Loại bỏ background dựa trên màu cụ thể

## 🚀 Tính năng

- **Upload ảnh**: Drag & drop hoặc click để chọn ảnh
- **AI Background Removal**: Tự động loại bỏ background bằng AI
- **Color-based Removal**: Chọn màu cụ thể để loại bỏ
- **Color Suggestions**: Gợi ý màu dominant từ ảnh
- **Multiple Output Formats**: PNG, JPEG, WEBP
- **High Quality**: Giữ nguyên chất lượng ảnh đầu vào
- **Download Result**: Tải về ảnh đã xử lý


## 🛠️ Công nghệ sử dụng

### Backend

- **Flask**: Web framework
- **OpenCV**: Image processing
- **rembg**: AI background removal
- **Pillow**: Image manipulation
- **scikit-learn**: Color clustering

### Frontend

- **Vue.js 3**: Frontend framework with Composition API
- **Tailwind CSS v4**: Next-generation utility-first CSS framework
  - CSS-first configuration with `@theme` directive
  - Improved performance and smaller bundle size
  - Native CSS variables support
  - Modern PostCSS integration

### DevOps

- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **AWS EC2**: Production deployment

## 🚀 Quick Start

### Development Setup

1. **Clone repository**

```bash
git clone https://github.com/YOUR_USERNAME/remove-bg-follow-color.git
cd remove-bg-follow-color
```

2. **Backend Setup**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

3. **Frontend Setup**

```bash
cd frontend
npm install
npm run serve
```

4. **Access Application**

- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

### Using Docker

1. **Full stack with Docker Compose (Recommended)**

```bash
docker-compose up --build
```

2. **Individual services**

```bash
# Backend only
cd backend
docker build -t remove-bg-backend .
docker run -p 5000:5000 remove-bg-backend

# Frontend only
cd frontend
docker build -t remove-bg-frontend .
docker run -p 8080:80 remove-bg-frontend
```


## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

Created from ThangDevAlone with ❤️ for efficient background removal

---

