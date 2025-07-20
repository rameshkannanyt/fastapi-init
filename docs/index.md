# FastAPI Kickstart Toolkit Documentation

## Overview

The **FastAPI Kickstart Toolkit** is designed to streamline the development process for FastAPI applications. This toolkit provides a comprehensive set of tools to help developers quickly scaffold projects, manage dependencies, analyze code for async pitfalls, and enhance error handling.

## Key Features

- **Project Scaffolding**: Quickly create a best-practice FastAPI layout with sensible folders, example modules, and working imports.
- **Automated Dependency Checker**: Scan for problems with `pip`, `poetry`, or missing required packages. Warn users and optionally install what’s missing.
- **Async/Safety Analyzer**: Detect blocking functions or sync code in async endpoints. Warn or offer code suggestions.
- **Plug-and-Play Error Middleware**: Add one import that provides robust, pretty, and customizable error responses universally.
- **Test Booster**: Set up async test harness and example tests instantly—no boilerplate required.
- **Onboarding Report**: Generate a single readable onboarding markdown file with all routes, project info, and possible issues.

## Installation

To install the FastAPI Kickstart Toolkit, use pip:

```bash
pip install fastapi-kickstart
```

## Usage

### Initialize a New Project

To create a new FastAPI project scaffold, run:

```bash
fastapi-kickstart init myproject
```

This command will generate a working FastAPI scaffold along with a README file.

### Check Environment

To check for any missing dependencies and fix common problems, execute:

```bash
fastapi-kickstart env-check
```

### Add Error Middleware

To install robust error handling with one command, use:

```bash
fastapi-kickstart add-error-middleware
```

### Set Up Testing

To set up async test support and an example test suite, run:

```bash
fastapi-kickstart test-init
```

## Contributing

Contributions to the FastAPI Kickstart Toolkit are welcome! Please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.