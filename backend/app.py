from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
from rembg import remove
import os
from dotenv import load_dotenv
from sklearn.cluster import KMeans

load_dotenv()

app = Flask(__name__)
CORS(app)



def image_to_base64(image, format='PNG'):
    buffer = io.BytesIO()
    image.save(buffer, format=format, quality=95 if format == 'JPEG' else None)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{img_str}"

def remove_color_background(image, target_color, tolerance=30):
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    target_bgr = np.array([
        int(target_color[5:7], 16),  # B
        int(target_color[3:5], 16),  # G
        int(target_color[1:3], 16)   # R
    ])
    
    lower_bound = np.maximum(target_bgr - tolerance, 0)
    upper_bound = np.minimum(target_bgr + tolerance, 255)
    
    mask = cv2.inRange(cv_image, lower_bound, upper_bound)
    
    rgba_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGBA)
    
    # Apply mask (make matching pixels transparent)
    rgba_image[mask > 0] = [0, 0, 0, 0]
    
    result = Image.fromarray(rgba_image, 'RGBA')
    return result

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Background removal service is running'})

@app.route('/remove-background', methods=['POST'])
def remove_background():
    """Remove background using AI model"""
    try:
        # Check if file is in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Get optional parameters from form data
        output_format = request.form.get('format', 'PNG').upper()
        if output_format not in ['PNG', 'JPEG', 'WEBP']:
            output_format = 'PNG'
        
        # Read and convert the uploaded file to PIL Image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Remove background using rembg
        output_bytes = remove(image_data)
        result_image = Image.open(io.BytesIO(output_bytes))
        
        # Convert to requested format
        if output_format == 'JPEG':
            # For JPEG, we need to handle transparency
            background = Image.new('RGB', result_image.size, (255, 255, 255))
            if result_image.mode == 'RGBA':
                background.paste(result_image, mask=result_image.split()[-1])
                result_image = background
        elif output_format == 'WEBP':
            # Ensure WEBP supports the current mode
            if result_image.mode not in ['RGB', 'RGBA']:
                result_image = result_image.convert('RGBA')
        
        # Convert to base64
        result_base64 = image_to_base64(result_image, output_format)
        
        return jsonify({
            'success': True,
            'result': result_base64,
            'format': output_format,
            'message': 'Background removed successfully using AI'
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/remove-color-background', methods=['POST'])
def remove_color_bg():
    """Remove background based on specific color"""
    try:
        # Check if file is in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Get parameters from form data
        target_color = request.form.get('color')
        if not target_color:
            return jsonify({'error': 'Target color is required'}), 400
            
        tolerance_str = request.form.get('tolerance', '30')
        try:
            tolerance = int(float(tolerance_str)) if tolerance_str else 30
            # Ensure tolerance is within valid range
            tolerance = max(1, min(100, tolerance))
        except (ValueError, TypeError):
            tolerance = 30
            
        output_format = request.form.get('format', 'PNG').upper()
        
        # Debug logging
        print(f"Debug - All form keys: {list(request.form.keys())}")
        print(f"Debug - Color: {target_color}, Tolerance: {tolerance_str} -> {tolerance}, Format: {output_format}")
        print(f"Debug - File info: {file.filename}")
        
        if output_format not in ['PNG', 'JPEG', 'WEBP']:
            output_format = 'PNG'
        
        if not target_color.startswith('#') or len(target_color) != 7:
            return jsonify({'error': 'Invalid color format. Use #RRGGBB'}), 400
        
        image_data = file.read()
        print(f"Debug - Image data size: {len(image_data)} bytes")
        image = Image.open(io.BytesIO(image_data))
        
        result_image = remove_color_background(image, target_color, tolerance)
        
        if output_format == 'JPEG':
            # For JPEG, add white background
            background = Image.new('RGB', result_image.size, (255, 255, 255))
            if result_image.mode == 'RGBA':
                background.paste(result_image, mask=result_image.split()[-1])
                result_image = background
        elif output_format == 'WEBP':
            # Ensure WEBP supports the current mode
            if result_image.mode not in ['RGB', 'RGBA']:
                result_image = result_image.convert('RGBA')
        
        result_base64 = image_to_base64(result_image, output_format)
        
        return jsonify({
            'success': True,
            'result': result_base64,
            'format': output_format,
            'color_removed': target_color,
            'tolerance': tolerance,
            'message': f'Background color {target_color} removed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/get-dominant-colors', methods=['POST'])
def get_dominant_colors():
    """Get dominant colors from image to help user choose background color"""
    try:
        # Check if file is in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read and convert the uploaded file to PIL Image
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image for faster processing
        image.thumbnail((150, 150))
        
        # Convert to numpy array
        img_array = np.array(image)
        pixels = img_array.reshape(-1, 3)
        
        # Use k-means clustering to find dominant colors
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the dominant colors
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert to hex format
        hex_colors = []
        for color in colors:
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            hex_colors.append(hex_color)
        
        return jsonify({
            'success': True,
            'dominant_colors': hex_colors,
            'message': 'Dominant colors extracted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Color extraction failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug) 
