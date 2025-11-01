# Icons8 Download CLI

A powerful command-line tool for efficiently downloading icons from [Icons8.com](https://icons8.com). Filter by style, download in parallel, and organize your icon collection with ease.

## Features

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

## Requirements

- Python 3.10 or higher
- `uv` package manager ([Installation guide](https://github.com/astral-sh/uv))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alexander-danilenko/icons8-download-cli.git
cd icons8-download-cli
```

2. Install dependencies:
```bash
uv sync
```

## Usage

### Basic Usage

Download icons filtered by a specific style:

```bash
uv run download --style ios
```

### Command Options

The tool provides several options to customize your download experience:

|               Option | Short | Description                                                               |
| -------------------: | ----- | ------------------------------------------------------------------------- |
| `--target-directory` | `-d`  | Target directory for downloaded icons (defaults to your Downloads folder) |
|             `--size` | `-s`  | Icon size: `24`, `48`, `96`, `192`, `384`, or `512` (default: `512`)      |
|            `--style` | `-S`  | Icon style filter (required)                                              |
|          `--workers` | `-w`  | Number of parallel download threads (default: `10`)                       |
|         `--no-cache` | `-C`  | Disable response caching                                                  |
|             `--help` |       | Show help message and exit                                                |

### Finding Style Values

You can find style values directly from the Icons8 website. When browsing icons by style on [Icons8.com](https://icons8.com), the style value is embedded in the URL:

- **URL format**: `https://icons8.com/icons/all--style-<STYLE_VALUE>`
- **Example**: `https://icons8.com/icons/all--style-fluency` → use `fluency` as the style value

Alternatively, you can browse the complete list of available styles in the [Style values reference](#style-values-reference) section below.

### Downloading All Styles

The [styles.json](./data/styles.json) file contains all available styles. To download all styles automatically, use one of the following commands:

**Linux/macOS (Bash):**

```bash
cat ./data/styles.json | jq -r '.styles[] | "\(.id)|\(.label)"' | while IFS='|' read -r id label; do uv run download --style "$id" --target-directory "./data/icons/$label"; done
```

**Windows (PowerShell):**

```powershell
Get-Content ./data/styles.json | ConvertFrom-Json | Select-Object -ExpandProperty styles | ForEach-Object { uv run download --style $_.id --target-directory ".\data\icons\$($_.label)" }
```

### Style Values Reference

| Description                | Image                                                                                                                                   | Style value                  | 🔗                                                                   |
| :------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------- | :------------------------------------------------------------------ |
| 3D Fluency                 | <img height="32" src="https://img-main.icons8.com/3d-fluency/48/home.png" alt="3D Fluency" />                                           | `3d-fluency`                 | [🔗](https://icons8.com/icons/all--style-3d-fluency)                 |
| 3D Plastilina              | <img height="32" src="https://img-main.icons8.com/3d-plastilina/48/home.png" alt="3D Plastilina" />                                     | `3d-plastilina`              | [🔗](https://icons8.com/icons/all--style-3d-plastilina)              |
| Apple SF Black             | <img height="32" src="https://img-main.icons8.com/sf-black/2x/home.png" alt="Apple SF Black" />                                         | `sf-black`                   | [🔗](https://icons8.com/icons/all--style-sf-black)                   |
| Apple SF Black Filled      | <img height="32" src="https://img-main.icons8.com/sf-black-filled/2x/home.png" alt="Apple SF Black Filled" />                           | `sf-black-filled`            | [🔗](https://icons8.com/icons/all--style-sf-black-filled)            |
| Apple SF Regular           | <img height="32" src="https://img-main.icons8.com/sf-regular/2x/home.png" alt="Apple SF Regular" />                                     | `sf-regular`                 | [🔗](https://icons8.com/icons/all--style-sf-regular)                 |
| Apple SF Regular Filled    | <img height="32" src="https://img-main.icons8.com/sf-regular-filled/2x/home.png" alt="Apple SF Regular Filled" />                       | `sf-regular-filled`          | [🔗](https://icons8.com/icons/all--style-sf-regular-filled)          |
| Apple SF Ultralight        | <img height="32" src="https://img-main.icons8.com/sf-ultralight/2x/home.png" alt="Apple SF Ultralight" />                               | `sf-ultralight`              | [🔗](https://icons8.com/icons/all--style-sf-ultralight)              |
| Apple SF Ultralight Filled | <img height="32" src="https://img-main.icons8.com/sf-ultralight-filled/2x/home.png" alt="Apple SF Ultralight Filled" />                 | `sf-ultralight-filled`       | [🔗](https://icons8.com/icons/all--style-sf-ultralight-filled)       |
| Arcade                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/1713fb15-eaad-40ae-ba1c-d8f02c451512.png" alt="Arcade" />                 | `arcade`                     | [🔗](https://icons8.com/icons/all--style-arcade)                     |
| Avantgarde                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/9397d03a-3788-4e9f-9c35-cc4d1fc72a6d.png" alt="Avantgarde" />             | `avantgarde`                 | [🔗](https://icons8.com/icons/all--style-avantgarde)                 |
| Badges                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/5dd9d34a-7e38-4d86-aa1c-0278a848d142.png" alt="Badges" />                 | `badges`                     | [🔗](https://icons8.com/icons/all--style-badges)                     |
| Blue UI                    | <img height="32" src="https://img-main.icons8.com/ultraviolet/2x/home.png" alt="Blue UI" />                                             | `ultraviolet`                | [🔗](https://icons8.com/icons/all--style-ultraviolet)                |
| Bubbles                    | <img height="32" src="https://img-main.icons8.com/bubbles/2x/home.png" alt="Bubbles" />                                                 | `bubbles`                    | [🔗](https://icons8.com/icons/all--style-bubbles)                    |
| Cloud                      | <img height="32" src="https://img-main.icons8.com/clouds/2x/home.png" alt="Cloud" />                                                    | `clouds`                     | [🔗](https://icons8.com/icons/all--style-clouds)                     |
| Color                      | <img height="32" src="https://img-main.icons8.com/color/2x/home.png" alt="Color" />                                                     | `color`                      | [🔗](https://icons8.com/icons/all--style-color)                      |
| Color Glass                | <img height="32" src="https://img-main.icons8.com/color-glass/2x/home.png" alt="Color Glass" />                                         | `clr-gls`                    | [🔗](https://icons8.com/icons/all--style-clr-gls)                    |
| Color Hand Drawn           | <img height="32" src="https://img-main.icons8.com/plasticine/2x/home.png" alt="Color Hand Drawn" />                                     | `plasticine`                 | [🔗](https://icons8.com/icons/all--style-plasticine)                 |
| Color Pixels               | <img height="32" src="https://maxcdn.icons8.com/style-preview/6bebe548-5f05-4080-9e9d-836ac8d2043e.png" alt="Color Pixels" />           | `color-pixels`               | [🔗](https://icons8.com/icons/all--style-color-pixels)               |
| Comic                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/7df92464-fc7d-4d6f-9e49-de057ec8707d.png" alt="Comic" />                  | `comic`                      | [🔗](https://icons8.com/icons/all--style-comic)                      |
| Connect                    | <img height="32" src="https://maxcdn.icons8.com/style-preview/0db682f1-dc0f-4ae4-a737-1b09b07b6a9f.png" alt="Connect" />                | `connect`                    | [🔗](https://icons8.com/icons/all--style-connect)                    |
| Connect Color              | <img height="32" src="https://maxcdn.icons8.com/style-preview/d5751e61-0b6c-4d3c-a647-4151dfae6f12.png" alt="Connect Color" />          | `connect-color`              | [🔗](https://icons8.com/icons/all--style-connect-color)              |
| Cute Clipart               | <img height="32" src="https://img-main.icons8.com/cute-clipart/2x/home.png" alt="Cute Clipart" />                                       | `cool`                       | [🔗](https://icons8.com/icons/all--style-cool)                       |
| Cute Color                 | <img height="32" src="https://img-main.icons8.com/dusk/2x/home.png" alt="Cute Color" />                                                 | `dusk`                       | [🔗](https://icons8.com/icons/all--style-dusk)                       |
| Cute Outline               | <img height="32" src="https://img-main.icons8.com/wired/2x/home.png" alt="Cute Outline" />                                              | `Dusk_Wired`                 | [🔗](https://icons8.com/icons/all--style-Dusk_Wired)                 |
| Deco Color                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/d1155f3e-5ed4-49cb-8403-1d1281b16348.png" alt="Deco Color" />             | `deco-color`                 | [🔗](https://icons8.com/icons/all--style-deco-color)                 |
| Deco Duotone               | <img height="32" src="https://maxcdn.icons8.com/style-preview/c4a9262f-a952-4ea4-ae53-8a5dd4b98442.png" alt="Deco Duotone" />           | `deco`                       | [🔗](https://icons8.com/icons/all--style-deco)                       |
| Deco Glyph                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/0f832638-2343-48b2-b201-e5471ef6dda7.png" alt="Deco Glyph" />             | `deco-glyph`                 | [🔗](https://icons8.com/icons/all--style-deco-glyph)                 |
| Doodle                     | <img height="32" src="https://img-main.icons8.com/doodle/2x/home.png" alt="Doodle" />                                                   | `doodle`                     | [🔗](https://icons8.com/icons/all--style-doodle)                     |
| Doodle Line                | <img height="32" src="https://maxcdn.icons8.com/style-preview/15888592-5f4c-4de2-920e-639297819b56.png" alt="Doodle Line" />            | `doodle-line`                | [🔗](https://icons8.com/icons/all--style-doodle-line)                |
| Dotted                     | <img height="32" src="https://img-main.icons8.com/dotty/2x/home.png" alt="Dotted" />                                                    | `dotty`                      | [🔗](https://icons8.com/icons/all--style-dotty)                      |
| Emoji                      | <img height="32" src="https://img.icons8.com/emoji/48/house-emoji.png" alt="Emoji" />                                                   | `emoji`                      | [🔗](https://icons8.com/icons/all--style-emoji)                      |
| Forma Bold                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/96b4f6c2-084f-48e5-b3e1-17e29ccf7c8a.png" alt="Forma Bold" />             | `forma-bold`                 | [🔗](https://icons8.com/icons/all--style-forma-bold)                 |
| Forma Bold Filled          | <img height="32" src="https://maxcdn.icons8.com/style-preview/faf1452f-9d4f-46f5-9a0e-c59b8ebea994.png" alt="Forma Bold Filled" />      | `forma-bold-filled`          | [🔗](https://icons8.com/icons/all--style-forma-bold-filled)          |
| Forma Bold Filled Sharp    | <img height="32" src="https://api-img.icons8.com/forma-bold-filled-sharp/home.svg?fromSite=true" alt="Forma Bold Filled Sharp" />       | `forma-bold-filled-sharp`    | [🔗](https://icons8.com/icons/all--style-forma-bold-filled-sharp)    |
| Forma Bold Sharp           | <img height="32" src="https://api-img.icons8.com/forma-bold-sharp/home.svg?fromSite=true" alt="Forma Bold Sharp" />                     | `forma-bold-sharp`           | [🔗](https://icons8.com/icons/all--style-forma-bold-sharp)           |
| Forma Light                | <img height="32" src="https://maxcdn.icons8.com/style-preview/a65b563c-87c4-4f44-a500-6776fd41f26b.png" alt="Forma Light" />            | `forma-light`                | [🔗](https://icons8.com/icons/all--style-forma-light)                |
| Forma Light Filled         | <img height="32" src="https://maxcdn.icons8.com/style-preview/5f94c5a4-1145-413a-8907-e0669dadfa07.png" alt="Forma Light Filled" />     | `forma-light-filled`         | [🔗](https://icons8.com/icons/all--style-forma-light-filled)         |
| Forma Light Filled Sharp   | <img height="32" src="https://api-img.icons8.com/forma-light-filled-sharp/home.svg?fromSite=true" alt="Forma Light Filled Sharp" />     | `forma-light-filled-sharp`   | [🔗](https://icons8.com/icons/all--style-forma-light-filled-sharp)   |
| Forma Light Sharp          | <img height="32" src="https://api-img.icons8.com/forma-light-sharp/home.svg?fromSite=true" alt="Forma Light Sharp" />                   | `forma-light-sharp`          | [🔗](https://icons8.com/icons/all--style-forma-light-sharp)          |
| Forma Regular              | <img height="32" src="https://maxcdn.icons8.com/style-preview/88a4d845-432b-4b98-b2fd-1eb025986e96.png" alt="Forma Regular" />          | `forma-regular`              | [🔗](https://icons8.com/icons/all--style-forma-regular)              |
| Forma Regular Filled       | <img height="32" src="https://maxcdn.icons8.com/style-preview/4528a81c-904f-4adf-89ca-bee6101e5012.png" alt="Forma Regular Filled" />   | `forma-regular-filled`       | [🔗](https://icons8.com/icons/all--style-forma-regular-filled)       |
| Forma Regular Filled Sharp | <img height="32" src="https://api-img.icons8.com/forma-regular-filled-sharp/home.svg?fromSite=true" alt="Forma Regular Filled Sharp" /> | `forma-regular-filled-sharp` | [🔗](https://icons8.com/icons/all--style-forma-regular-filled-sharp) |
| Forma Regular Sharp        | <img height="32" src="https://api-img.icons8.com/forma-regular-sharp/home.svg?fromSite=true" alt="Forma Regular Sharp" />               | `forma-regular-sharp`        | [🔗](https://icons8.com/icons/all--style-forma-regular-sharp)        |
| Forma Thin                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/8329df8f-8ca2-41d0-8474-cddebf60cd66.png" alt="Forma Thin" />             | `forma-thin`                 | [🔗](https://icons8.com/icons/all--style-forma-thin)                 |
| Forma Thin Filled          | <img height="32" src="https://maxcdn.icons8.com/style-preview/98c7be7f-cc7f-4a77-a241-0bde8eb26b0d.png" alt="Forma Thin Filled" />      | `forma-thin-filled`          | [🔗](https://icons8.com/icons/all--style-forma-thin-filled)          |
| Forma Thin Filled Sharp    | <img height="32" src="https://api-img.icons8.com/forma-thin-filled-sharp/home.svg?fromSite=true" alt="Forma Thin Filled Sharp" />       | `forma-thin-filled-sharp`    | [🔗](https://icons8.com/icons/all--style-forma-thin-filled-sharp)    |
| Forma Thin Sharp           | <img height="32" src="https://api-img.icons8.com/forma-thin-sharp/home.svg?fromSite=true" alt="Forma Thin Sharp" />                     | `forma-thin-sharp`           | [🔗](https://icons8.com/icons/all--style-forma-thin-sharp)           |
| Glassmorphism              | <img height="32" src="https://maxcdn.icons8.com/style-preview/6962fb7c-f28a-49ba-8ca6-d330692399af.png" alt="Glassmorphism" />          | `glassmorphism`              | [🔗](https://icons8.com/icons/all--style-glassmorphism)              |
| Glyph Neue                 | <img height="32" src="https://img-main.icons8.com/glyph-neue/2x/home.png" alt="Glyph Neue" />                                           | `glyph-neue`                 | [🔗](https://icons8.com/icons/all--style-glyph-neue)                 |
| Gradient                   | <img height="32" src="https://img-main.icons8.com/nolan/2x/home.png" alt="Gradient" />                                                  | `nolan`                      | [🔗](https://icons8.com/icons/all--style-nolan)                      |
| Handsy                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/c3539d25-5cc8-48fe-ba65-3a8a6ffed806.png" alt="Handsy" />                 | `hands`                      | [🔗](https://icons8.com/icons/all--style-hands)                      |
| Hatch                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/fb9a455a-4af0-4cda-8557-60bf198d1ae9.png" alt="Hatch" />                  | `hatch`                      | [🔗](https://icons8.com/icons/all--style-hatch)                      |
| Hieroglyphs                | <img height="32" src="https://maxcdn.icons8.com/style-preview/7200f7fb-e932-4eff-99fa-bbbfe951c3cf.png" alt="Hieroglyphs" />            | `hieroglyphs`                | [🔗](https://icons8.com/icons/all--style-hieroglyphs)                |
| Ice Cream                  | <img height="32" src="https://img-main.icons8.com/android/2x/home.png" alt="Ice Cream" />                                               | `android`                    | [🔗](https://icons8.com/icons/all--style-android)                    |
| Infographic                | <img height="32" src="https://img-main.icons8.com/flat-round/2x/home.png" alt="Infographic" />                                          | `flat_round`                 | [🔗](https://icons8.com/icons/all--style-flat_round)                 |
| Ink                        | <img height="32" src="https://maxcdn.icons8.com/style-preview/0a71bbbe-30d5-4f34-b02f-62ac9543b963.png" alt="Ink" />                    | `ink`                        | [🔗](https://icons8.com/icons/all--style-ink)                        |
| iOS 17 Filled              | <img height="32" src="https://img-main.icons8.com/ios-filled/2x/home.png" alt="iOS 17 Filled" />                                        | `ios_filled`                 | [🔗](https://icons8.com/icons/all--style-ios_filled)                 |
| iOS 17 Glyph               | <img height="32" src="https://img-main.icons8.com/ios-glyphs/2x/home.png" alt="iOS 17 Glyph" />                                         | `ios11`                      | [🔗](https://icons8.com/icons/all--style-ios11)                      |
| iOS 17 Outlined            | <img height="32" src="https://img-main.icons8.com/ios/2x/home.png" alt="iOS 17 Outlined" />                                             | `ios7`                       | [🔗](https://icons8.com/icons/all--style-ios7)                       |
| Isometric Color            | <img height="32" src="https://maxcdn.icons8.com/style-preview/c51f8561-afad-4d8e-9e8a-6ba62751fafb.png" alt="Isometric Color" />        | `isometric`                  | [🔗](https://icons8.com/icons/all--style-isometric)                  |
| Isometric Line             | <img height="32" src="https://maxcdn.icons8.com/style-preview/ad23fe3c-b838-4fcc-b0e7-1171d18ba344.png" alt="Isometric Line" />         | `isometric-line`             | [🔗](https://icons8.com/icons/all--style-isometric-line)             |
| Keek                       | <img height="32" src="https://maxcdn.icons8.com/style-preview/92121748-56b1-47b9-b453-6371470983fd.png" alt="Keek" />                   | `keek`                       | [🔗](https://icons8.com/icons/all--style-keek)                       |
| Laces                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/87c7322d-d556-4fc4-be17-e0953e9618a9.png" alt="Laces" />                  | `laces`                      | [🔗](https://icons8.com/icons/all--style-laces)                      |
| LED                        | <img height="32" src="https://maxcdn.icons8.com/style-preview/01b12524-65ff-4f33-a4a9-c8dbbba68990.png" alt="LED" />                    | `led`                        | [🔗](https://icons8.com/icons/all--style-led)                        |
| Liquid Glass               | <img height="32" src="https://maxcdn.icons8.com/style-preview/3e37121c-71a9-42b1-8cc7-a085b4bdf46f.png" alt="Liquid Glass" />           | `liquid-glass`               | [🔗](https://icons8.com/icons/all--style-liquid-glass)               |
| Liquid Glass Color         | <img height="32" src="https://maxcdn.icons8.com/style-preview/a5c392d2-b8b3-438b-82b8-9879d5d28165.png" alt="Liquid Glass Color" />     | `liquid-glass-color`         | [🔗](https://icons8.com/icons/all--style-liquid-glass-color)         |
| Lollipop                   | <img height="32" src="https://maxcdn.icons8.com/style-preview/a932e7d8-0b59-48fc-b00c-00482c1d5b6c.png" alt="Lollipop" />               | `lollipop`                   | [🔗](https://icons8.com/icons/all--style-lollipop)                   |
| Material Filled            | <img height="32" src="https://img-main.icons8.com/material/2x/home.png" alt="Material Filled" />                                        | `androidL`                   | [🔗](https://icons8.com/icons/all--style-androidL)                   |
| Material Outlined          | <img height="32" src="https://img-main.icons8.com/material-outlined/2x/home.png" alt="Material Outlined" />                             | `m_outlined`                 | [🔗](https://icons8.com/icons/all--style-m_outlined)                 |
| Material Rounded           | <img height="32" src="https://img-main.icons8.com/material-rounded/2x/home.png" alt="Material Rounded" />                               | `m_rounded`                  | [🔗](https://icons8.com/icons/all--style-m_rounded)                  |
| Material Sharp             | <img height="32" src="https://img-main.icons8.com/material-sharp/2x/home.png" alt="Material Sharp" />                                   | `m_sharp`                    | [🔗](https://icons8.com/icons/all--style-m_sharp)                    |
| Material Two Tone          | <img height="32" src="https://img-main.icons8.com/material-two-tone/2x/home.png" alt="Material Two Tone" />                             | `m_two_tone`                 | [🔗](https://icons8.com/icons/all--style-m_two_tone)                 |
| Matisse                    | <img height="32" src="https://maxcdn.icons8.com/style-preview/fbf30ff5-ebcb-4acb-8957-e38292cb44b2.png" alt="Matisse" />                | `matisse`                    | [🔗](https://icons8.com/icons/all--style-matisse)                    |
| Mini Stickers              | <img height="32" src="https://maxcdn.icons8.com/style-preview/c193394f-27aa-46f6-b324-fa3f97763442.png" alt="Mini Stickers" />          | `mini-stickers`              | [🔗](https://icons8.com/icons/all--style-mini-stickers)              |
| Neon                       | <img height="32" src="https://maxcdn.icons8.com/style-preview/f1024114-8072-4726-add2-20be4ba2ec4a.png" alt="Neon" />                   | `neon`                       | [🔗](https://icons8.com/icons/all--style-neon)                       |
| Office L                   | <img height="32" src="https://img-main.icons8.com/officel/2x/home.png" alt="Office L" />                                                | `office80`                   | [🔗](https://icons8.com/icons/all--style-office80)                   |
| Office M                   | <img height="32" src="https://img-main.icons8.com/office/2x/home.png" alt="Office M" />                                                 | `office40`                   | [🔗](https://icons8.com/icons/all--style-office40)                   |
| Office S                   | <img height="32" src="https://img-main.icons8.com/offices/2x/home.png" alt="Office S" />                                                | `office30`                   | [🔗](https://icons8.com/icons/all--style-office30)                   |
| Office XS                  | <img height="32" src="https://img-main.icons8.com/officexs/2x/home.png" alt="Office XS" />                                              | `office16`                   | [🔗](https://icons8.com/icons/all--style-office16)                   |
| Outline Hand Drawn         | <img height="32" src="https://img-main.icons8.com/carbon-copy/2x/home.png" alt="Outline Hand Drawn" />                                  | `carbon_copy`                | [🔗](https://icons8.com/icons/all--style-carbon_copy)                |
| Papercut                   | <img height="32" src="https://maxcdn.icons8.com/style-preview/f461d4e4-f062-447d-a839-26210c73233d.jpeg" alt="Papercut" />              | `papercut`                   | [🔗](https://icons8.com/icons/all--style-papercut)                   |
| Parakeet Color             | <img height="32" src="https://img-main.icons8.com/parakeet/2x/home.png" alt="Parakeet Color" />                                         | `parakeet`                   | [🔗](https://icons8.com/icons/all--style-parakeet)                   |
| Parakeet Line              | <img height="32" src="https://maxcdn.icons8.com/style-preview/bdb9a706-6e3c-440b-9698-1ecdb3bf0b71.png" alt="Parakeet Line" />          | `parakeet-line`              | [🔗](https://icons8.com/icons/all--style-parakeet-line)              |
| Pastel Color               | <img height="32" src="https://maxcdn.icons8.com/style-preview/6f473439-ab2b-4708-b1ea-e37b8153cf7e.png" alt="Pastel Color" />           | `cotton`                     | [🔗](https://icons8.com/icons/all--style-cotton)                     |
| Pastel Glyph               | <img height="32" src="https://maxcdn.icons8.com/style-preview/803f4221-cf38-4767-9632-333ec1bcfc48.png" alt="Pastel Glyph" />           | `pastel_glyph`               | [🔗](https://icons8.com/icons/all--style-pastel_glyph)               |
| Pieces                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/36fec220-7cc9-45eb-8540-e7665ad876d1.png" alt="Pieces" />                 | `pieces`                     | [🔗](https://icons8.com/icons/all--style-pieces)                     |
| Pin                        | <img height="32" src="https://maxcdn.icons8.com/style-preview/e62e1420-5e2d-40ea-8a58-56adb852edb1.png" alt="Pin" />                    | `pin`                        | [🔗](https://icons8.com/icons/all--style-pin)                        |
| Pixels                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/515d2d6d-7ac4-429c-9b84-6db7cb835a1a.png" alt="Pixels" />                 | `pixels`                     | [🔗](https://icons8.com/icons/all--style-pixels)                     |
| Plumpy                     | <img height="32" src="https://img-main.icons8.com/plumpy/2x/home.png" alt="Plumpy" />                                                   | `plumpy`                     | [🔗](https://icons8.com/icons/all--style-plumpy)                     |
| Poly                       | <img height="32" src="https://maxcdn.icons8.com/style-preview/6e98519d-40de-4463-b5ec-ab5211e79b89.png" alt="Poly" />                   | `poly`                       | [🔗](https://icons8.com/icons/all--style-poly)                       |
| Puffy Filled               | <img height="32" src="https://maxcdn.icons8.com/style-preview/ff652800-57a7-4fdb-85d6-9402fa325085.png" alt="Puffy Filled" />           | `puffy-filled`               | [🔗](https://icons8.com/icons/all--style-puffy-filled)               |
| Puffy Outline              | <img height="32" src="https://maxcdn.icons8.com/style-preview/c659470a-c48d-43bf-ae05-a73b1518af33.png" alt="Puffy Outline" />          | `puffy`                      | [🔗](https://icons8.com/icons/all--style-puffy)                      |
| Pulsar Color               | <img height="32" src="https://maxcdn.icons8.com/style-preview/3057d680-3365-49e4-a86e-00c04a55f91c.png" alt="Pulsar Color" />           | `pulsar-color`               | [🔗](https://icons8.com/icons/all--style-pulsar-color)               |
| Pulsar Gradient            | <img height="32" src="https://maxcdn.icons8.com/style-preview/929b9110-92c3-4cda-bce8-1e8c2b2cc432.png" alt="Pulsar Gradient" />        | `pulsar-gradient`            | [🔗](https://icons8.com/icons/all--style-pulsar-gradient)            |
| Pulsar Line                | <img height="32" src="https://maxcdn.icons8.com/style-preview/419a0680-736f-4290-9bc8-363b8faae7f6.png" alt="Pulsar Line" />            | `pulsar-line`                | [🔗](https://icons8.com/icons/all--style-pulsar-line)                |
| Quill                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/9b22c0ea-5859-44e1-9c4d-58e4cb2b2325.png" alt="Quill" />                  | `quill`                      | [🔗](https://icons8.com/icons/all--style-quill)                      |
| Retro                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/d6f9576a-d8f1-4eb6-8496-151956d87e14.png" alt="Retro" />                  | `retro`                      | [🔗](https://icons8.com/icons/all--style-retro)                      |
| Sci-Fi                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/79cd706b-9c20-492d-a0b0-34264b955a97.png" alt="Sci-Fi" />                 | `sci-fi`                     | [🔗](https://icons8.com/icons/all--style-sci-fi)                     |
| Scribby                    | <img height="32" src="https://maxcdn.icons8.com/style-preview/595e3099-c144-4692-ba90-e7c29aa5b782.png" alt="Scribby" />                | `scribby`                    | [🔗](https://icons8.com/icons/all--style-scribby)                    |
| Serif                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/1f11c37e-615a-4d44-899a-ca63e73e6652.png" alt="Serif" />                  | `serif`                      | [🔗](https://icons8.com/icons/all--style-serif)                      |
| Shadow                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/8f916a0a-9dc6-4f10-b051-8ec841884e42.png" alt="Shadow" />                 | `shadow`                     | [🔗](https://icons8.com/icons/all--style-shadow)                     |
| Simple Small               | <img height="32" src="https://img-main.icons8.com/small/2x/home.png" alt="Simple Small" />                                              | `p1em`                       | [🔗](https://icons8.com/icons/all--style-p1em)                       |
| Skeuomorphism              | <img height="32" src="https://maxcdn.icons8.com/style-preview/d2b9d899-5015-4574-9694-460d685b9c06.png" alt="Skeuomorphism" />          | `skeuomorphism`              | [🔗](https://icons8.com/icons/all--style-skeuomorphism)              |
| Softteal                   | <img height="32" src="https://maxcdn.icons8.com/style-preview/b50e5924-8e75-4377-9f19-39b37393d67e.png" alt="Softteal" />               | `softteal`                   | [🔗](https://icons8.com/icons/all--style-softteal)                   |
| Softteal Color             | <img height="32" src="https://maxcdn.icons8.com/style-preview/3f3303f2-8a68-409c-995d-30bdb1dd1e1a.png" alt="Softteal Color" />         | `softteal-color`             | [🔗](https://icons8.com/icons/all--style-softteal-color)             |
| Softteal Gradient          | <img height="32" src="https://maxcdn.icons8.com/style-preview/7522a063-1659-45a8-a83a-8a3172e91ada.png" alt="Softteal Gradient" />      | `softteal-gradient`          | [🔗](https://icons8.com/icons/all--style-softteal-gradient)          |
| Stamp                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/b4e3d164-3dfc-4b0f-8775-72bb5f486ea5.png" alt="Stamp" />                  | `stamp`                      | [🔗](https://icons8.com/icons/all--style-stamp)                      |
| Stencil                    | <img height="32" src="https://maxcdn.icons8.com/style-preview/151951b1-d634-4539-acad-f5e9a5e8870e.png" alt="Stencil" />                | `stencil`                    | [🔗](https://icons8.com/icons/all--style-stencil)                    |
| Stickers                   | <img height="32" src="https://img-main.icons8.com/stickers/2x/home.png" alt="Stickers" />                                               | `stickers`                   | [🔗](https://icons8.com/icons/all--style-stickers)                   |
| Stickers Duotone           | <img height="32" src="https://maxcdn.icons8.com/style-preview/0510bbba-a218-49db-9fa0-cdb67ae578c8.png" alt="Stickers Duotone" />       | `stickers-duotone`           | [🔗](https://icons8.com/icons/all--style-stickers-duotone)           |
| Stitch                     | <img height="32" src="https://maxcdn.icons8.com/style-preview/8b03ded4-1fc1-4494-a316-3e894c0e0709.png" alt="Stitch" />                 | `stitch`                     | [🔗](https://icons8.com/icons/all--style-stitch)                     |
| Tapes                      | <img height="32" src="https://maxcdn.icons8.com/style-preview/0e45fa3a-7d5a-4bea-b06f-a4141becdafc.png" alt="Tapes" />                  | `tapes`                      | [🔗](https://icons8.com/icons/all--style-tapes)                      |
| Tiny Bold                  | <img height="32" src="https://maxcdn.icons8.com/style-preview/d62792e1-dd77-4dfc-a0d0-40d75ebd194e.png" alt="Tiny Bold" />              | `tiny-bold`                  | [🔗](https://icons8.com/icons/all--style-tiny-bold)                  |
| Tiny Bold Color            | <img height="32" src="https://maxcdn.icons8.com/style-preview/ada5923e-1e02-4d3a-8be0-0ecb0ef272ba.png" alt="Tiny Bold Color" />        | `tiny-duotone`               | [🔗](https://icons8.com/icons/all--style-tiny-duotone)               |
| Tiny Color                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/d56fc07e-fd7c-4a7e-90a0-b7fc2f58d8d4.png" alt="Tiny Color" />             | `tiny-color`                 | [🔗](https://icons8.com/icons/all--style-tiny-color)                 |
| Tiny Glyph                 | <img height="32" src="https://maxcdn.icons8.com/style-preview/d8665ebc-dd6e-476b-a00e-5cc06aac7b0f.png" alt="Tiny Glyph" />             | `tiny-glyph`                 | [🔗](https://icons8.com/icons/all--style-tiny-glyph)                 |
| Water Color                | <img height="32" src="https://maxcdn.icons8.com/style-preview/935a875a-621b-4b57-ad7c-7f4e9ed35ba8.jpeg" alt="Water Color" />           | `water-color`                | [🔗](https://icons8.com/icons/all--style-water-color)                |
| Windows 10                 | <img height="32" src="https://img-main.icons8.com/windows/2x/home.png" alt="Windows 10" />                                              | `win10`                      | [🔗](https://icons8.com/icons/all--style-win10)                      |
| Windows 11 Color           | <img height="32" src="https://maxcdn.icons8.com/style-preview/f5c16571-621e-4107-894f-5928bd316b06.png" alt="Windows 11 Color" />       | `fluent`                     | [🔗](https://icons8.com/icons/all--style-fluent)                     |
| Windows 11 Filled          | <img height="32" src="https://img-main.icons8.com/fluency-systems-filled/2x/home.png" alt="Windows 11 Filled" />                        | `fluent-systems-filled`      | [🔗](https://icons8.com/icons/all--style-fluent-systems-filled)      |
| Windows 11 Outline         | <img height="32" src="https://img-main.icons8.com/fluency-systems-regular/2x/home.png" alt="Windows 11 Outline" />                      | `fluent-systems-regular`     | [🔗](https://icons8.com/icons/all--style-fluent-systems-regular)     |
| Windows Metro              | <img height="32" src="https://img-main.icons8.com/metro/2x/home.png" alt="Windows Metro" />                                             | `win8`                       | [🔗](https://icons8.com/icons/all--style-win8)                       |

## Contributing

Contributions are welcome! Whether it's bug fixes, new features, documentation improvements, or suggestions, we appreciate your help. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- [Icons8](https://icons8.com) for providing the API and icons
- ❤️ All contributors who help improve this project!

## Support

If you encounter any issues, have questions, or would like to request a feature, please [open an issue](https://github.com/alexander-danilenko/icons8-download-cli/issues) on GitHub.
