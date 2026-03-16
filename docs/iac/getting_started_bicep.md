---
title: Getting Started with Bicep
description: Learn more about Bicep and how to use it for Infrastructure as Code.
icon: material/arm-flex
---

# Getting Started with Bicep

> Bicep is Azure's domain-specific language for Infrastructure as Code. It gives you a cleaner authoring experience than raw ARM JSON while keeping full native integration with Azure Resource Manager.

!!! abstract "Why start with Bicep?"

    - Bicep is easier to read and review than raw ARM JSON.
    - It provides type-aware authoring and validation before deployment.
    - It stays native to Azure Resource Manager and fits Azure-first teams well.

---

## What is Bicep?

Bicep is Microsoft's Infrastructure as Code language for Azure. It is designed to make Azure deployments easier to author and easier to understand. It offers:

- **Simplified syntax**: Easier to read and write than JSON ARM templates
- **Modularity**: Supports reusable modules
- **Type safety & validation**: Catches errors before deployment
- **First-class Azure support**: Compiles directly to ARM templates

With Bicep, you can define, deploy, and manage Azure infrastructure in a repeatable and reliable way.

!!! tip "When to use Bicep"

    Bicep is a strong default when you are primarily targeting Azure and want native resource support, readable templates, and straightforward reuse through modules.

---

## Prerequisites

To get started with Bicep, you need:

- [ ] **Azure subscription** with permission to deploy resources
- [ ] **Azure CLI** version 2.20.0 or later
- [ ] **Bicep CLI** installed manually or downloaded automatically by Azure CLI
- [ ] **Visual Studio Code**
- [ ] **Bicep VS Code extension**

---

## Step 1: Install Azure CLI

Download and install the [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) for your OS.

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

## Step 2: Enable Bicep CLI (Optional)

The Azure CLI automatically downloads the Bicep CLI the first time you use Bicep-aware deployment commands. You can also install it explicitly:

```sh
az bicep install
az bicep version
```

!!! info "Recommended"

    If Bicep is already installed, run `az bicep upgrade` occasionally to stay current with fixes and language improvements.

---

## Step 3: Set Up Visual Studio Code

1. [Download and install VS Code](https://code.visualstudio.com/)
2. Open VS Code
3. Go to Extensions (Ctrl+Shift+X)
4. Search for **Bicep** and install the [Bicep extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)

**Features:**

- Syntax highlighting
- IntelliSense and autocompletion
- Linting and error checking
- Resource snippets

---

## Step 4: (Optional) Install Azure Account Extension

For seamless Azure authentication in VS Code, install the [Azure Account extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.azure-account).

This makes it easier to sign in, browse subscriptions, and work with Azure resources directly from the editor.

---

## Step 5: Create Your First Bicep File

Create a new file named `main.bicep` and add the following example:

```bicep
targetScope = 'subscription'

@description('Name of the resource group to create')
param resourceGroupName string = 'rg-bicep-demo'

@description('Azure region for the resource group')
param location string = 'westeurope'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}
```

This example creates a resource group at **subscription scope**, which is a good first deployment because it is small, clear, and easy to validate.

---

## Step 6: Deploy with Bicep

Sign in and deploy the template with Azure CLI:

```sh
az login
az deployment sub create --location westeurope --template-file main.bicep
```

!!! warning "Deployment scope matters"

    The example above uses `targetScope = 'subscription'`, so it must be deployed with `az deployment sub create`. If your template targets an existing resource group instead, use `az deployment group create`.

??? tip "Common first-run issues"

    - Make sure you are signed into the correct Azure subscription.
    - Confirm your account has permission to create resource groups.
    - If Bicep is missing, run `az bicep install` and retry.
    - If the deployment name collides with a previous run, Azure CLI will still create a new deployment record automatically unless you specify a fixed name.

## What to Do Next

Once this deployment works, the next logical steps are:

1. Add parameters for reusable values such as tags and naming prefixes.
2. Break larger templates into modules.
3. Validate before deployment with `az deployment sub validate`.
4. Store your Bicep files in source control and review them like application code.

---

## Additional Resources

- [Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Bicep Modules](https://learn.microsoft.com/azure/azure-resource-manager/bicep/modules)
- [Bicep Best Practices](https://learn.microsoft.com/azure/azure-resource-manager/bicep/best-practices)
- [Bicep VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
- [Bicep Playground](https://bicepdemo.z22.web.core.windows.net/)

---

**Congratulations!** You are now ready to start building Azure infrastructure with Bicep in VS Code.
