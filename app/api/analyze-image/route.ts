import { NextResponse } from 'next/server';
import { RekognitionClient, DetectLabelsCommand } from "@aws-sdk/client-rekognition";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const rekognition = new RekognitionClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || '',
  },
});

const s3 = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || '',
  },
});

export async function POST(request: Request) {
  try {
    const { imageKey } = await request.json();

    if (!imageKey) {
      return NextResponse.json(
        { error: 'Image key is required' },
        { status: 400 }
      );
    }

    // Get the image from S3
    const getObjectCommand = new GetObjectCommand({
      Bucket: process.env.S3_BUCKET_NAME,
      Key: imageKey,
    });

    const signedUrl = await getSignedUrl(s3, getObjectCommand, { expiresIn: 3600 });
    
    // Download the image
    const imageResponse = await fetch(signedUrl);
    const imageBuffer = await imageResponse.arrayBuffer();

    // Analyze the image with Rekognition
    const command = new DetectLabelsCommand({
      Image: {
        Bytes: Buffer.from(imageBuffer),
      },
      MaxLabels: 10,
      MinConfidence: 70,
    });

    const response = await rekognition.send(command);

    // Format the description
    const labels = response.Labels || [];
    const description = labels.length > 0
      ? `This image contains: ${labels.map(label => label.Name).join(', ')}`
      : 'No objects were detected in this image.';

    return NextResponse.json({ description });
  } catch (error) {
    console.error('Error analyzing image:', error);
    return NextResponse.json(
      { error: 'Failed to analyze image' },
      { status: 500 }
    );
  }
}