"use client";

import { useState } from "react";
import "./../app/app.css";
import { Amplify } from "aws-amplify";
import outputs from "@/amplify_outputs.json";
import "@aws-amplify/ui-react/styles.css";
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

Amplify.configure(outputs);

// Initialize the Bedrock client
const bedrockClient = new BedrockRuntimeClient({
  region: "us-east-1", // Update with your region
});

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendPrompt() {
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const input = {
        modelId: "anthropic.claude-3-sonnet-20240229-v1:0", // Nova Lite model ID
        contentType: "application/json",
        accept: "application/json",
        body: JSON.stringify({
          anthropic_version: "bedrock-2023-05-31",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: prompt
            }
          ]
        })
      };

      const command = new InvokeModelCommand(input);
      const data = await bedrockClient.send(command);

      // Parse the response
      const responseBody = JSON.parse(new TextDecoder().decode(data.body));
      setResponse(responseBody.content[0].text);
    } catch (error) {
      console.error("Error calling Bedrock:", error);
      setResponse("Error: Failed to get response from the model.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>Nova Lite AI Chat</h1>
      <div className="chat-interface">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt here..."
          rows={4}
          className="prompt-input"
        />
        <button 
          onClick={sendPrompt}
          disabled={loading}
          className="send-button"
        >
          {loading ? "Sending..." : "Send Prompt"}
        </button>
        {response && (
          <div className="response-container">
            <h2>Response:</h2>
            <div className="response-text">
              {response}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

