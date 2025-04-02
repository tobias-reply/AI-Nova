import { NextResponse } from 'next/server';
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({});
const bedrock = new BedrockRuntimeClient({
  region: "us-east-1", // Nova model is available in us-east-1
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

    // Validate bucket name
    const bucketName = process.env.S3_BUCKET_NAME;
    if (!bucketName) {
      throw new Error('S3_BUCKET_NAME environment variable is not set');
    }

    // Get the image from S3
    const getObjectCommand = new GetObjectCommand({
      Bucket: bucketName,
      Key: imageKey,
    });

    try {
      const signedUrl = await getSignedUrl(s3, getObjectCommand, { expiresIn: 3600 });
      
      // Download the image
      const imageResponse = await fetch(signedUrl);
      if (!imageResponse.ok) {
        throw new Error(`Failed to download image: ${imageResponse.statusText}`);
      }
      
      const imageBuffer = await imageResponse.arrayBuffer();
      const base64Image = Buffer.from(imageBuffer).toString('base64');

      // Prepare the prompt for Nova
      const prompt = {
        anthropic_version: "bedrock-2023-05-31",
        max_tokens: 300,
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: "Please describe what you see in this image in detail."
              },
              {
                type: "image",
                source: {
                  type: "base64",
                  media_type: "image/jpeg",
                  data: base64Image
                }
              }
            ]
          }
        ]
      };

      // Call Nova model through Bedrock
      const command = new InvokeModelCommand({
        modelId: "anthropic.claude-3-sonnet-20240229-v1:0",
        contentType: "application/json",
        accept: "application/json",
        body: JSON.stringify(prompt)
      });

      const response = await bedrock.send(command);
      const responseBody = JSON.parse(new TextDecoder().decode(response.body));
      const description = responseBody.content[0].text;

      return NextResponse.json({ description });
    } catch (error: any) {
      if (error.name === 'NoSuchKey') {
        return NextResponse.json(
          { error: 'Image not found in S3 bucket' },
          { status: 404 }
        );
      }
      throw error;
    }
  } catch (error: any) {
    console.error('Error analyzing image:', error);
    return NextResponse.json(
      { 
        error: 'Failed to analyze image',
        details: error.message 
      },
      { status: 500 }
    );
  }
}


