# Setup Instructions

## Adding the GitHub Actions Workflow

Due to GitHub security restrictions, the workflow file needs to be added manually. Follow these steps:

### Option 1: Add via GitHub Web Interface

1. Go to your repository: https://github.com/ProjectProblem/secure-cicd-pipeline
2. Click on "Add file" → "Create new file"
3. Name the file: `.github/workflows/security-pipeline.yml`
4. Copy the contents from the local file at `.github/workflows/security-pipeline.yml`
5. Commit the file directly to the main branch

### Option 2: Add via Git Command Line

If you have the repository cloned locally with your personal credentials:

```bash
# Clone the repository
git clone https://github.com/ProjectProblem/secure-cicd-pipeline.git
cd secure-cicd-pipeline

# Create the workflow directory
mkdir -p .github/workflows
mkdir -p .github/codeql

# Copy the workflow files (from this project directory)
# Then add and commit
git add .github
git commit -m "Add GitHub Actions security pipeline"
git push
```

### Option 3: Use the Provided Files

The workflow files are available in this project directory:
- `.github/workflows/security-pipeline.yml`
- `.github/codeql/codeql-config.yml`

You can copy these files to your local clone of the repository and push them.

## Verifying the Pipeline

Once the workflow file is added:

1. Go to the "Actions" tab in your GitHub repository
2. You should see the "Secure CI/CD Pipeline" workflow
3. The workflow will automatically run on push to main branch
4. You can also manually trigger it from the Actions tab

## Enabling CodeQL

To enable CodeQL scanning:

1. Go to your repository settings
2. Navigate to "Security" → "Code security and analysis"
3. Enable "CodeQL analysis" if not already enabled

## Next Steps

After the workflow is set up:

1. Make a small change to the code
2. Commit and push to trigger the pipeline
3. Watch the security scans run in the Actions tab
4. Review any findings in the Security tab

## Troubleshooting

If the workflow doesn't run:
- Check that the file is in the correct location: `.github/workflows/security-pipeline.yml`
- Verify that GitHub Actions are enabled for your repository
- Check the Actions tab for any error messages
