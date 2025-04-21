# Contributing to Offline Transcriber

Thank you for considering contributing to Offline Transcriber! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/offline-transcriber.git
   cd offline-transcriber
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   # or
   pip install -r requirements.txt
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
2. Make your changes
3. Format and lint your code:
   ```bash
   black src tests
   isort src tests
   flake8 src tests
   ```
4. Run tests:
   ```bash
   pytest
   ```
5. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
6. Push your branch:
   ```bash
   git push origin feature-name
   ```
7. Open a Pull Request

## Code Style

We follow the [Black](https://github.com/psf/black) code style. Please ensure your code is formatted with Black before submitting a PR.

Additionally:
- Use type hints where possible
- Write docstrings in the Google style format
- Keep lines under 100 characters
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions

## Testing

All new features should include tests. We use pytest for testing.

Run the tests with:
```bash
pytest
```

## Pull Request Process

1. Ensure your code is properly formatted and all tests pass
2. Update documentation if necessary
3. The PR should work for Python 3.8 and above
4. Include a clear description of the changes in your PR
5. Link any related issues

## Adding New Features

When adding new features, please consider:

1. Backward compatibility
2. Performance implications
3. Documentation updates
4. Test coverage

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 