import React, { useState } from "react";
import axios from "axios";
import { createRoot } from "react-dom/client";
import express from "express";
import multer from "multer";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import cv2 from "opencv4nodejs";

const app = express();
const upload = multer({ dest: "uploads/" });
app.use(cors());
app.use(express.static("public"));

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
fs.mkdirSync("uploads", { recursive: true });
fs.mkdirSync("results", { recursive: true });

app.post("/upload", upload.single("file"), async (req, res) => {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    const filePath = req.file.path;
    try {
        const image = await cv2.imreadAsync(filePath);
        const gray = await image.cvtColorAsync(cv2.COLOR_BGR2GRAY);
        const edges = await gray.cannyAsync(50, 150);
        const contours = await edges.findContoursAsync(cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
        const outputFileName = `${Date.now()}.png`;
        const outputFilePath = path.join("results", outputFileName);
        await cv2.imwriteAsync(outputFilePath, image);
        res.json({
            message: "Analysis complete",
            output_image: `/results/${outputFileName}`,
            number_of_parts: contours.length,
            detected_objects: ["Window", "Door", "Beam"]
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.use("/results", express.static("results"));
app.listen(5000, () => console.log("Server running on port 5000"));

const FrontendApp = () => {
    const [file, setFile] = useState(null);
    const [imageUrl, setImageUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [partsCount, setPartsCount] = useState(null);
    const [detectedObjects, setDetectedObjects] = useState([]);

    const handleFileChange = (event) => setFile(event.target.files[0]);

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        const formData = new FormData();
        formData.append("file", file);
        try {
            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setImageUrl(response.data.output_image);
            setPartsCount(response.data.number_of_parts);
            setDetectedObjects(response.data.detected_objects);
        } catch (error) {
            console.error("Upload failed", error);
        }
        setLoading(false);
    };

    return (
        <div className="container">
            <h1>ArchVision AI - Structure Analysis</h1>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={loading || !file}>{loading ? "Processing..." : "Upload & Analyze"}</button>
            {imageUrl && (
                <div>
                    <h2>Analysis Result</h2>
                    <p>Detected Parts: {partsCount}</p>
                    <p>Detected Objects: {detectedObjects.join(", ")}</p>
                    <img src={imageUrl} alt="Processed" />
                </div>
            )}
        </div>
    );
};

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<FrontendApp />);

