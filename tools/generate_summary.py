import argparse
import json
import xml.etree.ElementTree as ET

def parse_trivy(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def parse_dependency_check(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        vulns = []
        for dep in root.findall(".//dependency"):
            for vuln in dep.findall("vulnerability"):
                vulns.append({
                    "dependency": dep.findtext("fileName"),
                    "name": vuln.findtext("name"),
                    "severity": vuln.findtext("severity")
                })
        return vulns
    except:
        return []

def parse_sonar(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sonar", help="SonarQube JSON report", required=False)
    parser.add_argument("--trivy", help="Trivy JSON report", required=False)
    parser.add_argument("--depdep", help="Dependency-check XML report", required=False)
    args = parser.parse_args()

    report = {}

    if args.sonar:
        report["sonar"] = parse_sonar(args.sonar)
    if args.trivy:
        report["trivy"] = parse_trivy(args.trivy)
    if args.depdep:
        report["dependency_check"] = parse_dependency_check(args.depdep)

    with open("reports/summary.json", "w") as f:
        json.dump(report, f, indent=2)

    print("✅ Security Summary Report generated at reports/summary.json")

if __name__ == "__main__":
    main()
