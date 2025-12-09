#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🛑 Stopping SonarQube..."
cd "$COMPOSE_DIR"

docker compose down

echo "✅ SonarQube stopped successfully"
echo ""
echo "💡 To remove all data volumes, run:"
echo "   docker compose down -v"

