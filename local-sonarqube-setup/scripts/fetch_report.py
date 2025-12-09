#!/usr/bin/env python3
"""
SonarQube Admin API Report Fetcher

Fetches quality gate status, metrics, and issues from SonarQube API
and generates JSON, HTML, and console reports.
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from typing import Dict, Any, Optional

# ANSI color codes for console output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def fetch_quality_gate_status(host: str, auth_tuple, project_key: str) -> Dict[str, Any]:
    """Fetch quality gate status for a project."""
    url = f"{host}/api/qualitygates/project_status"
    params = {"projectKey": project_key}
    
    response = requests.get(url, params=params, auth=auth_tuple)
    response.raise_for_status()
    return response.json()


def fetch_measures(host: str, auth_tuple, project_key: str) -> Dict[str, Any]:
    """Fetch project measures/metrics."""
    url = f"{host}/api/measures/component"
    params = {
        "component": project_key,
        "metricKeys": "coverage,bugs,vulnerabilities,code_smells,duplicated_lines_density,lines,lines_to_cover"
    }
    
    response = requests.get(url, params=params, auth=auth_tuple)
    response.raise_for_status()
    return response.json()


def fetch_issues(host: str, auth_tuple, project_key: str) -> Dict[str, Any]:
    """Fetch project issues."""
    url = f"{host}/api/issues/search"
    params = {
        "projectKeys": project_key,
        "resolved": "false",
        "ps": 500
    }
    
    response = requests.get(url, params=params, auth=auth_tuple)
    response.raise_for_status()
    return response.json()


def extract_metric_value(measures: Dict, metric_key: str) -> Optional[float]:
    """Extract metric value from measures response."""
    try:
        for measure in measures.get("component", {}).get("measures", []):
            if measure.get("metric") == metric_key:
                value = measure.get("value")
                return float(value) if value else 0.0
    except (KeyError, ValueError, TypeError):
        pass
    return 0.0


def get_code_context(file_path: str, line_number: int, context_lines: int = 3) -> Dict[str, Any]:
    """Get code context around a specific line number."""
    try:
        # Try to read from sample-project directory
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        full_path = os.path.join(project_root, "sample-project", file_path)
        
        if not os.path.exists(full_path):
            # Try relative path
            full_path = file_path
            if not os.path.exists(full_path):
                return {"error": f"File not found: {file_path}"}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = max(0, line_number - context_lines - 1)
        end_line = min(len(lines), line_number + context_lines)
        
        context = []
        for i in range(start_line, end_line):
            context.append({
                "line": i + 1,
                "code": lines[i].rstrip('\n'),
                "is_issue_line": (i + 1) == line_number
            })
        
        return {
            "file": file_path,
            "issue_line": line_number,
            "context": context,
            "start_line": start_line + 1,
            "end_line": end_line
        }
    except Exception as e:
        return {"error": str(e)}


def generate_json_report(data: Dict[str, Any], output_file: str = "report.json"):
    """Generate JSON report."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"📄 JSON report saved to: {output_file}")


