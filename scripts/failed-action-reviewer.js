#!/usr/bin/env node

const { BedrockRuntimeClient, InvokeModelCommand } = require('@aws-sdk/client-bedrock-runtime');
const { Octokit } = require('@octokit/rest');

async function main() {
  try {
    const workflowRunId = process.env.WORKFLOW_RUN_ID;
    const workflowName = process.env.WORKFLOW_NAME;
    const headSha = process.env.HEAD_SHA;
    const pullRequestNumber = process.env.PULL_REQUEST_NUMBER;
    const githubToken = process.env.GITHUB_TOKEN;
    
    console.log('Environment check:');
    console.log('- AWS_ACCESS_KEY_ID:', process.env.AWS_ACCESS_KEY_ID ? 'Present' : 'Missing');
    console.log('- AWS_SECRET_ACCESS_KEY:', process.env.AWS_SECRET_ACCESS_KEY ? 'Present' : 'Missing');
    console.log('- AWS_REGION:', process.env.AWS_REGION || 'us-east-1');
    console.log('- Workflow Run ID:', workflowRunId);
    console.log('- Workflow Name:', workflowName);
    console.log('- Pull Request Number:', pullRequestNumber);
    
    if (!process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY) {
      console.error('AWS credentials not found in environment variables');
      process.exit(1);
    }
    
    if (!workflowRunId) {
      console.log('No workflow run ID found, skipping...');
      return;
    }

    // Initialize GitHub client
    const octokit = new Octokit({
      auth: githubToken
    });

    const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

    // Get workflow run details and jobs
    console.log('Fetching workflow run details...');
    const workflowRun = await octokit.rest.actions.getWorkflowRun({
      owner,
      repo,
      run_id: workflowRunId
    });

    const jobs = await octokit.rest.actions.listJobsForWorkflowRun({
      owner,
      repo,
      run_id: workflowRunId
    });

    // Find failed jobs and get their logs
    const failedJobs = jobs.data.jobs.filter(job => job.conclusion === 'failure');
    
    if (failedJobs.length === 0) {
      console.log('No failed jobs found');
      return;
    }

    console.log(`Found ${failedJobs.length} failed job(s)`);

    // Get logs for failed jobs
    let failureDetails = '';
    for (const job of failedJobs) {
      console.log(`Getting logs for job: ${job.name}`);
      try {
        const logs = await octokit.rest.actions.downloadJobLogsForWorkflowRun({
          owner,
          repo,
          job_id: job.id
        });
        
        failureDetails += `\n## Job: ${job.name}\n`;
        failureDetails += `Status: ${job.conclusion}\n`;
        failureDetails += `Started: ${job.started_at}\n`;
        failureDetails += `Completed: ${job.completed_at}\n`;
        
        // Extract key failure information from logs
        if (logs.data) {
          const logText = logs.data.toString();
          const errorLines = logText.split('\n').filter(line => 
            line.includes('Error') || 
            line.includes('FAILED') || 
            line.includes('error:') ||
            line.includes('ERROR') ||
            line.includes('FAILURE')
          ).slice(-10); // Last 10 error lines
          
          if (errorLines.length > 0) {
            failureDetails += `\nKey error messages:\n${errorLines.join('\n')}\n`;
          }
        }
      } catch (logError) {
        console.log(`Could not fetch logs for job ${job.name}:`, logError.message);
        failureDetails += `\n## Job: ${job.name}\n`;
        failureDetails += `Status: ${job.conclusion}\n`;
        failureDetails += `Error: Could not fetch detailed logs\n`;
      }
    }

    // Initialize Bedrock client
    const credentials = {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    };
    
    if (process.env.AWS_SESSION_TOKEN) {
      credentials.sessionToken = process.env.AWS_SESSION_TOKEN;
    }

    const bedrockClient = new BedrockRuntimeClient({
      region: process.env.AWS_REGION || 'us-east-1',
      credentials
    });
    
    console.log('Analyzing failure with Claude via Bedrock...');

    // Prepare the analysis prompt
    const analysisPrompt = `You are a senior software engineer helping debug failed GitHub Actions. Analyze the following workflow failure and provide helpful insights.

**Workflow Information:**
- Name: ${workflowName}
- Run ID: ${workflowRunId}
- Repository: ${owner}/${repo}

**Failure Details:**
${failureDetails}

**Instructions:**
1. Identify the root cause of the failure
2. Provide specific, actionable steps to fix the issue
3. Suggest preventive measures if applicable
4. Keep your response concise but helpful
5. Format your response in markdown for GitHub comments

Please provide your analysis:`;

    // Call Bedrock
    const command = new InvokeModelCommand({
      modelId: 'anthropic.claude-3-sonnet-20240229-v1:0',
      body: JSON.stringify({
        anthropic_version: 'bedrock-2023-05-31',
        max_tokens: 2000,
        messages: [{
          role: 'user',
          content: analysisPrompt
        }]
      }),
      contentType: 'application/json',
      accept: 'application/json'
    });

    const response = await bedrockClient.send(command);
    console.log('Bedrock analysis successful');
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));
    const analysis = responseBody.content[0].text.trim();

    console.log('Creating comment with analysis...');

    // Create comment on PR or commit
    const commentBody = `## 🤖 Automated Failure Analysis

${analysis}

---
*This analysis was generated automatically by Claude via AWS Bedrock when the "${workflowName}" workflow failed.*`;

    if (pullRequestNumber && pullRequestNumber !== 'null') {
      // Comment on PR
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: parseInt(pullRequestNumber),
        body: commentBody
      });
      console.log(`Created analysis comment on PR #${pullRequestNumber}`);
    } else {
      // Comment on commit
      await octokit.rest.repos.createCommitComment({
        owner,
        repo,
        commit_sha: headSha,
        body: commentBody
      });
      console.log(`Created analysis comment on commit ${headSha}`);
    }

  } catch (error) {
    console.error('Error analyzing failed workflow:', error);
    process.exit(1);
  }
}

main();