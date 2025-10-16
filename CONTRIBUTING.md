# Contributing to Android AI Assistant

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code Style

### Kotlin Code Style
- Follow the [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use meaningful variable and function names
- Add comments for complex logic

### Compose Guidelines
- Keep composables small and focused
- Use `remember` for state that shouldn't cause recomposition
- Prefer `LaunchedEffect` for side effects

### Architecture
- Follow MVVM pattern
- Keep business logic in ViewModels
- Use Repository for data operations
- Models should be simple data classes

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add dark mode support

- Implement dark color scheme
- Add theme toggle in settings
- Update documentation

Fixes #123
```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the BUILD.md if you change build process
3. Ensure all tests pass
4. Ensure code follows the style guidelines
5. Get approval from maintainers

## Bug Reports

Create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Device and Android version

## Feature Requests

Create an issue with:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
