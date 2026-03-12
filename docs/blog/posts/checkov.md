---
date:
    created: 2026-03-11
    updated: 2026-03-11
categories:
    - Technology
tags:
    - Cloud Computing
authors:
    - rushikesh
slug: policy-as-code
---
# 🛡️ Policy as Code with Checkov — Azure Infrastructure Security

> A comprehensive guide to implementing Policy as Code using [Checkov](https://www.checkov.io/) for Azure infrastructure, including custom policies, exceptions, CI/CD pipelines, and code examples.

<!-- more -->

## 📋 Table of Contents

- [What is Policy as Code?](#what-is-policy-as-code)
- [What is Checkov?](#what-is-checkov)
- [Benefits of Checkov](#benefits-of-checkov)
- [Installation & Quick Start](#installation--quick-start)
- [How to Use Checkov](#how-to-use-checkov)
- [Azure Policy Checks (Key CKV_AZURE Rules)](#azure-policy-checks)
- [Python Custom Policy for Azure](#python-custom-policy-for-azure)
- [Go-based Policy Runner for Azure](#go-based-policy-runner-for-azure)
- [Exceptions & Suppression in Checkov](#exceptions--suppression-in-checkov)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Azure DevOps Pipeline](#azure-devops-pipeline)
- [Output Formats](#output-formats)
- [References](#references)

---

## What is Policy as Code?

**Policy as Code (PaC)** is the practice of defining, managing, and enforcing security, compliance, and operational policies through machine-readable definition files — the same way developers manage application code.

Instead of manually reviewing infrastructure for compliance, policies are:

- Stored in **version control** (Git)
- **Automatically evaluated** on every code change
- **Enforced in CI/CD pipelines** before any resources are deployed
- **Auditable** and **traceable** with a full history of changes

### Traditional vs. Policy as Code

| Aspect | Traditional | Policy as Code |
|---|---|---|
| Policy enforcement | Manual review | Automated scanning |
| Consistency | Varies by reviewer | Consistent every run |
| Speed | Slow, bottleneck | Instant in pipeline |
| Auditability | Hard to track | Full Git history |
| Drift detection | Reactive | Proactive / pre-deploy |

---

## What is Checkov?

[Checkov](https://www.checkov.io/) is an **open-source static analysis tool** for Infrastructure as Code (IaC) developed by [Bridgecrew (now part of Prisma Cloud)](https://bridgecrew.io/). It scans cloud infrastructure configurations to detect security misconfigurations and compliance violations **before** resources are deployed.

Checkov supports:

| IaC Framework | Support |
|---|---|
| Terraform (HCL) | ✅ Full |
| Azure ARM Templates | ✅ Full |
| Azure Bicep | ✅ Full |
| Kubernetes (YAML) | ✅ Full |
| Dockerfile | ✅ Full |
| CloudFormation | ✅ Full |
| Ansible | ✅ Full |
| GitHub Actions | ✅ Full |
| Azure Pipelines YAML | ✅ Full |
| Helm Charts | ✅ Full |

Checkov contains **over 1,000 built-in policies** mapped to CIS Benchmarks, NIST, PCI-DSS, SOC2, and other compliance frameworks.

---

## Benefits of Checkov

### 🔒 Security
- Detects misconfigurations **before deployment** — shift-left security
- Covers encryption, access controls, logging, network exposure, and secrets
- Maps violations to industry frameworks (CIS, NIST, SOC2, PCI-DSS, HIPAA)

### 💰 Cost & Risk Reduction
- Prevents costly security incidents caused by misconfigured infrastructure
- Reduces manual security review overhead
- Eliminates compliance drift between environments

### ⚡ Developer Experience
- Integrates natively into Git workflows (pre-commit, PR checks)
- Provides clear, actionable output with resource names and fix guidance
- Supports inline suppressions for justified exceptions

### 🔁 Consistency & Repeatability
- Same policy checks run identically across every environment
- Policies evolve alongside code in version control
- No reliance on individual reviewer expertise

### 🧩 Extensibility
- Write **custom policies** in Python or YAML
- Share policies across teams using external policy repositories
- Integrate with Prisma Cloud for enterprise-grade management

### 📊 Multi-Format Reporting
- Output as JSON, JUnit XML, SARIF, CycloneDX, CSV
- Native integration with GitHub Security tab (SARIF)
- Dashboards via Bridgecrew/Prisma Cloud platform

---

## Installation & Quick Start

### Prerequisites
- Python 3.7+
- pip or pipx
- Terraform, ARM, or Bicep files to scan

### Install Checkov

```bash
# Via pip
pip install checkov

# Via pipx (recommended for isolation)
pipx install checkov

# Via Docker
docker pull bridgecrew/checkov
```

### Verify Installation

```bash
checkov --version
```

### Basic Scan

```bash
# Scan a Terraform directory
checkov -d ./terraform/

# Scan a specific file
checkov -f ./main.tf

# Scan ARM templates
checkov -d ./arm-templates/ --framework arm

# Scan Bicep files
checkov -d ./bicep/ --framework bicep

# Scan and output to JSON
checkov -d ./terraform/ -o json > results.json
```

---

## How to Use Checkov

### Scan by Framework

```bash
# Terraform
checkov -d . --framework terraform

# Azure ARM
checkov -d . --framework arm

# Azure Bicep
checkov -d . --framework bicep

# Kubernetes
checkov -d . --framework kubernetes

# All frameworks
checkov -d . --framework all
```

### Run Specific Checks

```bash
# Run only specific check IDs
checkov -d . --check CKV_AZURE_1,CKV_AZURE_35,CKV_AZURE_13

# Skip specific check IDs
checkov -d . --skip-check CKV_AZURE_50,CKV_AZURE_131
```

### Filter by Severity

```bash
# Only show HIGH and CRITICAL failures
checkov -d . --check-threshold HIGH
```

### Soft Fail Mode (non-blocking)

```bash
# Exit 0 even on failures (useful for reporting-only mode)
checkov -d . --soft-fail
```

### External Custom Policies

```bash
# Point to a directory with custom policies
checkov -d . --external-checks-dir ./custom_policies/
```

---

## Azure Policy Checks

Checkov includes hundreds of built-in Azure checks (prefix `CKV_AZURE_`). Below are the most critical ones:

### Storage & Data

| Check ID | Description |
|---|---|
| `CKV_AZURE_3` | Ensure that Storage Account has 'Secure Transfer' enabled |
| `CKV_AZURE_33` | Ensure Storage logging is enabled for Queue service |
| `CKV_AZURE_35` | Ensure default action is set to Deny for Storage Accounts |
| `CKV_AZURE_36` | Ensure 'Trusted Microsoft Services' is enabled for Storage |
| `CKV_AZURE_43` | Ensure Storage Account names use lowercase letters only |
| `CKV_AZURE_44` | Ensure Storage Account uses the latest TLS version |
| `CKV2_AZURE_1` | Ensure Storage Account has CMK encryption enabled |
| `CKV2_AZURE_21` | Ensure Storage logging is enabled for Blob service |

### Networking & Security

| Check ID | Description |
|---|---|
| `CKV_AZURE_9` | Ensure no SQL Databases allow ingress from 0.0.0.0/0 |
| `CKV_AZURE_10` | Ensure that Microsoft Antimalware is configured to auto-update |
| `CKV_AZURE_13` | Ensure App Service has 'Register with Azure Active Directory' enabled |
| `CKV_AZURE_16` | Ensure App Service uses an SSL certificate |
| `CKV_AZURE_17` | Ensure Web App Redirect HTTPS is enabled |
| `CKV_AZURE_78` | Ensure Web app does not have an overly permissive CORS policy |

### Identity & Access (IAM)

| Check ID | Description |
|---|---|
| `CKV_AZURE_1` | Ensure Azure Instance does not use basic authentication |
| `CKV_AZURE_110` | Ensure Keyvault has soft delete enabled |
| `CKV_AZURE_111` | Ensure Keyvault has purge protection enabled |
| `CKV_AZURE_131` | Ensure Keyvault key expiration is set |

### Monitoring & Logging

| Check ID | Description |
|---|---|
| `CKV_AZURE_4` | Ensure AKS Logging to Azure Monitoring is configured |
| `CKV_AZURE_6` | Ensure that the Azure Monitor logging profile stores the activity logs |
| `CKV_AZURE_37` | Ensure that 'Activity Retention Log' is set to 1 year or greater |
| `CKV_AZURE_50` | Ensure Azure Application Insights is configured |

### Encryption

| Check ID | Description |
|---|---|
| `CKV_AZURE_22` | Ensure that the Azure Activity Log has at least one alert for security events |
| `CKV_AZURE_52` | Ensure Azure SQL Server TDE protector is encrypted with Customer-managed key |
| `CKV_AZURE_54` | Ensure that PostgreSQL server infrastructure encryption is enabled |
| `CKV_AZURE_66` | Ensure Azure SQL Database is using the latest TLS version |

---

## Python Custom Policy for Azure

### Example 1: Ensure Azure Storage Account Uses HTTPS Only

```python
# custom_policies/azure_storage_https_only.py

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class StorageAccountHTTPSOnly(BaseResourceCheck):
    """
    Ensures Azure Storage Accounts enforce HTTPS-only access.
    Maps to: CIS Azure 3.1, Azure Security Benchmark NS-3
    """

    def __init__(self):
        name = "Ensure Azure Storage Account enforces HTTPS-only traffic"
        id = "CKV_CUSTOM_AZURE_001"
        supported_resources = ["azurerm_storage_account"]
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf):
        """
        Checks that enable_https_traffic_only is set to true.
        """
        https_only = conf.get("enable_https_traffic_only", [True])
        if isinstance(https_only, list):
            https_only = https_only[0]

        if https_only is True:
            return CheckResult.PASSED
        return CheckResult.FAILED


scanner = StorageAccountHTTPSOnly()
```

### Example 2: Ensure Azure Key Vault Has Soft Delete and Purge Protection

```python
# custom_policies/azure_keyvault_protection.py

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class KeyVaultSoftDeletePurgeProtection(BaseResourceCheck):
    """
    Ensures Azure Key Vault has both soft_delete_retention_days configured
    and purge_protection_enabled set to true.
    """

    def __init__(self):
        name = "Ensure Azure Key Vault has soft delete and purge protection enabled"
        id = "CKV_CUSTOM_AZURE_002"
        supported_resources = ["azurerm_key_vault"]
        categories = [CheckCategories.BACKUP_AND_RECOVERY]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_resources=supported_resources,
        )

    def scan_resource_conf(self, conf):
        purge_protection = conf.get("purge_protection_enabled", [False])
        soft_delete_days = conf.get("soft_delete_retention_days", [0])

        if isinstance(purge_protection, list):
            purge_protection = purge_protection[0]
        if isinstance(soft_delete_days, list):
            soft_delete_days = soft_delete_days[0]

        if purge_protection is True and int(soft_delete_days) >= 7:
            return CheckResult.PASSED

        return CheckResult.FAILED


scanner = KeyVaultSoftDeletePurgeProtection()
```

### Example 3: YAML-based Custom Policy for Azure NSG

```yaml
# custom_policies/azure_nsg_deny_ssh.yaml

metadata:
  name: "Ensure NSG does not allow unrestricted SSH from the internet"
  id: "CKV2_CUSTOM_AZURE_001"
  category: "NETWORKING"
  severity: "HIGH"
  guidelines: |
    Azure Network Security Groups should not allow inbound SSH (port 22)
    from 0.0.0.0/0 or ::/0. Restrict SSH access to trusted IP ranges only.

scope:
  provider: azurerm

definition:
  and:
    - not:
        resource_type: azurerm_network_security_group
        contains:
          security_rule:
            - access: Allow
              direction: Inbound
              protocol: "Tcp"
              destination_port_range: "22"
              source_address_prefix: "*"
```

### Example 4: Full Python Scanner Script for Azure Resources

```python
#!/usr/bin/env python3
"""
azure_checkov_scanner.py
Run Checkov programmatically against Azure Terraform configurations
and generate a structured compliance report.
"""

import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path


def run_checkov_scan(
    target_dir: str,
    framework: str = "terraform",
    check_ids: list = None,
    skip_ids: list = None,
    external_checks_dir: str = None,
    output_format: str = "json",
) -> dict:
    """
    Runs a Checkov scan against an IaC directory and returns structured results.

    Args:
        target_dir:          Path to the directory containing IaC files
        framework:           IaC framework (terraform, arm, bicep)
        check_ids:           List of specific check IDs to run (None = all)
        skip_ids:            List of check IDs to skip
        external_checks_dir: Path to custom policy directory
        output_format:       Output format (json, sarif, junitxml)

    Returns:
        dict: Parsed scan results
    """
    cmd = [
        "checkov",
        "-d", target_dir,
        "--framework", framework,
        "-o", output_format,
        "--compact",
        "--quiet",
    ]

    if check_ids:
        cmd += ["--check", ",".join(check_ids)]

    if skip_ids:
        cmd += ["--skip-check", ",".join(skip_ids)]

    if external_checks_dir:
        cmd += ["--external-checks-dir", external_checks_dir]

    print(f"[{datetime.now().isoformat()}] Running: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    try:
        scan_results = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("ERROR: Could not parse Checkov output as JSON.")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    return scan_results


def print_azure_summary(results: dict):
    """Print a human-readable summary of Azure-specific findings."""

    results_list = results if isinstance(results, list) else [results]

    total_passed = 0
    total_failed = 0
    azure_failures = []

    for result in results_list:
        summary = result.get("summary", {})
        total_passed += summary.get("passed", 0)
        total_failed += summary.get("failed", 0)

        for check in result.get("results", {}).get("failed_checks", []):
            check_id = check.get("check_id", "")
            if check_id.startswith("CKV_AZURE") or check_id.startswith("CKV2_AZURE"):
                azure_failures.append({
                    "check_id":    check_id,
                    "check_name":  check.get("check_type", ""),
                    "resource":    check.get("resource", ""),
                    "file":        check.get("repo_file_path", ""),
                    "line":        check.get("file_line_range", []),
                    "guideline":   check.get("guideline", ""),
                })

    print("\n" + "=" * 70)
    print("  CHECKOV AZURE COMPLIANCE REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print(f"  ✅ Passed Checks : {total_passed}")
    print(f"  ❌ Failed Checks : {total_failed}")
    print(f"  🔵 Azure Failures: {len(azure_failures)}")
    print("=" * 70)

    if azure_failures:
        print("\n  AZURE POLICY VIOLATIONS:\n")
        for i, failure in enumerate(azure_failures, 1):
            print(f"  [{i}] {failure['check_id']} — {failure['check_name']}")
            print(f"       Resource : {failure['resource']}")
            print(f"       File     : {failure['file']} (lines {failure['line']})")
            if failure["guideline"]:
                print(f"       Guideline: {failure['guideline']}")
            print()

    pass_rate = (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
    print(f"  Compliance Rate: {pass_rate:.1f}%")
    print("=" * 70 + "\n")

    return len(azure_failures) > 0


def save_report(results: dict, output_path: str = "checkov_report.json"):
    """Save full scan results to a JSON file."""
    Path(output_path).write_text(json.dumps(results, indent=2))
    print(f"Full report saved to: {output_path}")


if __name__ == "__main__":
    TARGET_DIR         = "./terraform"          # Path to your Terraform code
    FRAMEWORK          = "terraform"
    EXTERNAL_CHECKS    = "./custom_policies"    # Optional: your custom policies
    REPORT_OUTPUT      = "checkov_azure_report.json"

    # Azure-specific checks to enforce (leave empty for ALL checks)
    ENFORCE_CHECKS = [
        "CKV_AZURE_3",    # Storage HTTPS
        "CKV_AZURE_13",   # App Service AAD auth
        "CKV_AZURE_35",   # Storage default deny
        "CKV_AZURE_36",   # Storage trusted MS services
        "CKV_AZURE_44",   # Storage TLS version
        "CKV_AZURE_110",  # KeyVault soft delete
        "CKV_AZURE_111",  # KeyVault purge protection
        "CKV_AZURE_131",  # KeyVault key expiration
        "CKV2_AZURE_1",   # Storage CMK encryption
        "CKV2_AZURE_21",  # Storage logging - Blob
    ]

    results = run_checkov_scan(
        target_dir=TARGET_DIR,
        framework=FRAMEWORK,
        check_ids=ENFORCE_CHECKS if ENFORCE_CHECKS else None,
        external_checks_dir=EXTERNAL_CHECKS,
        output_format="json",
    )

    save_report(results, REPORT_OUTPUT)
    has_failures = print_azure_summary(results)

    sys.exit(1 if has_failures else 0)
```

---

## Go-based Policy Runner for Azure

The following Go program wraps the Checkov CLI, parses its JSON output, and generates a structured Azure compliance report. Ideal for integrating into Go-based toolchains or custom internal developer platforms.

```go
// main.go — Azure Checkov Policy Runner in Go
// Usage: go run main.go --dir ./terraform --framework terraform

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

// ---------------------------------------------------------------------------
// Data Structures
// ---------------------------------------------------------------------------

type CheckovSummary struct {
	Passed   int `json:"passed"`
	Failed   int `json:"failed"`
	Skipped  int `json:"skipped"`
	Errors   int `json:"parsing_error"`
}

type FailedCheck struct {
	CheckID      string   `json:"check_id"`
	CheckType    string   `json:"check_type"`
	Resource     string   `json:"resource"`
	RepoFilePath string   `json:"repo_file_path"`
	FileLines    []int    `json:"file_line_range"`
	Guideline    string   `json:"guideline"`
}

type CheckovResults struct {
	FailedChecks []FailedCheck `json:"failed_checks"`
	PassedChecks []FailedCheck `json:"passed_checks"`
}

type CheckovOutput struct {
	Summary CheckovSummary `json:"summary"`
	Results CheckovResults `json:"results"`
}

// ---------------------------------------------------------------------------
// Run Checkov
// ---------------------------------------------------------------------------

func runCheckov(dir, framework, externalChecksDir string, checkIDs, skipIDs []string) (*CheckovOutput, error) {
	args := []string{
		"-d", dir,
		"--framework", framework,
		"-o", "json",
		"--compact",
		"--quiet",
	}

	if len(checkIDs) > 0 {
		args = append(args, "--check", strings.Join(checkIDs, ","))
	}
	if len(skipIDs) > 0 {
		args = append(args, "--skip-check", strings.Join(skipIDs, ","))
	}
	if externalChecksDir != "" {
		args = append(args, "--external-checks-dir", externalChecksDir)
	}

	fmt.Printf("[%s] Running: checkov %s\n", time.Now().Format(time.RFC3339), strings.Join(args, " "))

	cmd := exec.Command("checkov", args...)
	output, err := cmd.Output()
	if err != nil {
		// Checkov returns exit code 1 on failures — that's expected
		if exitErr, ok := err.(*exec.ExitError); ok {
			_ = exitErr // non-zero exit is expected when checks fail
		} else {
			return nil, fmt.Errorf("failed to run checkov: %w", err)
		}
	}

	// Handle array-wrapped JSON (Checkov sometimes returns a JSON array)
	rawOutput := strings.TrimSpace(string(output))

	var result CheckovOutput
	if strings.HasPrefix(rawOutput, "[") {
		var arr []CheckovOutput
		if err := json.Unmarshal([]byte(rawOutput), &arr); err != nil {
			return nil, fmt.Errorf("failed to parse checkov JSON array: %w", err)
		}
		if len(arr) > 0 {
			result = arr[0]
		}
	} else {
		if err := json.Unmarshal([]byte(rawOutput), &result); err != nil {
			return nil, fmt.Errorf("failed to parse checkov JSON: %w\nOutput: %s", err, rawOutput[:min(500, len(rawOutput))])
		}
	}

	return &result, nil
}

// ---------------------------------------------------------------------------
// Reporting
// ---------------------------------------------------------------------------

func printAzureSummary(result *CheckovOutput) bool {
	azureFailures := []FailedCheck{}
	for _, check := range result.Results.FailedChecks {
		if strings.HasPrefix(check.CheckID, "CKV_AZURE") || strings.HasPrefix(check.CheckID, "CKV2_AZURE") {
			azureFailures = append(azureFailures, check)
		}
	}

	total := result.Summary.Passed + result.Summary.Failed
	passRate := 0.0
	if total > 0 {
		passRate = float64(result.Summary.Passed) / float64(total) * 100
	}

	border := strings.Repeat("=", 70)
	fmt.Println("\n" + border)
	fmt.Println("  CHECKOV AZURE COMPLIANCE REPORT")
	fmt.Printf("  Generated: %s\n", time.Now().Format("2006-01-02 15:04:05"))
	fmt.Println(border)
	fmt.Printf("  ✅ Passed Checks  : %d\n", result.Summary.Passed)
	fmt.Printf("  ❌ Failed Checks  : %d\n", result.Summary.Failed)
	fmt.Printf("  ⏭  Skipped Checks : %d\n", result.Summary.Skipped)
	fmt.Printf("  🔵 Azure Failures : %d\n", len(azureFailures))
	fmt.Println(border)

	if len(azureFailures) > 0 {
		fmt.Println("\n  AZURE POLICY VIOLATIONS:\n")
		for i, f := range azureFailures {
			fmt.Printf("  [%d] %s — %s\n", i+1, f.CheckID, f.CheckType)
			fmt.Printf("       Resource : %s\n", f.Resource)
			fmt.Printf("       File     : %s (lines %v)\n", f.RepoFilePath, f.FileLines)
			if f.Guideline != "" {
				fmt.Printf("       Guideline: %s\n", f.Guideline)
			}
			fmt.Println()
		}
	}

	fmt.Printf("  Compliance Rate: %.1f%%\n", passRate)
	fmt.Println(border + "\n")

	return len(azureFailures) > 0
}

func saveReport(result *CheckovOutput, outputPath string) error {
	data, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		return err
	}
	if err := os.WriteFile(outputPath, data, 0644); err != nil {
		return err
	}
	fmt.Printf("Full report saved to: %s\n", outputPath)
	return nil
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

func main() {
	dir              := flag.String("dir", "./terraform", "Directory containing IaC files")
	framework        := flag.String("framework", "terraform", "IaC framework: terraform, arm, bicep")
	externalChecks   := flag.String("external-checks", "", "Path to custom policy directory")
	reportOutput     := flag.String("report", "checkov_azure_report.json", "Output JSON report path")
	softFail         := flag.Bool("soft-fail", false, "Exit 0 even if checks fail (report-only mode)")
	flag.Parse()

	// Azure checks to enforce
	enforceChecks := []string{
		"CKV_AZURE_3",    // Storage HTTPS only
		"CKV_AZURE_13",   // App Service AAD auth
		"CKV_AZURE_35",   // Storage default deny
		"CKV_AZURE_36",   // Storage trusted Microsoft services
		"CKV_AZURE_44",   // Storage TLS version
		"CKV_AZURE_110",  // KeyVault soft delete
		"CKV_AZURE_111",  // KeyVault purge protection
		"CKV_AZURE_131",  // KeyVault key expiration
		"CKV2_AZURE_1",   // Storage CMK encryption
		"CKV2_AZURE_21",  // Storage logging for Blob service
	}

	result, err := runCheckov(*dir, *framework, *externalChecks, enforceChecks, nil)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: %v\n", err)
		os.Exit(2)
	}

	if err := saveReport(result, *reportOutput); err != nil {
		fmt.Fprintf(os.Stderr, "WARNING: Could not save report: %v\n", err)
	}

	hasFailures := printAzureSummary(result)

	if hasFailures && !*softFail {
		os.Exit(1)
	}

	os.Exit(0)
}
```

**Build and run:**

```bash
go mod init azure-checkov-runner
go build -o checkov-runner .
./checkov-runner --dir ./terraform --framework terraform --report report.json
```

---

## Exceptions & Suppression in Checkov

There are legitimate scenarios where you need to suppress a Checkov check — for example, a legacy resource, a planned remediation, or an accepted business risk. Checkov provides several mechanisms for this.

### ⚠️ When to Use Exceptions

Use exceptions **only** when:
- A deviation is **formally approved** through your risk management process
- A **compensating control** is in place
- The resource is **ephemeral / test-only** and not in scope
- The check produces a **false positive** for your specific use case

**Never** use blanket suppressions to silence noise without investigation.

---

### Method 1: Inline Suppression via Code Comments (Terraform)

Add a `checkov:skip` annotation directly in your Terraform resource:

```hcl
resource "azurerm_storage_account" "example" {
  #checkov:skip=CKV_AZURE_3: Legacy account - HTTPS migration tracked in JIRA-1234
  #checkov:skip=CKV_AZURE_44: TLS upgrade scheduled for Q2 2025 - Risk accepted by InfoSec
  name                     = "mystorageaccount"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  enable_https_traffic_only = false   # Will be remediated
}
```

> **Best practice:** Always include a justification comment after the colon. Suppressions without justification should be rejected in code review.

---

### Method 2: Suppress via `.checkov.yaml` Configuration File

Create a `.checkov.yaml` in your project root:

```yaml
# .checkov.yaml — Project-level Checkov configuration

# Skip specific check IDs globally
skip-check:
  - CKV_AZURE_50    # App Insights — not applicable for backend-only services
  - CKV_AZURE_131   # Key Vault key expiration — managed by separate rotation policy

# Run only these frameworks
framework:
  - terraform
  - arm

# Directories to scan
directory:
  - ./terraform
  - ./arm-templates

# External custom policy directory
external-checks-dir:
  - ./custom_policies

# Output format
output:
  - cli
  - json

# Fail only on HIGH and CRITICAL
check-threshold: MEDIUM

# Compact output
compact: true
```

---

### Method 3: Suppress via `.checkov.baseline` File

Generate a baseline of known/accepted failures and only alert on **new** violations:

```bash
# Generate baseline from current state
checkov -d . -o json > baseline.json
checkov -d . --create-baseline

# Future scans compare against baseline — only new failures are flagged
checkov -d . --baseline .checkov.baseline
```

---

### Method 4: Skip via CLI Flag

```bash
# Skip one or more checks in a one-off scan
checkov -d . --skip-check CKV_AZURE_50,CKV_AZURE_131,CKV2_AZURE_18
```

---

### Suppression Governance Best Practices

```
1. Require justification text for every inline skip comment
2. Track all suppressions in a central register (e.g., spreadsheet, Jira)
3. Set an expiry date for time-limited suppressions
4. Review all suppressions quarterly in security governance meetings
5. Require InfoSec sign-off for HIGH/CRITICAL suppressions
6. Never suppress in main/prod branches without PR approval
```

---

## GitHub Actions Pipeline

Save as `.github/workflows/checkov.yml`:

```yaml
# .github/workflows/checkov.yml
# Checkov IaC security scanning — runs on every PR and push to main

name: "🔐 Checkov Policy as Code"

on:
  push:
    branches:
      - main
      - develop
    paths:
      - "terraform/**"
      - "arm-templates/**"
      - "bicep/**"
      - ".github/workflows/checkov.yml"
  pull_request:
    branches:
      - main
      - develop
    paths:
      - "terraform/**"
      - "arm-templates/**"
      - "bicep/**"

permissions:
  contents: read
  security-events: write   # Required to upload SARIF to GitHub Security tab
  pull-requests: write     # Required to post PR comments

jobs:

  # ── Job 1: Terraform Scan ──────────────────────────────────────────────────
  checkov-terraform:
    name: "Terraform Azure Policies"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov — Terraform
        id: checkov_tf
        run: |
          checkov \
            -d ./terraform \
            --framework terraform \
            -o cli \
            -o sarif \
            --output-file-path . \
            --external-checks-dir ./custom_policies \
            --compact \
            --skip-check CKV_AZURE_50 \
            --check-threshold MEDIUM
        continue-on-error: true   # Upload SARIF even on failure

      - name: Upload SARIF to GitHub Security Tab
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: results.sarif
          category: "checkov-terraform"

      - name: Enforce — fail if HIGH/CRITICAL violations found
        run: |
          checkov \
            -d ./terraform \
            --framework terraform \
            --check-threshold HIGH \
            --compact \
            --quiet
        # This step will actually fail the pipeline on HIGH/CRITICAL

  # ── Job 2: ARM Templates Scan ─────────────────────────────────────────────
  checkov-arm:
    name: "ARM Template Azure Policies"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov — ARM Templates
        run: |
          checkov \
            -d ./arm-templates \
            --framework arm \
            -o cli \
            --compact

  # ── Job 3: Bicep Scan ─────────────────────────────────────────────────────
  checkov-bicep:
    name: "Bicep Azure Policies"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov — Bicep
        run: |
          checkov \
            -d ./bicep \
            --framework bicep \
            -o cli \
            --compact

  # ── Job 4: Secrets Scanning ───────────────────────────────────────────────
  checkov-secrets:
    name: "Secrets Detection"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov — Secrets
        run: |
          checkov \
            -d . \
            --framework secrets \
            --enable-secret-scan-all-files \
            -o cli \
            --compact

  # ── Job 5: Generate Compliance Report ────────────────────────────────────
  compliance-report:
    name: "Generate Compliance Report"
    runs-on: ubuntu-latest
    needs: [checkov-terraform, checkov-arm, checkov-bicep]
    if: always()
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install Checkov
        run: pip install checkov

      - name: Generate JSON Report
        run: |
          checkov \
            -d . \
            --framework terraform,arm,bicep \
            -o json \
            --output-file-path compliance_report \
            --compact \
            --soft-fail

      - name: Upload Compliance Report
        uses: actions/upload-artifact@v4
        with:
          name: checkov-compliance-report
          path: compliance_report/
          retention-days: 30
```

---

## Azure DevOps Pipeline

Save as `azure-pipelines-checkov.yml` in your repository root:

```yaml
# azure-pipelines-checkov.yml
# Checkov IaC security scanning for Azure DevOps

trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - terraform/**
      - arm-templates/**
      - bicep/**
      - azure-pipelines-checkov.yml

pr:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - terraform/**
      - arm-templates/**
      - bicep/**

pool:
  vmImage: "ubuntu-latest"

variables:
  pythonVersion: "3.11"
  checkovVersion: "latest"
  reportDir: "$(Build.ArtifactStagingDirectory)/checkov-reports"
  terraformDir: "$(System.DefaultWorkingDirectory)/terraform"
  armDir: "$(System.DefaultWorkingDirectory)/arm-templates"
  bicepDir: "$(System.DefaultWorkingDirectory)/bicep"

stages:

  # ── Stage 1: Install & Validate ───────────────────────────────────────────
  - stage: Setup
    displayName: "🛠️ Setup"
    jobs:
      - job: InstallCheckov
        displayName: "Install Checkov"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"
            displayName: "Use Python $(pythonVersion)"

          - script: |
              pip install checkov
              checkov --version
            displayName: "Install & verify Checkov"

  # ── Stage 2: Terraform Scan ───────────────────────────────────────────────
  - stage: ScanTerraform
    displayName: "🔐 Scan Terraform"
    dependsOn: Setup
    jobs:
      - job: CheckovTerraform
        displayName: "Checkov — Terraform"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"

          - script: pip install checkov
            displayName: "Install Checkov"

          - script: mkdir -p $(reportDir)
            displayName: "Create report directory"

          - script: |
              checkov \
                -d $(terraformDir) \
                --framework terraform \
                -o cli \
                -o junitxml \
                --output-file-path $(reportDir) \
                --external-checks-dir $(System.DefaultWorkingDirectory)/custom_policies \
                --compact \
                --check-threshold MEDIUM \
                --skip-check CKV_AZURE_50 \
                || true
            displayName: "Run Checkov scan (Terraform)"

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: "JUnit"
              testResultsFiles: "$(reportDir)/results_junitxml.xml"
              testRunTitle: "Checkov — Terraform Azure Policies"
              failTaskOnFailedTests: true
            displayName: "Publish JUnit results"
            condition: always()

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: "$(reportDir)"
              artifactName: "checkov-terraform-report"
            displayName: "Publish report artifacts"
            condition: always()

  # ── Stage 3: ARM Templates Scan ───────────────────────────────────────────
  - stage: ScanARM
    displayName: "🔐 Scan ARM Templates"
    dependsOn: Setup
    jobs:
      - job: CheckovARM
        displayName: "Checkov — ARM Templates"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"

          - script: pip install checkov
            displayName: "Install Checkov"

          - script: mkdir -p $(reportDir)
            displayName: "Create report directory"

          - script: |
              checkov \
                -d $(armDir) \
                --framework arm \
                -o cli \
                -o junitxml \
                --output-file-path $(reportDir) \
                --compact \
                || true
            displayName: "Run Checkov scan (ARM)"

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: "JUnit"
              testResultsFiles: "$(reportDir)/results_junitxml.xml"
              testRunTitle: "Checkov — ARM Templates Azure Policies"
              failTaskOnFailedTests: false
            displayName: "Publish JUnit results"
            condition: always()

  # ── Stage 4: Bicep Scan ───────────────────────────────────────────────────
  - stage: ScanBicep
    displayName: "🔐 Scan Bicep"
    dependsOn: Setup
    jobs:
      - job: CheckovBicep
        displayName: "Checkov — Bicep"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"

          - script: pip install checkov
            displayName: "Install Checkov"

          - script: mkdir -p $(reportDir)
            displayName: "Create report directory"

          - script: |
              checkov \
                -d $(bicepDir) \
                --framework bicep \
                -o cli \
                -o junitxml \
                --output-file-path $(reportDir) \
                --compact \
                || true
            displayName: "Run Checkov scan (Bicep)"

          - task: PublishTestResults@2
            inputs:
              testResultsFormat: "JUnit"
              testResultsFiles: "$(reportDir)/results_junitxml.xml"
              testRunTitle: "Checkov — Bicep Azure Policies"
              failTaskOnFailedTests: false
            displayName: "Publish JUnit results"
            condition: always()

  # ── Stage 5: Secrets Detection ────────────────────────────────────────────
  - stage: SecretsDetection
    displayName: "🔑 Secrets Detection"
    dependsOn: Setup
    jobs:
      - job: CheckovSecrets
        displayName: "Checkov — Secrets"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"

          - script: pip install checkov
            displayName: "Install Checkov"

          - script: |
              checkov \
                -d $(System.DefaultWorkingDirectory) \
                --framework secrets \
                --enable-secret-scan-all-files \
                -o cli \
                --compact
            displayName: "Run secrets scan"
            failOnStderr: false

  # ── Stage 6: Compliance Gate ──────────────────────────────────────────────
  - stage: ComplianceGate
    displayName: "🚦 Compliance Gate"
    dependsOn:
      - ScanTerraform
      - ScanARM
      - ScanBicep
    condition: and(succeeded('ScanTerraform'), not(failed()), not(canceled()))
    jobs:
      - job: ComplianceSummary
        displayName: "Generate Full Compliance Summary"
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(pythonVersion)"

          - script: pip install checkov
            displayName: "Install Checkov"

          - script: mkdir -p $(reportDir)
            displayName: "Create report directory"

          - script: |
              checkov \
                -d $(System.DefaultWorkingDirectory) \
                --framework terraform,arm,bicep \
                -o json \
                --output-file-path $(reportDir)/full_report \
                --compact \
                --soft-fail
            displayName: "Generate full JSON report"

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: "$(reportDir)/full_report"
              artifactName: "checkov-full-compliance-report"
            displayName: "Publish full compliance report"
            condition: always()
```

---

## Output Formats

Checkov supports multiple output formats to fit different toolchain integrations:

| Format | Flag | Use Case |
|---|---|---|
| CLI (default) | `-o cli` | Human-readable terminal output |
| JSON | `-o json` | Parsing, dashboards, APIs |
| JUnit XML | `-o junitxml` | Azure DevOps / Jenkins test results |
| SARIF | `-o sarif` | GitHub Security tab integration |
| CycloneDX BOM | `-o cyclonedx` | Software supply chain compliance |
| CSV | `-o csv` | Spreadsheet reporting |
| GitLab SAST | `-o gitlab_sast` | GitLab Security Dashboard |

### Multi-format output in one run:

```bash
checkov -d ./terraform \
  -o cli \
  -o json \
  -o sarif \
  -o junitxml \
  --output-file-path ./reports
```

---

## References

| Resource | URL |
|---|---|
| Checkov Documentation | https://www.checkov.io/1.Welcome/What%20is%20Checkov.html |
| Full Policy Index | https://www.checkov.io/5.Policy%20Index/all.html |
| Azure ARM Policy Index | https://www.checkov.io/5.Policy%20Index/arm.html |
| Terraform Azure Policy Index | https://www.checkov.io/5.Policy%20Index/terraform.html |
| Custom Python Policies | https://www.checkov.io/3.Custom%20Policies/Python%20Custom%20Policies.html |
| Custom YAML Policies | https://www.checkov.io/3.Custom%20Policies/YAML%20Custom%20Policies.html |
| Suppressing Policies | https://www.checkov.io/2.Basics/Suppressing%20and%20Skipping%20Policies.html |
| GitHub Actions Integration | https://www.checkov.io/4.Integrations/GitHub%20Actions.html |
| Checkov GitHub Repository | https://github.com/bridgecrewio/checkov |
| CIS Azure Benchmark | https://www.cisecurity.org/benchmark/azure |
| Azure Security Benchmark | https://learn.microsoft.com/en-us/security/benchmark/azure/ |

---

*Generated using Checkov v3.x | Policy Index: https://www.checkov.io/5.Policy%20Index/all.html*