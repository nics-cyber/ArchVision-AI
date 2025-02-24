# ArchVision AI - Structure Analysis

ArchVision AI is a full-stack web application that uses AI and computer vision to analyze images of architectural structures. It detects structural components, extracts features, and provides a visual breakdown of the uploaded image.

## Features

- **Image Upload & Processing**: Users can upload images of buildings or structures for analysis.
- **AI-Based Structure Detection**: Identifies windows, doors, beams, and other architectural elements.
- **Contour & Edge Detection**: Uses OpenCV to highlight key parts of the structure.
- **Bounding Box Visualization**: Shows detected components with bounding boxes.
- **Real-Time Processing**: Fast analysis and response time.
- **Full-Stack Implementation**: Built with React (frontend) and Express with OpenCV (backend).
- **REST API Integration**: Backend processes images and returns structured data.
- **Cross-Origin Support**: Uses CORS to allow frontend-backend communication.

## Installation & Usage

### Prerequisites
- Node.js installed on your system
- npm (Node Package Manager)

### Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-username/ArchVision-AI.git
   cd ArchVision-AI
   ```
2. **Install dependencies**
   ```sh
   npm install
   ```

### Running the Application

1. **Start the server**
   ```sh
   node index.js
   ```
2. **Open the frontend**
   - Go to `http://localhost:5000` in your browser.
   - Upload an image and get an AI-powered breakdown of its structure.

## API Endpoints

### Upload Image
- **Endpoint:** `POST /upload`
- **Description:** Uploads an image and analyzes it.
- **Request:**
  - Form-data with a file field named `file`.
- **Response:**
  ```json
  {
    "message": "Analysis complete",
    "output_image": "/results/{filename}.png",
    "number_of_parts": 5,
    "detected_objects": ["Window", "Door", "Beam"]
  }
  ```

## Technologies Used
- **Frontend:** React
- **Backend:** Node.js, Express
- **AI & Image Processing:** OpenCV (opencv4nodejs)
- **File Handling:** Multer
- **Styling:** Tailwind CSS

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License


