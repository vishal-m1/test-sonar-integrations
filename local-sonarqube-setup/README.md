

# Local SonarQube Setup Guide

Complete guide to set up and run SonarQube locally for code quality analysis.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Using SonarQube](#using-sonarqube)
- [Sample Project Scanning](#sample-project-scanning)
- [Generating Reports](#generating-reports)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Python 3.7+** (for report scripts)
- **SonarScanner** (CLI tool) - installation instructions below
- **curl** (for health checks)

### Installing SonarScanner

#### macOS
```bash
brew install sonar-scanner
```

#### Linux
```bash
# Download and extract
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
sudo mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner
export PATH=$PATH:/opt/sonar-scanner/bin
```

#### Windows
1. Download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
2. Extract and add to PATH

Verify installation:
```bash
sonar-scanner --version
```

---

## Quick Start

### One-Command Workflow

From the project root directory:

```bash
bash run_local_scan.sh
```

This script will:
1. Start SonarQube
2. Wait for it to be ready
3. Run SonarScanner on the sample project
4. Generate reports
5. Display summary

---

## Detailed Setup

### Step 1: Start SonarQube

```bash
cd local-sonarqube-setup
bash scripts/start_sonar.sh
```

Or manually:
```bash
docker compose up -d
```

Wait 1-2 minutes for SonarQube to initialize (especially on first run).

### Step 2: Access SonarQube

Open your browser and navigate to:
```
http://localhost:9000
```

### Step 3: Login

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin`

⚠️ **Important:** You will be prompted to change the password on first login. Choose a strong password and save it.

### Step 4: Create a Project

1. Click **"Create Project"** → **"Manually"**
2. Fill in:
   - **Project display name:** `sample-project`
   - **Project key:** `sample-project`
3. Click **"Set Up"**
4. Choose **"Locally"** as the analysis method
5. Generate a token:
   - Click **"Generate a token"**
   - Name it: `local-scan-token`
   - Click **"Generate"**
   - **COPY THE TOKEN** (you won't see it again!)

### Step 5: Configure Sample Project

1. Navigate to the `sample-project` directory:
   ```bash
   cd ../sample-project
   ```

2. Edit `sonar-project.properties` and replace `<TOKEN_PLACEHOLDER>` with your token:
   ```properties
   sonar.login=your-actual-token-here
   ```

---

## Using SonarQube

### Starting SonarQube

```bash
cd local-sonarqube-setup
bash scripts/start_sonar.sh
```

### Stopping SonarQube

```bash
cd local-sonarqube-setup
bash scripts/stop_sonar.sh
```

### Viewing Logs

```bash
cd local-sonarqube-setup
docker compose logs -f sonarqube
```

### Resetting SonarQube (Remove All Data)

```bash
cd local-sonarqube-setup
docker compose down -v
```

This will delete all projects, tokens, and data. Use with caution!

### Upgrading SonarQube Version

If you see a warning about SonarQube version being inactive, you can upgrade:

1. **Backup your data** (if needed):
   ```bash
   docker compose exec sonarqube-db pg_dump -U sonar sonar > backup.sql
   ```

2. **Update the version in docker-compose.yml**:
   - Change `image: sonarqube:10.3-community` to the latest version
   - Check available versions: https://hub.docker.com/r/sonarqube/tags

3. **Restart with new version**:
   ```bash
   docker compose down
   docker compose pull
   docker compose up -d
   ```

**Note:** The current setup uses SonarQube 10.3 Community Edition (LTS). For the latest version, check the [SonarQube Docker Hub](https://hub.docker.com/r/sonarqube/tags).

---

## Sample Project Scanning

### Manual Scan

1. Ensure SonarQube is running:
   ```bash
   curl http://localhost:9000/api/system/status
   ```

2. Navigate to sample project:
   ```bash
   cd sample-project
   ```

3. Run SonarScanner:
   ```bash
   sonar-scanner
   ```

4. View results in SonarQube:
   - Open http://localhost:9000
   - Click on `sample-project`

### Automated Scan (via run_local_scan.sh)

The `run_local_scan.sh` script automates the entire process. Make sure you've:
1. Created the project in SonarQube UI
2. Generated a token
3. Updated `sample-project/sonar-project.properties` with your token

Then run:
```bash
bash run_local_scan.sh
```

---

## Generating Reports

### Using fetch_report.py

The `fetch_report.py` script generates comprehensive reports from SonarQube API.

#### Prerequisites

Install required Python packages:
```bash
pip install requests
```

#### Usage

```bash
cd local-sonarqube-setup/scripts
python3 fetch_report.py \
  --host http://localhost:9000 \
  --token YOUR_TOKEN \
  --project sample-project
```

#### Environment Variables (Alternative)

```bash
export SONAR_HOST=http://localhost:9000
export SONAR_TOKEN=your-token-here
export SONAR_PROJECT_KEY=sample-project

python3 fetch_report.py
```

#### Output Files

The script generates:
- **report.json** - Complete data in JSON format
- **report.html** - Visual HTML report with metrics and charts
- **Console output** - Slack and email-formatted summaries

#### Report Contents

- Quality Gate Status (OK/ERROR/WARN)
- Coverage percentage
- Bugs count
- Vulnerabilities count
- Code Smells count
- Duplicated lines percentage
- Issues breakdown by severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)

---

## Troubleshooting

### SonarQube Won't Start

**Check Docker:**
```bash
docker ps
docker compose ps
```

**Check logs:**
```bash
cd local-sonarqube-setup
docker compose logs sonarqube
```

**Common issues:**
- Port 9000 already in use: `lsof -i :9000` and kill the process
- Insufficient memory: SonarQube needs at least 2GB RAM
- Docker not running: Start Docker Desktop

### SonarScanner Fails

**Check SonarQube is accessible:**
```bash
curl http://localhost:9000/api/system/status
```

**Verify token:**
- Token must be valid and not expired
- Check token in SonarQube UI: User → My Account → Security

**Check project key:**
- Must match exactly (case-sensitive)
- Verify in SonarQube UI

### Report Script Fails

**Check Python dependencies:**
```bash
pip install requests
```

**Verify API access:**
```bash
curl -u YOUR_TOKEN: http://localhost:9000/api/system/status
```

**Check project exists:**
- Project must be created in SonarQube UI first
- At least one scan must have completed

### Port Already in Use

If port 9000 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "9001:9000"  # Change 9001 to any available port
```

Then update all references to `localhost:9000` to `localhost:9001`.

---

## Architecture

```
local-sonarqube-setup/
├── docker-compose.yml          # SonarQube + PostgreSQL setup
├── README.md                   # This file
└── scripts/
    ├── start_sonar.sh          # Start SonarQube
    ├── stop_sonar.sh           # Stop SonarQube
    └── fetch_report.py         # Generate reports from API

sample-project/
├── sonar-project.properties    # SonarScanner configuration
├── src/
│   └── main.py                 # Sample code with issues
└── tests/
    └── test_main.py            # Sample tests

run_local_scan.sh               # One-command orchestration
```

---

## Next Steps

After successfully running local scans:

1. **Integrate with CI/CD:** Add SonarScanner to your build pipeline
2. **Set Quality Gates:** Configure quality gate rules in SonarQube
3. **Add More Projects:** Scan additional codebases
4. **Deploy to ECS:** Use this setup as a reference for cloud deployment

---

## Support

For issues or questions:
- SonarQube Documentation: https://docs.sonarqube.org/
- SonarQube Community: https://community.sonarsource.com/

---

**Last Updated:** 2024

