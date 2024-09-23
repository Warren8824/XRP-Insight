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
    - [Code Formatting and Linting](#code-formatting-and-linting)
    - [Commit Your Changes](#commit-your-changes)
    - [Push to GitHub](#push-to-github)
    - [Submit a Pull Request](#submit-a-pull-request)
3. [Contributing to Issues](#contributing-to-issues)
4. [Style Guide](#style-guide)
5. [Resources](#resources)
6. [Roadmap](#roadmap)

## Code of Conduct
We ask that all contributors adhere to our project's [Code of Conduct](../CODE_OF_CONDUCT.md). It’s important to respect others, stay positive, and foster a collaborative and welcoming environment.

## How to Contribute

### 1. Fork the Repository
Click the "Fork" button at the top of the repository page to create a copy of the repository under your GitHub account.

### 2. Clone the Fork
Clone your fork to your local machine by running the following command:
```bash
git clone https://github.com/your-username/your-forked-repo.git
```

### 3. Create a Branch
To make changes, create a new branch in your local repository. Choose a branch name that reflects your changes (e.g., feature-analysis, bugfix-issue123): `git checkout -b feature-name`

### 4. Make Your Changes
- Make your changes in the project.
- Ensure your code adheres to the Style Guide and passes Black checks (details below).
- Make sure your changes do not break any existing functionality. Running tests is always a good idea.

### 5. Code Formatting and Linting
To maintain code consistency, we use Black for code formatting. Before committing your code, please follow these steps to ensure your code adheres to the project standards:

- Run Black: This will automatically format your code. `black .`

Our GitHub Actions workflow will also automatically run these tools on each pull request, but it's best to check locally before submitting your changes.

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

## Contributing to Issues
We use GitHub Issues to track bugs, feature requests, and tasks. If you'd like to contribute, follow these steps:

1. Browse the Issues section to find open issues.
2. Comment on the issue you’d like to work on to let others know you're working on it.
3. If you don't find an existing issue for what you’re working on, feel free to open a new issue.

### Creating an Issue
When reporting bugs or suggesting features, please be as descriptive as possible:

- Bug Reports: Include steps to reproduce the problem, any error messages, and the environment (e.g., OS, Python version).
- Feature Requests: Clearly explain the proposed feature and its benefit to the project.

## Style Guide
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
