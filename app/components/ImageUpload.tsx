"use client";

import { useState } from 'react';
import { uploadData } from 'aws-amplify/storage';

export default function ImageUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string>('');
  const [imageDescription, setImageDescription] = useState<string>('');
  const [analyzing, setAnalyzing] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setFile(files[0]);
      setImageDescription('');
      setUploadResult('');
    }
  };

  const analyzeImage = async (key: string) => {
    try {
      setAnalyzing(true);
      const response = await fetch('/api/analyze-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageKey: key }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setImageDescription(data.description);
    } catch (error) {
      console.error('Error analyzing image:', error);
      setImageDescription('Failed to analyze image. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    try {
      setUploading(true);
      
      const result = await uploadData({
        key: file.name,
        data: file,
        options: {
          contentType: file.type
        }
      }).result;

      setUploadResult('File uploaded successfully!');
      
      // After successful upload, analyze the image
      await analyzeImage(file.name);
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadResult('Error uploading file. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="image-upload-container">
      <h2>Upload Image</h2>
      <input
        type="file"
        onChange={handleFileChange}
        accept="image/*"
        disabled={uploading || analyzing}
      />
      <button 
        onClick={handleUpload}
        disabled={!file || uploading || analyzing}
      >
        {uploading ? 'Uploading...' : analyzing ? 'Analyzing...' : 'Upload Image'}
      </button>
      {uploadResult && (
        <p className={uploadResult.includes('Error') ? 'error' : 'success'}>
          {uploadResult}
        </p>
      )}
      {imageDescription && (
        <div className="analysis-result">
          <h3>Image Analysis Result:</h3>
          <p>{imageDescription}</p>
        </div>
      )}
    </div>
  );
}

