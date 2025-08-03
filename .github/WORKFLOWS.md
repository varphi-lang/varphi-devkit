# GitHub Actions Workflows

This repository uses GitHub Actions for continuous integration and deployment. Here's an overview of the configured workflows:

## CI/CD Workflows

### 1. CI (`ci.yml`)
**Triggers**: Push to main/master, Pull Requests
- **Testing**: Runs pytest across Python 3.10, 3.11, and 3.12
- **Linting**: Runs pylint on source code and tests
- **Caching**: Uses Poetry dependency caching for faster builds
- **Coverage**: Uploads coverage reports to Codecov

### 2. Release (`release.yml`)
**Triggers**: Push to main/master branch
- **Semantic Release**: Automatically creates releases based on conventional commits
- **Testing & Linting**: Ensures code quality before release
- **Package Building**: Creates distribution packages
- **PyPI Publishing**: Publishes to PyPI (requires configuration)
- **GitHub Releases**: Creates GitHub releases with artifacts

### 3. Manual Release (`manual-release.yml`)
**Triggers**: Manual workflow dispatch
- **Version Control**: Allows manual version bumping (patch/minor/major)
- **Dry Run**: Option to test release process without publishing
- **Override**: Can force specific version bumps

### 4. Code Quality (`code-quality.yml`)
**Triggers**: Push to main/master, Pull Requests
- **Coverage**: Detailed test coverage reporting
- **Security**: Bandit security analysis
- **Code Style**: Black formatting check
- **Import Sorting**: isort import organization check
- **Type Checking**: mypy static type analysis

### 5. PR Title Check (`pr-title-check.yml`)
**Triggers**: Pull Request events
- **Conventional Commits**: Ensures PR titles follow conventional commit format
- **Semantic Release**: Required for automatic version detection

## Dependencies Management

### Dependabot (`dependabot.yml`)
- **Python Dependencies**: Weekly updates for Poetry dependencies
- **GitHub Actions**: Weekly updates for workflow actions
- **Auto-assignment**: Assigns maintainers to dependency PRs

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for semantic versioning:

- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `perf:` - Performance improvements (patch version bump)
- `BREAKING CHANGE:` - Breaking changes (major version bump)
- `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `test:` - No version bump

## Setup Requirements

### For PyPI Publishing
1. Enable trusted publishing in PyPI project settings, or
2. Add `PYPI_API_TOKEN` to repository secrets

### For Full Functionality
- Repository must have write permissions for GitHub Actions
- Codecov integration (optional, for coverage reports)
- Maintain team/user assignment in dependabot.yml

## Local Development
To run the same checks locally:

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest tests/ -v

# Run linting
poetry run pylint src/varphi_devkit/

# Run with coverage
poetry run pytest tests/ --cov=src/varphi_devkit --cov-report=term-missing

# Check formatting (if added to dev dependencies)
poetry run black --check src/ tests/
poetry run isort --check-only src/ tests/
```

## Workflow Status
- ✅ CI: Tests and linting on every PR
- ✅ Release: Automatic releases on main branch
- ✅ Code Quality: Comprehensive quality checks
- ✅ Security: Automated security scanning
- ✅ Dependencies: Automated dependency updates