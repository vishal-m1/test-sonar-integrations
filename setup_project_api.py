#!/usr/bin/env python3
"""Setup SonarQube project and token via API"""

import requests
import sys
import json
import time

SONAR_HOST = "http://localhost:9000"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
PROJECT_KEY = "sample-project"
PROJECT_NAME = "sample-project"
TOKEN_NAME = "local-scan-token"

def wait_for_sonar():
    """Wait for SonarQube to be ready"""
    print("⏳ Waiting for SonarQube to be ready...")
    for i in range(30):
        try:
            resp = requests.get(f"{SONAR_HOST}/api/system/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "UP":
                    print("✅ SonarQube is ready!")
                    return True
        except:
            pass
        time.sleep(2)
    return False

def create_project(session):
    """Create project in SonarQube"""
    print(f"📦 Creating project '{PROJECT_NAME}'...")
    try:
        # Try the web API endpoint
        resp = session.post(
            f"{SONAR_HOST}/api/projects/create",
            data={"project": PROJECT_KEY, "name": PROJECT_NAME}
        )
        if resp.status_code in [200, 201]:
            print("✅ Project created successfully")
            return True
        elif "already exists" in resp.text.lower() or resp.status_code == 400:
            print("ℹ️  Project already exists (this is fine)")
            return True
        else:
            print(f"⚠️  Project creation response: {resp.status_code}")
            print(resp.text[:200])
            return False
    except Exception as e:
        print(f"⚠️  Error creating project: {e}")
        return False

def generate_token(session):
    """Generate authentication token"""
    print(f"🔑 Generating token '{TOKEN_NAME}'...")
    try:
        # First, try to revoke existing token if it exists
        try:
            session.post(
                f"{SONAR_HOST}/api/user_tokens/revoke",
                data={"name": TOKEN_NAME}
            )
        except:
            pass
        
        # Generate new token
        resp = session.post(
            f"{SONAR_HOST}/api/user_tokens/generate",
            data={"name": TOKEN_NAME, "type": "GLOBAL_ANALYSIS_TOKEN"}
        )
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("token")
            if token:
                print(f"✅ Token generated: {token[:20]}...")
                return token
        else:
            print(f"⚠️  Token generation failed: {resp.status_code}")
            print(resp.text[:200])
            return None
    except Exception as e:
        print(f"❌ Error generating token: {e}")
        return None

def update_properties_file(token):
    """Update sonar-project.properties with token"""
    prop_file = "sample-project/sonar-project.properties"
    try:
        with open(prop_file, 'r') as f:
            content = f.read()
        
        content = content.replace("<TOKEN_PLACEHOLDER>", token)
        
        with open(prop_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {prop_file} with token")
        return True
    except Exception as e:
        print(f"❌ Error updating properties file: {e}")
        return False

def main():
    if not wait_for_sonar():
        print("❌ SonarQube did not become ready in time")
        sys.exit(1)
    
    # Create session with authentication
    session = requests.Session()
    session.auth = (ADMIN_USER, ADMIN_PASS)
    
    # Create project
    create_project(session)
    
    # Generate token
    token = generate_token(session)
    if not token:
        print("\n❌ Failed to generate token automatically.")
        print("💡 You may need to:")
        print("   1. Login to http://localhost:9000 (admin/admin)")
        print("   2. Change password if prompted")
        print("   3. Create project manually: " + PROJECT_KEY)
        print("   4. Generate token manually: " + TOKEN_NAME)
        print("   5. Update sample-project/sonar-project.properties")
        sys.exit(1)
    
    # Update properties file
    if update_properties_file(token):
        print(f"\n✅ Setup complete! Token: {token}")
        return token
    else:
        print(f"\n⚠️  Setup partially complete. Token: {token}")
        return token

if __name__ == "__main__":
    token = main()
    if token:
        print(token)  # Output token for use in other scripts

