# Contributing to XRP-Insight

🎉 **Thank you for your interest in contributing to XRP-Insight!** 🎉  
We welcome all contributions and are excited to work together to improve the project. This document outlines the guidelines and steps to help you contribute.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
    - [Fork the Repository](#fork-the-repository)
    - [Clone the Fork](#clone-the-fork)
    - [Create a Branch](#create-a-branch)
    - [Make Your Changes](#make-your-changes)
    - [Code Formatting](#code-formatting)
    - [Commit Your Changes](#commit-your-changes)
    - [Push to GitHub](#push-to-github)
    - [Submit a Pull Request](#submit-a-pull-request)
    - [Configure GitHub Secrets for CI Workflow](#configure-github-secrets-for-ci-workflow)
3. [Contributing to Issues](#contributing-to-issues)
4. [Style Guide](#style-guide)
5. [Resources](#resources)
6. [Roadmap](#roadmap)

## Code of Conduct
We ask that all contributors adhere to our project's [Code of Conduct](CODE_OF_CONDUCT.md). It’s important to respect others, stay positive, and foster a collaborative and welcoming environment.

## How to Contribute

### 1. Fork the Repository
Click the "Fork" button at the top of the repository page to create a copy of the repository under your GitHub account.

### 2. Clone the Fork
Clone your fork to your local machine by running the following command:
```bash
git clone https://github.com/Warren8824/XRP-Insight.git
```

### 3. Create a Branch
To make changes, create a new branch in your local repository. Choose a branch name that reflects your changes (e.g., feature-analysis, bugfix-issue123): `git checkout -b feature-name`

### 4. Make Your Changes
Make your changes in the project.
Ensure your code adheres to the Style Guide and passes Black checks (details below).
Make sure your changes do not break any existing functionality. Running tests is always a good idea.

### 5. Code Formatting
To maintain code consistency, we use Black for code formatting. Before committing your code, please follow this step to ensure your code adheres to the project standards:

- Run Black: This will automatically format your code. `black .`

Our GitHub Actions workflow will also automatically run this tool on each pull request, but it's best to check locally before submitting your changes.

You can install this tool using pip: `pip install black`

### 6. Commit Your Changes
After making your changes, stage and commit them with a descriptive message: 

```
git add .
git commit -m "Add feature XYZ"
```

### 7. Push to GitHub
Push your changes to your GitHub repository: `git push origin feature-name`

### 8. Submit a Pull Request
Go to the original repository on GitHub and create a Pull Request (PR) from your branch:

- Title: Clear and concise (e.g., "Add feature XYZ for data analysis").
- Description: Explain the purpose of your changes and any related issues. Provide context, screenshots, or examples if possible.
- Your PR will be reviewed, and you may be asked to make adjustments before it is merged.

### 9. Configure GitHub Secrets for CI Workflow

Our project uses GitHub Actions for Continuous Integration (CI) to run tests and ensure that all changes pass before merging. In order to successfully run the CI workflow, certain environment variables (such as database credentials and API keys) must be set up as **GitHub Secrets**.

If you want to run the CI tests in your own fork or clone of this repository, you will need to set up the required secrets. Here’s what you need to do:

### Required Secrets:
1. **Database Secrets:**
- DATABASE_URL: The full connection string for the test database.
- DATABASE_NAME: The name of the test database.
- DATABASE_PASSWORD: The password for the test database.

2. **API Keys:**
- COINAPI_API_KEY: Your API key for the CoinAPI service.
- COINGECKO_API_KEY: Your API key for the CoinGecko service.

Steps to Set Up GitHub Secrets:

1. Navigate to your repository on GitHub.

2. Go to Settings → Secrets and variables → Actions.

3. Click New repository secret.

4. Add the following secrets, one by one:

- `DATABASE_URL`
- `DATABASE_NAME`
- `DATABASE_PASSWORD`
- `COINAPI_API_KEY`
- `COINGECKO_API_KEY`

### Example Secrets Configuration:


```
DATABASE_URL=postgres://user:password@localhost:5432/test_db
DATABASE_NAME=test_db
DATABASE_PASSWORD=your_password_here
COINAPI_API_KEY=your_coinapi_key_here
COINGECKO_API_KEY=your_coingecko_key_here
```

Once these secrets are configured in your forked repository, the CI workflow should pass as expected when you push changes or create pull requests.

### Contributing to Issues

We use GitHub Issues to track bugs, feature requests, and tasks. If you'd like to contribute, follow these steps:

1. Browse the Issues section to find open issues.
2. Comment on the issue you’d like to work on to let others know you're working on it.
3. If you don't find an existing issue for what you’re working on, feel free to open a new issue.

### Creating an Issue
When reporting bugs or suggesting features, please be as descriptive as possible:

- Bug Reports: Include steps to reproduce the problem, any error messages, and the environment (e.g., OS, Python version).
- Feature Requests: Clearly explain the proposed feature and its benefit to the project.

### Style Guide

To ensure consistency and readability, please follow these guidelines:

- Code Formatting: We use Black for consistent formatting across the project. Run black . before committing to automatically format your code.
- Commit Messages: Write clear, concise commit messages. Use imperative mood (e.g., "Fix bug in data parsing").
- Documentation: For any new features, add relevant documentation in the code and, if necessary, update the project documentation.

## Resources
Here are some resources that might be helpful when contributing:

- **Python Style Guide**: [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- **GitHub Flow**: [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- **How to Write a Good Commit Message**: [Commit Message Guide](https://chris.beams.io/posts/git-commit/)
- **Black**: [Black Formatter Documentation](https://black.readthedocs.io/en/stable/)
- **Flake8**: [Flake8 Documentation](https://flake8.pycqa.org/en/latest/)

---

## Roadmap
Check out the project's **Roadmap** to see the planned features and phases of development. You can find the roadmap [here](ROADMAP.md).

Feel free to pick up tasks from Phase 1 to get started. Contributions are welcome at every step!





