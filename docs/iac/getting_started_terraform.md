---
title: Getting Started with Terraform
description: Learn more about Terraform and how to use it for Infrastructure as Code.
icon: material/terraform
---

# Getting Started with Terraform

> Terraform is a declarative Infrastructure as Code tool that helps you provision and manage infrastructure consistently across environments. It is a strong fit when you want reusable workflows, provider-based automation, and a common language across cloud platforms.

!!! abstract "Why start with Terraform?"

    - Terraform uses a consistent workflow across providers and environments.
    - It gives you a clear execution plan before infrastructure changes are applied.
    - It works well for teams that want reusable modules and multi-environment automation.

---

## What is Terraform?

Terraform is HashiCorp's Infrastructure as Code tool for defining and provisioning infrastructure through configuration files. It offers:

- **Declarative configuration**: Describe the desired state instead of scripting every step
- **Execution plans**: Review what will change before applying it
- **Provider ecosystem**: Manage Azure, AWS, GitHub, Kubernetes, and more
- **Reusable modules**: Standardize common infrastructure patterns across teams

With Terraform, you can provision, update, and manage infrastructure in a repeatable and version-controlled way.

!!! tip "When to use Terraform"

    Terraform is a good default when you want a provider-based workflow, reusable modules, and a consistent deployment model across multiple environments or multiple platforms.

---

## Prerequisites

To get started with Terraform on Azure, you need:

- [ ] **Azure subscription** with permission to create resources
- [ ] **Terraform CLI** installed locally
- [ ] **Azure CLI** for authentication to Azure
- [ ] **Visual Studio Code**
- [ ] **Terraform VS Code extension**

---

## Step 1: Install Terraform CLI

Download and install Terraform from the [official Terraform installation guide](https://developer.hashicorp.com/terraform/install).

=== ":material-microsoft-windows: Windows"

    ```powershell
    winget install --exact Hashicorp.Terraform
    ```

=== ":material-apple: macOS"

    ```sh
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
    ```

=== ":material-linux: Linux"

        ```sh
        wget -O- https://apt.releases.hashicorp.com/gpg | \
            gpg --dearmor | \
            sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
            sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt update
        sudo apt install terraform
        ```

Verify installation:

```sh
terraform version
```

---

## Step 2: Install Azure CLI

Terraform can authenticate to Azure in several ways. For local development, Azure CLI authentication is the simplest path.

=== ":material-microsoft-windows: Windows"

    ```powershell
    winget install --exact --id Microsoft.AzureCLI
    ```

=== ":material-apple: macOS"

    ```sh
    brew update
    brew install azure-cli
    ```

=== ":material-linux: Linux"

    ```sh
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
    ```

Verify installation:

```sh
az --version
```

---

## Step 3: Set Up Visual Studio Code

1. [Download and install VS Code](https://code.visualstudio.com/)
2. Open VS Code
3. Go to Extensions (Ctrl+Shift+X)
4. Search for **HashiCorp Terraform** and install the [Terraform extension](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)

**Features:**

- Syntax highlighting
- IntelliSense and autocompletion
- Formatting support
- Linting and validation assistance

---

## Step 4: Create Your First Terraform File

Create a new file named `main.tf` and add the following example:

```hcl
terraform {
    required_version = ">= 1.5.0"

    required_providers {
        azurerm = {
            source  = "hashicorp/azurerm"
            version = "~> 4.0"
        }
    }
}

provider "azurerm" {
    features {}
}

resource "azurerm_resource_group" "demo" {
    name     = "rg-terraform-demo"
    location = "westeurope"
}
```

This example uses the AzureRM provider to create a resource group, which is a good first Terraform deployment because the configuration is small, readable, and easy to verify.

---

## Step 5: Initialize the Working Directory

Before Terraform can plan or apply changes, initialize the directory so it can download the required provider plugins:

```sh
terraform init
```

!!! info "What `terraform init` does"

    Initialization prepares the working directory, downloads the AzureRM provider, and creates the `.terraform` metadata used for future commands.

---

## Step 6: Deploy with Terraform

Sign in to Azure, review the execution plan, and apply the configuration:

```sh
az login
terraform plan
terraform apply
```

!!! warning "Review the plan before applying"

    `terraform plan` shows the resources Terraform intends to create, update, or destroy. Review it carefully before running `terraform apply`, especially in shared or production subscriptions.

??? tip "Common first-run issues"

    - Make sure you are signed into the correct Azure subscription.
    - Confirm your account has permission to create Azure resources.
    - If the AzureRM provider version changes, rerun `terraform init`.
    - If your working directory already has state from a previous experiment, inspect `terraform.tfstate` before applying new changes.

## What to Do Next

Once this deployment works, the next logical steps are:

1. Add input variables for names, tags, and locations.
2. Split reusable infrastructure into Terraform modules.
3. Run `terraform fmt` and `terraform validate` before planning.
4. Store state securely and avoid keeping production state only on a local machine.

---

## Additional Resources

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [AzureRM Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language)
- [Terraform VS Code Extension](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
- [Terraform Registry](https://registry.terraform.io/)

---

**Congratulations!** You are now ready to start building Azure infrastructure with Terraform in VS Code.
