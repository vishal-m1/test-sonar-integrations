#!/usr/bin/env bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SONAR_SETUP_DIR="$SCRIPT_DIR/local-sonarqube-setup"
SAMPLE_PROJECT_DIR="$SCRIPT_DIR/sample-project"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  SonarQube Local Scan Orchestrator${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Start SonarQube
echo -e "${YELLOW}[1/5] Starting SonarQube...${NC}"
cd "$SONAR_SETUP_DIR"
bash scripts/start_sonar.sh

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start SonarQube${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ SonarQube is running${NC}"
echo ""

# Step 2: Wait for port 9000 to be ready (already done in start_sonar.sh, but double-check)
echo -e "${YELLOW}[2/5] Verifying SonarQube is ready...${NC}"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s -f http://localhost:9000/api/system/status > /dev/null 2>&1; then
        echo -e "${GREEN}✅ SonarQube is ready${NC}"
        break
    fi
    attempt=$((attempt + 1))
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}❌ SonarQube did not become ready in time${NC}"
    exit 1
fi

echo ""

# Step 3: Check if token is configured
echo -e "${YELLOW}[3/5] Checking sample project configuration...${NC}"
cd "$SAMPLE_PROJECT_DIR"

if grep -q "<TOKEN_PLACEHOLDER>" sonar-project.properties; then
    echo -e "${RED}❌ Error: Token not configured in sonar-project.properties${NC}"
    echo ""
    echo "Please:"
    echo "  1. Open SonarQube at http://localhost:9000"
    echo "  2. Login (admin/admin, then change password)"
    echo "  3. Create project 'sample-project'"
    echo "  4. Generate a token"
    echo "  5. Update sample-project/sonar-project.properties with your token"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Configuration looks good${NC}"
echo ""

# Step 4: Run SonarScanner
echo -e "${YELLOW}[4/5] Running SonarScanner on sample project...${NC}"
echo ""

# Check if sonar-scanner is installed
if ! command -v sonar-scanner &> /dev/null; then
    echo -e "${YELLOW}⚠️  sonar-scanner not found in PATH, using Docker instead...${NC}"
    USE_DOCKER=true
else
    USE_DOCKER=false
fi

cd "$SAMPLE_PROJECT_DIR"

if [ "$USE_DOCKER" = true ]; then
    # Use Docker to run SonarScanner
    echo -e "${BLUE}Running SonarScanner via Docker:${NC}"
    echo ""
    echo -e "${BLUE}docker run --rm --network host \\${NC}"
    echo -e "${BLUE}  -v \"$(pwd):/usr/src\" \\${NC}"
    echo -e "${BLUE}  -w /usr/src \\${NC}"
    echo -e "${BLUE}  sonarsource/sonar-scanner-cli:latest \\${NC}"
    echo -e "${BLUE}  sonar-scanner${NC}"
    echo ""
    echo "----------------------------------------"
    
    docker run --rm --network host \
      -v "$(pwd):/usr/src" \
      -w /usr/src \
      sonarsource/sonar-scanner-cli:latest \
      sonar-scanner
    
    SCAN_EXIT_CODE=$?
else
    # Use local sonar-scanner
    echo -e "${BLUE}Running SonarScanner locally:${NC}"
    echo ""
    echo -e "${BLUE}sonar-scanner${NC}"
    echo ""
    echo "----------------------------------------"
    
    sonar-scanner
    
    SCAN_EXIT_CODE=$?
fi

echo ""
echo "----------------------------------------"

if [ $SCAN_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}❌ SonarScanner failed with exit code: $SCAN_EXIT_CODE${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Scan completed successfully${NC}"
echo ""

# Wait a bit for SonarQube to process the results
echo -e "${YELLOW}⏳ Waiting for SonarQube to process results...${NC}"
sleep 10

# Step 5: Generate report
echo -e "${YELLOW}[5/5] Generating report...${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 not found. Skipping report generation.${NC}"
    echo -e "${YELLOW}   Install Python3 and run fetch_report.py manually.${NC}"
else
    # Check if requests module is available
    if python3 -c "import requests" 2>/dev/null; then
        cd "$SONAR_SETUP_DIR/scripts"
        # Use admin credentials for report generation (more reliable than token)
        python3 fetch_report.py \
            --host http://localhost:9000 \
            --user admin \
            --password admin \
            --project sample-project \
            --json-output "$SCRIPT_DIR/report.json" \
            --html-output "$SCRIPT_DIR/report.html"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Report generated successfully${NC}"
            echo ""
            echo -e "${BLUE}📄 Reports saved:${NC}"
            echo -e "   - JSON: $SCRIPT_DIR/report.json"
            echo -e "   - HTML: $SCRIPT_DIR/report.html"
        else
            echo -e "${YELLOW}⚠️  Report generation had issues, but scan completed${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Python 'requests' module not found.${NC}"
        echo -e "${YELLOW}   Install with: pip install requests${NC}"
        echo -e "${YELLOW}   Then run fetch_report.py manually.${NC}"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Local scan completed!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "🌐 View results in SonarQube:"
echo -e "   http://localhost:9000"
echo ""
echo -e "📊 View project dashboard:"
echo -e "   http://localhost:9000/dashboard?id=sample-project"
echo ""

