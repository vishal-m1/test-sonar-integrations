# GitHub Actions Setup Instructions

## 🔐 Required GitHub Secrets

Go to your repository settings: **Settings → Secrets and variables → Actions → New repository secret**

Add these 3 secrets:

### 1. SONAR_TOKEN
- **Value**: Your SonarQube/SonarCloud authentication token
- **How to get**:
  - **SonarCloud**: https://sonarcloud.io → My Account → Security → Generate Token
  - **Self-hosted SonarQube**: http://your-sonarqube:9000 → My Account → Security → Generate Token

### 2. SONAR_HOST_URL
- **Value**: Your SonarQube server URL
- **Examples**:
  - SonarCloud: `https://sonarcloud.io`
  - Self-hosted: `http://your-sonarqube-server:9000` or `https://sonar.yourdomain.com`

### 3. SLACK_WEBHOOK_URL
- **Value**: Your Slack webhook URL (provided separately)
- **Channel**: `#testing-sonarqube`
- **Format**: `https://hooks.slack.com/services/...`

## 📝 Steps to Configure

1. **Go to repository**: https://github.com/vishal-m1/test-sonar-integrations
2. **Click**: Settings → Secrets and variables → Actions
3. **Click**: New repository secret
4. **Add each secret** as listed above

## 🧪 Testing the Workflow

1. **Create a test branch**:
   ```bash
   git checkout -b test-pr
   ```

2. **Add some code with issues** (or use the existing test file):
   ```bash
   # The test_bad_code.py file already has issues
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Test PR for SonarQube"
   git push -u origin test-pr
   ```

4. **Create Pull Request**:
   - Go to: https://github.com/vishal-m1/test-sonar-integrations/pulls
   - Click "New Pull Request"
   - Select `test-pr` → `main`
   - Create PR

5. **Watch the workflow**:
   - Go to Actions tab
   - See the SonarQube check run
   - If quality gate fails, check Slack for notification

## 🔗 Create Test PR

You can create a test PR manually:
- **URL**: https://github.com/vishal-m1/test-sonar-integrations/compare/main...test-pr-branch
- Or use the existing branch: `test-pr-branch`

## ✅ Expected Behavior

- ✅ Workflow runs on every PR
- ✅ SonarQube scans the code
- ✅ Quality gate is checked
- ✅ If failed → Slack notification sent to `#testing-sonarqube`
- ✅ PR shows check status (pass/fail)

## 🐛 Troubleshooting

### Workflow not running?
- Check if secrets are set correctly
- Verify branch name matches workflow trigger (main/master/develop)

### SonarQube scan fails?
- Verify `SONAR_TOKEN` is valid
- Check `SONAR_HOST_URL` is correct
- Ensure project exists in SonarQube/SonarCloud

### Slack notification not sent?
- Verify `SLACK_WEBHOOK_URL` secret is set
- Check webhook URL is correct
- Test webhook manually with curl

