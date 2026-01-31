---
description: Setup the Flutter and Firebase development environment on macOS
---

1. Check if Homebrew is installed
```bash
which brew
```

2. Install Flutter SDK
// turbo
```bash
brew install --cask flutter
```

3. Install Firebase CLI
// turbo
```bash
curl -sL https://firebase.tools | bash
```

4. Verify Installations
```bash
flutter doctor -v
firebase --version
```

5. Enable Flutter Web (Optional but good for quick testing)
```bash
flutter config --enable-web
```
