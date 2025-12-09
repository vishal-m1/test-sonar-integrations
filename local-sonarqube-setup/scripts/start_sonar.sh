#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting SonarQube..."
cd "$COMPOSE_DIR"

docker compose up -d

echo "⏳ Waiting for SonarQube to be ready..."
echo "   This may take 1-2 minutes on first startup..."

# Wait for SonarQube to be healthy
max_attempts=60
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s -f http://localhost:9000/api/system/status > /dev/null 2>&1; then
        echo "✅ SonarQube is ready!"
        echo ""
        echo "🌐 Access SonarQube at: http://localhost:9000"
        echo "👤 Default credentials:"
        echo "   Username: admin"
        echo "   Password: admin"
        echo ""
        echo "⚠️  You will be prompted to change the password on first login."
        exit 0
    fi
    
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts - waiting..."
    sleep 2
done

echo "❌ SonarQube failed to start within expected time"
echo "   Check logs with: docker compose logs sonarqube"
exit 1

