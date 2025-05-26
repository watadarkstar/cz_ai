![PyPI](https://img.shields.io/pypi/v/cz-ai?label=pypi)

# 🤖 AI Commitizen Plugin

A [Commitizen](https://github.com/commitizen-tools/commitizen) plugin that leverages OpenAI's GPT-4o to automatically generate clear, concise, and conventional commit messages based on your staged git changes.

## ✨ Features

- 🔍 Analyzes your staged diffs using OpenAI GPT-4o
- 🧠 Generates commit messages that follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- 💬 Suggests high-quality messages instantly to save time
- 🛠️ Seamlessly integrates with existing Commitizen workflows

## 🚀 Ideal For

- Developers who want to maintain a consistent and meaningful commit history
- Teams adopting conventional commits without manual formatting
- Projects aiming for automated changelog generation and semantic versioning

## Install

```
pip install cz-ai
```

## Usage

```
cz --name cz_ai commit
```

## Development

Install the plugin locally:

```
pip install -e .
```

Then check that cz recognizes the plugin:

```
cz ls
```

It should appear as `cz_ai`

Then run this command to test it:

```
cz commit
```

## Build

```
python3 -m build
```

## Upload to pypi.org

```
twine upload dist/*
```

## Author

Adrian C (author@commitizen)

## Credits

Generated using this template: https://github.com/commitizen-tools/commitizen_cz_template

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute it as needed.
