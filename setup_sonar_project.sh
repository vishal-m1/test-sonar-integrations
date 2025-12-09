#!/bin/bash

# Helper script to create SonarQube project and token via API

SONAR_HOST="http://localhost:9000"
ADMIN_USER="admin"
ADMIN_PASS="admin"
PROJECT_KEY="sample-project"
PROJECT_NAME="sample-project"
TOKEN_NAME="local-scan-token"

echo "🔧 Setting up SonarQube project and token..."

# Try to create project (may fail if it exists, that's ok)
echo "📦 Creating project..."
PROJECT_RESPONSE=$(curl -s -w "\n%{http_code}" -u "${ADMIN_USER}:${ADMIN_PASS}" \
  -X POST "${SONAR_HOST}/api/projects/create" \
  -d "project=${PROJECT_KEY}&name=${PROJECT_NAME}" 2>&1)

HTTP_CODE=$(echo "$PROJECT_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Project created successfully"
elif echo "$PROJECT_RESPONSE" | grep -q "already exists"; then
    echo "ℹ️  Project already exists (this is fine)"
else
    echo "⚠️  Project creation response: $HTTP_CODE"
    echo "$PROJECT_RESPONSE" | head -n -1
fi

# Generate token
echo "🔑 Generating token..."
TOKEN_RESPONSE=$(curl -s -w "\n%{http_code}" -u "${ADMIN_USER}:${ADMIN_PASS}" \
  -X POST "${SONAR_HOST}/api/user_tokens/generate" \
  -d "name=${TOKEN_NAME}" 2>&1)

HTTP_CODE=$(echo "$TOKEN_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    TOKEN=$(echo "$TOKEN_RESPONSE" | head -n -1 | grep -o '"token":"[^"]*' | cut -d'"' -f4)
    if [ -n "$TOKEN" ]; then
        echo "✅ Token generated: ${TOKEN:0:20}..."
        
        # Update sonar-project.properties
        PROP_FILE="../sample-project/sonar-project.properties"
        if [ -f "$PROP_FILE" ]; then
            sed -i "s/sonar.login=<TOKEN_PLACEHOLDER>/sonar.login=${TOKEN}/" "$PROP_FILE"
            echo "✅ Updated sonar-project.properties with token"
            echo "$TOKEN"
            exit 0
        else
            echo "⚠️  Could not find $PROP_FILE"
            echo "Token: $TOKEN"
            exit 1
        fi
    else
        echo "❌ Could not extract token from response"
        echo "$TOKEN_RESPONSE" | head -n -1
        exit 1
    fi
else
    # Token might already exist, try to revoke and recreate
    echo "⚠️  Token generation failed (HTTP $HTTP_CODE), trying to revoke existing token..."
    curl -s -u "${ADMIN_USER}:${ADMIN_PASS}" \
      -X POST "${SONAR_HOST}/api/user_tokens/revoke" \
      -d "name=${TOKEN_NAME}" > /dev/null 2>&1
    
    sleep 1
    
    TOKEN_RESPONSE=$(curl -s -w "\n%{http_code}" -u "${ADMIN_USER}:${ADMIN_PASS}" \
      -X POST "${SONAR_HOST}/api/user_tokens/generate" \
      -d "name=${TOKEN_NAME}" 2>&1)
    
    HTTP_CODE=$(echo "$TOKEN_RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "200" ]; then
        TOKEN=$(echo "$TOKEN_RESPONSE" | head -n -1 | grep -o '"token":"[^"]*' | cut -d'"' -f4)
        if [ -n "$TOKEN" ]; then
            PROP_FILE="../sample-project/sonar-project.properties"
            if [ -f "$PROP_FILE" ]; then
                sed -i "s/sonar.login=<TOKEN_PLACEHOLDER>/sonar.login=${TOKEN}/" "$PROP_FILE"
                echo "✅ Token generated and updated: ${TOKEN:0:20}..."
                echo "$TOKEN"
                exit 0
            fi
        fi
    fi
    
    echo "❌ Failed to generate token. Response:"
    echo "$TOKEN_RESPONSE" | head -n -1
    echo ""
    echo "💡 You may need to:"
    echo "   1. Login to http://localhost:9000 (admin/admin)"
    echo "   2. Change password if prompted"
    echo "   3. Create project manually"
    echo "   4. Generate token manually"
    exit 1
fi