def generate_html_report(data: Dict[str, Any], output_file: str = "report.html"):
    """Generate HTML report."""
    qg_status = data.get("quality_gate", {}).get("status", "UNKNOWN")
    measures = data.get("measures", {})
    issues = data.get("issues", {})
    
    status_color = {
        "OK": "#4CAF50",
        "ERROR": "#F44336",
        "WARN": "#FF9800",
        "NONE": "#9E9E9E"
    }.get(qg_status, "#9E9E9E")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SonarQube Report - {data.get('project_key', 'Unknown')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid {status_color};
            padding-bottom: 10px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            color: white;
            font-weight: bold;
            background-color: {status_color};
            margin-bottom: 20px;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .metric-card {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #2196F3;
        }}
        .metric-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .issues-section {{
            margin-top: 30px;
        }}
        .issue-severity {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
        }}
        .severity-blocker {{ background: #D32F2F; color: white; }}
        .severity-critical {{ background: #F44336; color: white; }}
        .severity-major {{ background: #FF9800; color: white; }}
        .severity-minor {{ background: #FFC107; color: black; }}
        .severity-info {{ background: #2196F3; color: white; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: 600;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 12px;
            text-align: center;
        }}
        .issue-detail {{
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: #fafafa;
        }}
        .issue-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        .issue-file {{
            font-family: 'Courier New', monospace;
            color: #666;
            font-size: 14px;
            margin-left: 10px;
        }}
        .code-block {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            margin-top: 10px;
        }}
        .code-line {{
            display: flex;
            padding: 2px 0;
        }}
        .line-number {{
            color: #666;
            padding-right: 15px;
            text-align: right;
            min-width: 50px;
            user-select: none;
        }}
        .line-number.issue-line {{
            color: #ff6b6b;
            font-weight: bold;
        }}
        .code-content {{
            flex: 1;
        }}
        .code-content.issue-line {{
            background: rgba(255, 107, 107, 0.2);
            padding: 2px 5px;
            border-left: 3px solid #ff6b6b;
        }}
        .issue-message {{
            margin: 10px 0;
            padding: 10px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
        }}
        .issue-meta {{
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SonarQube Quality Report</h1>
        <div class="status-badge">Quality Gate: {qg_status}</div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Coverage</div>
                <div class="metric-value">{measures.get('coverage', 0):.1f}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Bugs</div>
                <div class="metric-value">{measures.get('bugs', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Vulnerabilities</div>
                <div class="metric-value">{measures.get('vulnerabilities', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Code Smells</div>
                <div class="metric-value">{measures.get('code_smells', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Duplicated Lines</div>
                <div class="metric-value">{measures.get('duplicated_lines_density', 0):.1f}%</div>
            </div>
        </div>
        
        <div class="issues-section">
            <h2>Issues Summary</h2>
            <table>
                <thead>
                    <tr>
                        <th>Severity</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><span class="issue-severity severity-blocker">BLOCKER</span></td>
                        <td>{issues.get('severity_counts', {}).get('BLOCKER', 0)}</td>
                    </tr>
                    <tr>
                        <td><span class="issue-severity severity-critical">CRITICAL</span></td>
                        <td>{issues.get('severity_counts', {}).get('CRITICAL', 0)}</td>
                    </tr>
                    <tr>
                        <td><span class="issue-severity severity-major">MAJOR</span></td>
                        <td>{issues.get('severity_counts', {}).get('MAJOR', 0)}</td>
                    </tr>
                    <tr>
                        <td><span class="issue-severity severity-minor">MINOR</span></td>
                        <td>{issues.get('severity_counts', {}).get('MINOR', 0)}</td>
                    </tr>
                    <tr>
                        <td><span class="issue-severity severity-info">INFO</span></td>
                        <td>{issues.get('severity_counts', {}).get('INFO', 0)}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="issues-section">
            <h2>Detailed Issues</h2>"""
    
    # Add detailed issues with code blocks
    detailed_issues = issues.get('detailed', [])
    for issue in detailed_issues:
        severity = issue.get('severity', 'UNKNOWN')
        severity_class = f"severity-{severity.lower()}"
        component = issue.get('component', 'Unknown')
        line = issue.get('line', 'N/A')
        message = issue.get('message', 'No message')
        rule = issue.get('rule', 'Unknown')
        code_context = issue.get('codeContext', {})
        
        html += f"""
            <div class="issue-detail">
                <div class="issue-header">
                    <span class="issue-severity {severity_class}">{severity}</span>
                    <span class="issue-file">{component}:{line}</span>
                </div>
                <div class="issue-message">
                    <strong>{message}</strong>
                </div>
                <div class="issue-meta">
                    Rule: {rule} | Effort: {issue.get('effort', 'N/A')}
                </div>"""
        
        # Add code block if available
        if code_context and 'context' in code_context and not code_context.get('error'):
            html += """
                <div class="code-block">"""
            for ctx_line in code_context['context']:
                line_num = ctx_line['line']
                code = ctx_line['code'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                is_issue = ctx_line.get('is_issue_line', False)
                line_class = 'issue-line' if is_issue else ''
                html += f"""
                    <div class="code-line">
                        <span class="line-number {line_class}">{line_num}</span>
                        <span class="code-content {line_class}">{code}</span>
                    </div>"""
            html += """
                </div>"""
        
        html += """
            </div>"""
    
    html += f"""
        </div>
        
        <div class="footer">
            Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w') as f:
        f.write(html)
    print(f"🌐 HTML report saved to: {output_file}")


def print_slack_summary(data: Dict[str, Any]):
    """Print Slack-formatted summary."""
    qg_status = data.get("quality_gate", {}).get("status", "UNKNOWN")
    measures = data.get("measures", {})
    issues = data.get("issues", {})
    
    status_emoji = {
        "OK": "✅",
        "ERROR": "❌",
        "WARN": "⚠️",
        "NONE": "⚪"
    }.get(qg_status, "❓")
    
    print("\n" + "="*60)
    print("📱 SLACK-FORMATTED SUMMARY")
    print("="*60)
    print(f"{status_emoji} *Quality Gate Status:* {qg_status}")
    print(f"📊 *Coverage:* {measures.get('coverage', 0):.1f}%")
    print(f"🐛 *Bugs:* {measures.get('bugs', 0)}")
    print(f"🔒 *Vulnerabilities:* {measures.get('vulnerabilities', 0)}")
    print(f"💨 *Code Smells:* {measures.get('code_smells', 0)}")
    print(f"📋 *Duplicated Lines:* {measures.get('duplicated_lines_density', 0):.1f}%")
    print("\n*Issues by Severity:*")
    for severity in ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO']:
        count = issues.get('severity_counts', {}).get(severity, 0)
        if count > 0:
            print(f"  • {severity}: {count}")
    print("="*60 + "\n")


def print_email_summary(data: Dict[str, Any]):
    """Print email-friendly summary."""
    qg_status = data.get("quality_gate", {}).get("status", "UNKNOWN")
    measures = data.get("measures", {})
    issues = data.get("issues", {})
    
    print("\n" + "="*60)
    print("📧 EMAIL-FORMATTED SUMMARY")
    print("="*60)
    print(f"Quality Gate Status: {qg_status}")
    print(f"Project: {data.get('project_key', 'Unknown')}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nMetrics:")
    print(f"  - Coverage: {measures.get('coverage', 0):.1f}%")
    print(f"  - Bugs: {measures.get('bugs', 0)}")
    print(f"  - Vulnerabilities: {measures.get('vulnerabilities', 0)}")
    print(f"  - Code Smells: {measures.get('code_smells', 0)}")
    print(f"  - Duplicated Lines: {measures.get('duplicated_lines_density', 0):.1f}%")
    print("\nIssues by Severity:")
    for severity in ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO']:
        count = issues.get('severity_counts', {}).get(severity, 0)
        print(f"  - {severity}: {count}")
    print("="*60 + "\n")


def print_detailed_issues(data: Dict[str, Any]):
    """Print detailed issues with code blocks."""
    issues = data.get("issues", {})
    detailed_issues = issues.get("detailed", [])
    
    if not detailed_issues:
        return
    
    print("\n" + "="*80)
    print("📋 DETAILED ISSUES WITH CODE CONTEXT")
    print("="*80)
    
    for idx, issue in enumerate(detailed_issues, 1):
        severity = issue.get("severity", "UNKNOWN")
        component = issue.get("component", "Unknown")
        line = issue.get("line", "N/A")
        message = issue.get("message", "No message")
        rule = issue.get("rule", "Unknown")
        code_context = issue.get("codeContext", {})
        
        # Color based on severity
        severity_colors = {
            "BLOCKER": Colors.RED,
            "CRITICAL": Colors.RED,
            "MAJOR": Colors.YELLOW,
            "MINOR": Colors.BLUE,
            "INFO": Colors.BLUE
        }
        color = severity_colors.get(severity, Colors.RESET)
        
        print(f"\n{color}[{severity}]{Colors.RESET} Issue #{idx}")
        print(f"  File: {component}")
        print(f"  Line: {line}")
        print(f"  Rule: {rule}")
        print(f"  Message: {message}")
        
        # Print code context
        if code_context and 'context' in code_context and not code_context.get('error'):
            print(f"\n  Code Context (lines {code_context.get('start_line', '?')}-{code_context.get('end_line', '?')}):")
            print("  " + "-"*76)
            for ctx_line in code_context['context']:
                line_num = ctx_line['line']
                code = ctx_line['code']
                is_issue = ctx_line.get('is_issue_line', False)
                
                if is_issue:
                    print(f"  {Colors.RED}>>>{Colors.RESET} {line_num:4d} | {code}")
                else:
                    print(f"     {line_num:4d} | {code}")
            print("  " + "-"*76)
        elif code_context.get('error'):
            print(f"  {Colors.YELLOW}⚠️  Could not load code context: {code_context['error']}{Colors.RESET}")
        
        print()
    
    print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch SonarQube project report")
    parser.add_argument("--host", default=os.getenv("SONAR_HOST", "http://localhost:9000"),
                       help="SonarQube host URL")
    parser.add_argument("--token", default=None,
                       help="SonarQube authentication token (or set SONAR_TOKEN env var)")
    parser.add_argument("--user", default=None,
                       help="SonarQube username (for admin access)")
    parser.add_argument("--password", default=None,
                       help="SonarQube password (for admin access)")
    parser.add_argument("--project", required=True,
                       help="SonarQube project key (or set SONAR_PROJECT_KEY env var)")
    parser.add_argument("--json-output", default="report.json",
                       help="JSON output file path")
    parser.add_argument("--html-output", default="report.html",
                       help="HTML output file path")
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("SONAR_TOKEN")
    project_key = args.project or os.getenv("SONAR_PROJECT_KEY")
    
    if not project_key:
        print("❌ Error: Project key is required. Use --project or set SONAR_PROJECT_KEY env var.")
        sys.exit(1)
    
    # Determine authentication method
    if token:
        auth_tuple = (token, "")  # Token as username, empty password
    else:
        auth_tuple = (args.user or "admin", args.password or "admin")  # Username/password
    
    host = args.host.rstrip('/')
    
    print(f"🔍 Fetching report for project: {project_key}")
    print(f"🌐 SonarQube host: {host}")
    
    try:
        # Fetch data
        print("📊 Fetching quality gate status...")
        qg_data = fetch_quality_gate_status(host, auth_tuple, project_key)
        
        print("📈 Fetching measures...")
        measures_data = fetch_measures(host, auth_tuple, project_key)
        
        print("🔎 Fetching issues...")
        issues_data = fetch_issues(host, auth_tuple, project_key)
        
        # Process measures
        measures = {
            "coverage": extract_metric_value(measures_data, "coverage"),
            "bugs": int(extract_metric_value(measures_data, "bugs")),
            "vulnerabilities": int(extract_metric_value(measures_data, "vulnerabilities")),
            "code_smells": int(extract_metric_value(measures_data, "code_smells")),
            "duplicated_lines_density": extract_metric_value(measures_data, "duplicated_lines_density")
        }
        
        # Process issues with detailed information
        severity_counts = {}
        detailed_issues = []
        
        for issue in issues_data.get("issues", []):
            severity = issue.get("severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Extract detailed issue information
            component = issue.get("component", "").replace(f"{project_key}:", "")
            line_number = issue.get("line")
            
            # Get code context
            code_context = {}
            if line_number and component:
                code_context = get_code_context(component, line_number)
            
            issue_detail = {
                "key": issue.get("key"),
                "rule": issue.get("rule"),
                "severity": severity,
                "type": issue.get("type"),
                "component": component,
                "line": line_number,
                "message": issue.get("message"),
                "effort": issue.get("effort"),
                "textRange": issue.get("textRange", {}),
                "tags": issue.get("tags", []),
                "codeContext": code_context
            }
            detailed_issues.append(issue_detail)
        
        issues = {
            "total": issues_data.get("total", 0),
            "severity_counts": severity_counts,
            "detailed": detailed_issues
        }
        
        # Compile report data
        report_data = {
            "project_key": project_key,
            "generated_at": datetime.now().isoformat(),
            "quality_gate": {
                "status": qg_data.get("projectStatus", {}).get("status", "UNKNOWN"),
                "conditions": qg_data.get("projectStatus", {}).get("conditions", [])
            },
            "measures": measures,
            "issues": issues
        }
        
        # Generate reports
        generate_json_report(report_data, args.json_output)
        generate_html_report(report_data, args.html_output)
        
        # Print summaries
        print_slack_summary(report_data)
        print_email_summary(report_data)
        print_detailed_issues(report_data)
        
        print(f"{Colors.GREEN}✅ Report generation completed successfully!{Colors.RESET}")
        
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}❌ Error fetching data from SonarQube: {e}{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()

