#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { BedrockRuntimeClient, InvokeModelCommand } = require('@aws-sdk/client-bedrock-runtime');

async function main() {
  try {
    const issueNumber = process.env.ISSUE_NUMBER;
    const issueBody = process.env.ISSUE_BODY;
    const githubToken = process.env.GITHUB_TOKEN;
    
    if (!issueBody) {
      console.log('No issue body found, skipping...');
      return;
    }

    // Check if issue contains "WIP" string
    if (!issueBody.includes('WIP')) {
      console.log('Issue does not contain "WIP", skipping revision...');
      return;
    }

    console.log('Processing WIP issue...');

    // Read system prompt and project context
    const systemPrompt = fs.readFileSync(path.join(__dirname, 'system-prompt.txt'), 'utf-8');
    const projectContext = fs.readFileSync(path.join(__dirname, 'project-context.txt'), 'utf-8');

    // Initialize Bedrock client
    const bedrockClient = new BedrockRuntimeClient({
      region: process.env.AWS_REGION || 'us-east-1'
    });

    // Prepare the prompt
    const fullPrompt = `${systemPrompt}

Project Context:
${projectContext}

Issue Description to Revise:
${issueBody}

Please provide only the revised issue description:`;

    // Call Bedrock
    const command = new InvokeModelCommand({
      modelId: 'anthropic.claude-3-sonnet-20240229-v1:0',
      body: JSON.stringify({
        anthropic_version: 'bedrock-2023-05-31',
        max_tokens: 4000,
        messages: [
          {
            role: 'user',
            content: fullPrompt
          }
        ]
      }),
      contentType: 'application/json',
      accept: 'application/json'
    });

    const response = await bedrockClient.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));
    const revisedDescription = responseBody.content[0].text.trim();

    console.log('Got revised description from LLM');

    // Update the issue via GitHub API
    const { Octokit } = require('@octokit/rest');
    const octokit = new Octokit({
      auth: githubToken
    });

    const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

    await octokit.rest.issues.update({
      owner,
      repo,
      issue_number: parseInt(issueNumber),
      body: revisedDescription
    });

    console.log(`Successfully updated issue #${issueNumber} with revised description`);

  } catch (error) {
    console.error('Error processing issue:', error);
    process.exit(1);
  }
}

main();