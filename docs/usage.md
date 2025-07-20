# Usage Instructions for FastAPI Kickstart Toolkit

## Overview
The FastAPI Kickstart Toolkit is designed to streamline the development process for FastAPI applications by providing a set of tools that address common pain points. This document outlines how to use the toolkit effectively.

## Installation
To install the FastAPI Kickstart Toolkit, use pip:

```bash
pip install fastapi-kickstart
```

## Commands

### 1. Initialize a New Project
To create a new FastAPI project scaffold, run:

```bash
fastapi-kickstart init <project_name>
```

This command generates a complete project structure with sensible defaults, including example modules and working imports.

### 2. Check Environment
To check for missing dependencies and common configuration issues, use:

```bash
fastapi-kickstart env-check
```

This command scans your environment and reports any problems, offering to install missing packages if necessary.

### 3. Add Error Middleware
To enhance your FastAPI application with robust error handling, run:

```bash
fastapi-kickstart add-error-middleware
```

This command installs customizable error middleware that provides consistent and user-friendly error responses across your application.

### 4. Set Up Async Testing
To quickly set up an async testing environment with example tests, execute:

```bash
fastapi-kickstart test-init
```

This command configures your project for async testing, providing a framework to write and run tests efficiently.

### 5. Generate Onboarding Report
To create a comprehensive onboarding report for your project, use:

```bash
fastapi-kickstart generate-report
```

This command generates a markdown file summarizing project information, routes, dependencies, and potential issues.

## Example Usage
Here’s a quick example of how to use the toolkit:

```bash
# Create a new FastAPI project
fastapi-kickstart init myproject

# Navigate into the project directory
cd myproject

# Check for environment issues
fastapi-kickstart env-check

# Add error handling middleware
fastapi-kickstart add-error-middleware

# Set up async testing
fastapi-kickstart test-init

# Generate an onboarding report
fastapi-kickstart generate-report
```

## Conclusion
The FastAPI Kickstart Toolkit is designed to simplify the development process for FastAPI applications. By using the commands outlined in this document, you can quickly set up a new project, manage dependencies, enhance error handling, and streamline testing. Happy coding!