# SonarQube Local Setup & CI/CD Integration  

Complete SonarQube setup for local development and GitHub Actions integration.

## 📋 Overview

This repository contains:
- **Local SonarQube setup** with Docker Compose
- **Sample project** with intentionally bad code for testing
- **Automated scanning scripts** with detailed reporting
- **GitHub Actions workflow** for PR quality gate checks
- **Slack notifications** on quality gate failures

## 🚀 Quick Start

### Local Setup

1. **Start SonarQube:**
   ```bash
   cd local-sonarqube-setup
   bash scripts/start_sonar.sh
   ```

2. **Run a scan:**
   ```bash
   bash run_local_scan.sh
   ```

3. **View results:**
   - Web UI: http://localhost:9000
   - Reports: `report.json` and `report.html`

## 📁 Repository Structure

```
.
├── local-sonarqube-setup/     # SonarQube Docker setup
│   ├── docker-compose.yml
│   ├── README.md
│   └── scripts/
│       ├── start_sonar.sh
│       ├── stop_sonar.sh
│       └── fetch_report.py
├── sample-project/            # Sample code for scanning
│   ├── src/
│   ├── tests/
│   └── sonar-project.properties
├── .github/
│   └── workflows/
│       └── sonarqube-simple.yml  # GitHub Actions workflow
├── run_local_scan.sh          # One-command local scan
└── README.md
```

## 🔧 GitHub Actions Setup

### Required Secrets

Configure these secrets in your GitHub repository settings:

1. **SONAR_TOKEN**: Your SonarQube authentication token
   - Generate at: SonarQube → My Account → Security → Generate Token

2. **SONAR_HOST_URL**: Your SonarQube server URL
   - Example: `https://sonarcloud.io` (for SonarCloud)
   - Or: `http://your-sonarqube-server:9000` (for self-hosted)

3. **SLACK_WEBHOOK_URL**: Slack webhook URL for notifications
   - Format: `https://hooks.slack.com/services/...`

### How It Works

1. **On Pull Request**: The workflow automatically triggers
2. **SonarQube Scan**: Analyzes the code changes
3. **Quality Gate Check**: Validates code quality metrics
4. **Slack Notification**: Sends alert if quality gate fails
5. **PR Status**: Updates PR with check status

## 📊 Features

- ✅ Automated code quality checks on PRs
- ✅ Detailed reports with line numbers and code context
- ✅ Slack notifications on failures
- ✅ Local development environment
- ✅ Sample project for testing

## 🔗 Links

- [Local Setup Guide](local-sonarqube-setup/README.md)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📝 License

MIT

