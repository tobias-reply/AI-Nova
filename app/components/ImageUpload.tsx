"use client";

import { useState } from 'react';
import { uploadData } from 'aws-amplify/storage';

export default function ImageUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setFile(files[0]);
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
        disabled={uploading}
      />
      <button 
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? 'Uploading...' : 'Upload Image'}
      </button>
      {uploadResult && (
        <p className={uploadResult.includes('Error') ? 'error' : 'success'}>
          {uploadResult}
        </p>
      )}
    </div>
  );
}