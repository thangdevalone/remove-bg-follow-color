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
- **Axios**: HTTP client
- **PostCSS**: CSS processing with modern features

### DevOps

- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **AWS EC2**: Production deployment
- **Nginx**: Web server

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

## 🌐 Production Deployment

### AWS EC2 Setup

1. **Launch EC2 Instance**

   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t3.medium (minimum)
   - Security Group: Allow ports 22, 80, 443, 5000

2. **Setup Server**

```bash
# SSH to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Run setup script
curl -o setup.sh https://raw.githubusercontent.com/YOUR_USERNAME/remove-bg-follow-color/main/backend/setup.sh
chmod +x setup.sh
./setup.sh
```

3. **Configure GitHub Secrets**

   - `EC2_HOST`: Your EC2 public IP
   - `EC2_USERNAME`: Your EC2 username (usually `ubuntu`)
   - `EC2_SSH_KEY`: Your private SSH key content

4. **Deploy**

```bash
# Push to main branch to trigger deployment
git push origin main
```

### Manual Deployment

```bash
# On EC2 instance
cd /home/ubuntu/remove-bg-app
git clone https://github.com/YOUR_USERNAME/remove-bg-follow-color.git .

# Deploy backend
cd backend
docker build -t remove-bg-backend .
docker run -d --name remove-bg-backend-container -p 5000:5000 --restart unless-stopped remove-bg-backend
```

## 📝 API Documentation

### Endpoints

#### 1. Health Check

```http
GET /health
```

#### 2. AI Background Removal

```http
POST /remove-background
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "format": "PNG"
}
```

#### 3. Color-based Background Removal

```http
POST /remove-color-background
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "color": "#000000",
  "tolerance": 30,
  "format": "PNG"
}
```

#### 4. Get Dominant Colors

```http
POST /get-dominant-colors
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

### Response Format

```json
{
  "success": true,
  "result": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "format": "PNG",
  "message": "Background removed successfully"
}
```

## 🎨 Frontend Usage

1. **Upload Image**: Click upload area or drag & drop image
2. **Choose Method**: AI Removal or Color Removal
3. **Configure Options**:
   - For Color Removal: Select color and tolerance
   - Choose output format (PNG/JPEG/WEBP)
4. **Process**: Click "Remove Background"
5. **Download**: Download processed image

## 🔧 Configuration

### Environment Variables

**Backend** (`.env`):

```env
FLASK_DEBUG=False
PORT=5000
FLASK_ENV=production
```

**Frontend** (Vue.js):

```javascript
// In src/views/Home.vue
apiUrl: process.env.VUE_APP_API_URL || "http://localhost:5000";
```

### Production Settings

Set `VUE_APP_API_URL` to your production backend URL:

```bash
export VUE_APP_API_URL=http://your-ec2-ip:5000
```

## 🛡️ Security Considerations

- Enable HTTPS in production
- Configure CORS properly
- Use environment variables for sensitive data
- Regular security updates
- Monitor resource usage

## 📊 Performance

- **AI Removal**: ~2-5 seconds per image
- **Color Removal**: ~0.5-1 second per image
- **Supported formats**: JPEG, PNG, WEBP
- **Max image size**: Limited by server memory

## 🐛 Troubleshooting

### Common Issues

1. **Docker build fails**: Ensure sufficient disk space
2. **AI model loading**: First request may take longer
3. **CORS errors**: Check API URL configuration
4. **Memory issues**: Use t3.medium or larger EC2 instance

### Logs

```bash
# Backend logs
docker logs remove-bg-backend-container

# System logs
sudo journalctl -u docker
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

Created with ❤️ for efficient background removal

---

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username before deployment.
