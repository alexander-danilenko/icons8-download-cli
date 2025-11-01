# 🚀 Icons8 Download CLI

A powerful command-line tool for efficiently downloading icons from [Icons8.com](https://icons8.com). Filter by style, download in parallel, and organize your icon collection with ease.

## ✨ Features

- 🎨 **Style Filtering**: Download icons filtered by specific styles
- 📥 **Parallel Downloads**: Fast downloads with configurable worker threads for maximum efficiency
- 💾 **Smart Caching**: Intelligent response caching to minimize API calls and speed up subsequent runs
- 📂 **Auto Directory Detection**: Automatically detects and uses your system's Downloads folder
- 🎯 **Multiple Sizes**: Choose from various icon sizes (24px, 48px, 96px, 192px, 384px, or 512px)
- 📊 **Progress Tracking**: Real-time progress bars and comprehensive download summaries
- 📝 **Detailed Logging**: Automatic log file generation for each download session for troubleshooting
- 🛡️ **Filename Conflict Resolution**: Automatically handles duplicate filenames to prevent overwrites
- 🖼️ **PNG Format**: Downloads PNG format icons (free format available on Icons8)

> [!IMPORTANT]
> CSV format is not supported. Only PNG format downloads are available.

## 📋 Requirements

- Python 3.10 or higher
- `uv` package manager ([Installation guide](https://github.com/astral-sh/uv))

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/alexander-danilenko/icons8-download-cli.git
cd icons8-download-cli
```

2. Install dependencies:
```bash
uv sync
```

## 🎯 Usage

### 📥 Basic Usage

Download icons filtered by a specific style:

```bash
uv run icons8-download --style ios
```

### ⚙️ Command Options

The tool provides several options to customize your download experience:

|               Option | Short | Description                                                               |
| -------------------: | ----- | ------------------------------------------------------------------------- |
| `--target-directory` | `-d`  | Target directory for downloaded icons (defaults to your Downloads folder) |
|             `--size` | `-s`  | Icon size: `24`, `48`, `96`, `192`, `384`, or `512` (default: `512`)      |
|            `--style` | `-S`  | Icon style filter (required)                                              |
|          `--workers` | `-w`  | Number of parallel download threads (default: `10`)                       |
|         `--no-cache` | `-C`  | Disable response caching                                                  |
|             `--help` |       | Show help message and exit                                                |

### 🔍 Finding Style Values

You can find style values directly from the Icons8 website. When browsing icons by style on [Icons8.com](https://icons8.com), the style value is embedded in the URL:

- **URL format**: `https://icons8.com/icons/all--style-<STYLE_VALUE>`
- **Example**: `https://icons8.com/icons/all--style-fluency` → use `fluency` as the style value

Alternatively, you can browse the complete list of available styles in the [Style values reference](#style-values-reference) section below.

### ⬇️ Downloading All Styles

The [styles.json](./data/styles.json) file contains all available styles. To download all styles automatically, use one of the following commands:

**Linux/macOS (Bash):**

```bash
cat ./data/styles.json | jq -r '.styles[] | "\(.id)|\(.label)"' | while IFS='|' read -r id label; do uv run icons8-download --style "$id" --target-directory "./data/icons/$label"; done
```

**Windows (PowerShell):**

```powershell
Get-Content ./data/styles.json | ConvertFrom-Json | Select-Object -ExpandProperty styles | ForEach-Object { uv run icons8-download --style $_.id --target-directory ".\data\icons\$($_.label)" }
```

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, new features, documentation improvements, or suggestions, we appreciate your help. Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- [Icons8](https://icons8.com) for providing the API and icons
- ❤️ All contributors who help improve this project!

## 💬 Support

If you encounter any issues, have questions, or would like to request a feature, please [open an issue](https://github.com/alexander-danilenko/icons8-download-cli/issues) on GitHub.
