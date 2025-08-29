<h3 align="center">
  🤖 AI Commitizen Plugin
</h3>

<p align="center">
A <a href="https://github.com/commitizen-tools/commitizen"
target="_blank">Commitizen</a> plugin that leverages OpenAI's GPT-4o to automatically generate clear,<br />concise, and conventional commit messages based on your staged git changes.
</p>

<p align="center">
  <a href="https://pypi.org/project/cz-ai/">
    <img alt="npm version" src="https://img.shields.io/pypi/v/cz-ai?label=pypi"/>
  </a>
  <a title='License' href="https://github.com/watadarkstar/cz_ai/blob/master/LICENSE" height="18">
    <img src='https://img.shields.io/badge/license-MIT-blue.svg' />
  </a>
</p>

<p align="center">
  <a href="https://x.com/icookandcode" target="_blank">Need help building your AI tool? Connect with Adrian on X 🚀 </a>
</p>

## Features

- Analyzes your staged diffs using OpenAI GPT-4o
- Generates commit messages that follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
- Suggests high-quality messages instantly to save time
- Seamlessly integrates with existing Commitizen workflows
- Choose your preferred OpenAI model (gpt-4o-mini, gpt-4o, etc.)

## Prerequisites

- Python 3.x
- Install [commitizen](https://commitizen-tools.github.io/commitizen/#installation)

## Install

```bash
pip install cz-ai
```

## Usage

```bash
cz --name cz_ai commit
```

## Terminal Alias

To make it persistent across sessions, add this line to your `~/.bashrc` or
`~/.bash_profile` or `/.config/fish/config.fish` or `~/.zshrc` (depending on your setup):

```bash
alias gai='cz --name cz_ai commit'
```

## Development

Install the plugin locally:

```bash
pip install -e .
```

Then check that cz recognizes the plugin:

```bash
cz ls
```

It should appear as `cz_ai`

Then run this command to test it:

```bash
cz commit
```

## Build

```bash
uv build
```

## Upload to pypi.org

```bash
twine upload dist/*
```

## Author

Adrian C ([watadarkstar](https://github.com/watadarkstar/))

## Credits

Generated using this template: https://github.com/commitizen-tools/commitizen_cz_template

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute it as needed.

---

<div align="center">

**Ready to build your AI tool?**

⭐ **Star this repo** • 💬 **[Contact Adrian to Build It](https://x.com/icookandcode)**

_Built with ❤️ by [Adrian](https://x.com/icookandcode)_

</div>

---

**Keywords:** react-native, react, ai, tool, commits, aicommits, python, commitizen
