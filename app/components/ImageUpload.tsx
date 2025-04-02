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
      
      // Generate a unique filename to prevent conflicts
      const fileExtension = file.name.split('.').pop();
      const uniqueFileName = `${Date.now()}-${Math.random().toString(36).substring(2)}.${fileExtension}`;
      
      const result = await uploadData({
        key: uniqueFileName,
        data: file,
        options: {
          contentType: file.type,
          accessLevel: 'public'
        }
      }).result;

      console.log('Upload successful:', result);
      setUploadResult('File uploaded successfully!');
      
      // After successful upload, analyze the image
      await analyzeImage(uniqueFileName);
    } catch (error: any) {
      console.error('Error uploading file:', error);
      setUploading(false);
      
      // Handle specific error types
      if (error.name === 'StorageError') {
        setUploadResult('Storage error: Please check if the file is valid and try again.');
      } else if (error.name === 'NetworkError') {
        setUploadResult('Network error: Please check your internet connection.');
      } else if (error.message?.includes('size')) {
        setUploadResult('File size error: The image might be too large. Please try a smaller file.');
      } else if (error.message?.includes('type')) {
        setUploadResult('Invalid file type: Please upload only image files.');
      } else {
        setUploadResult('Error uploading file. Please try again.');
      }
      return; // Don't proceed to analysis if upload failed
    }

    try {
      // After successful upload, analyze the image
      await analyzeImage(uniqueFileName);
    } catch (error: any) {
      console.error('Error analyzing image:', error);
      setImageDescription('Failed to analyze image. Please try again.');
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





