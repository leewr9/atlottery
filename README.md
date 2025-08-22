# AutoLottery

[![releases](https://img.shields.io/github/v/release/leewr9/atlottery)](https://github.com/leewr9/atlottery/releases)
[![exe-build-release](https://github.com/leewr9/atlottery/actions/workflows/exe-build-release.yml/badge.svg)](https://github.com/leewr9/atlottery/actions/workflows/exe-build-release.yml)

This tool automates Korean lottery ticket purchases, providing both a PySide6-based GUI for interactive use and a command-line script for headless execution, allowing users to buy tickets automatically without opening a web browser.

![main](resources/main.png)

## Feature

- Simple GUI built with PySide6
- Command-line script for headless execution
- Automated lottery purchase using Selenium
- No external web browser required
- Supports executable build with PyInstaller

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/leewr9/atlottery.git
   cd atlottery
   ```

2. **Install dependencies via uv**

   ```bash
   uv sync
   ```

## Usage

### Run Script (Background)

```bash
uv run python cli_app.py
```

- Executes the lottery automation script without opening the GUI.
- Uses environment variables for configuration:
  - `LOTTERY_USER` → Lottery account ID
  - `LOTTERY_PASS` → Lottery account password
  - `LOTTERY_COUNT` → Number of tickets to purchase (default: 5)
  - `EMAIL_SENDER` → Email account for sending notifications (optional)
  - `EMAIL_PASSWORD` → Password for the email account (required if `EMAIL_SENDER` is set)
    - For Gmail, you can use an **App Password** generated here: https://myaccount.google.com/apppasswords
    - If both `EMAIL_SENDER` and `EMAIL_PASSWORD` are provided, the script can send email notifications about the purchase result.
- Suitable for running in the background, scheduled tasks, or automated execution in GitHub Actions workflows.
  - [example workflow](https://github.com/leewr9/atlottery/blob/master/.github/workflows/weekly-purchase.yml)

### Run GUI (Executable)

```bash
uv run python gui_app.py
```

- Launches the GUI for interactive use.
- Make sure the required resource files are correctly placed.

### Build Executable

You can build an executable file using PyInstaller and the provided spec file.

```bash
uv run pyinstaller ./atlottery.spec
```

- The executable will be created in the `dist` folder.
- Ensure the `atlottery.spec` file is correctly configured with resource paths and build options.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
