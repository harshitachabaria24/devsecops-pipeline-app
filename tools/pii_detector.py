import re
import os
import sys

# Define regex patterns for sensitive data
patterns = {
    "AWS Secret Key": r"(?i)aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Password": r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
    "Email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
}

def scan_file(filepath):
    findings = []
    with open(filepath, "r", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            for name, regex in patterns.items():
                if re.search(regex, line):
                    findings.append(f"{name} in {filepath}:{i} → {line.strip()}")
    return findings

def main():
    root = "."
    findings = []
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith((".java", ".xml", ".yml", ".properties", ".txt", ".py")):
                filepath = os.path.join(subdir, file)
                findings.extend(scan_file(filepath))
    
    if findings:
        print("❌ Sensitive data detected:")
        for f in findings:
            print(f)
        sys.exit(1)  # Fail build
    else:
        print("✅ No sensitive data found.")

if __name__ == "__main__":
    main()
