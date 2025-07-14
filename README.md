# AutoLottery
[![Latest Release](https://img.shields.io/github/v/release/leewr9/atlottery)](https://github.com/leewr9/atlottery/releases)
![Build Status](https://github.com/leewr9/atlottery/actions/workflows/build.yml/badge.svg)

This is a Korean automatic lottery purchase program. Built with a PySide6-based GUI and Selenium, it enables automatic lottery ticket buying without the need for a separate web browser.

![](resources/main.png)

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

3. **Run the application**
    ```bash
    uv run python main.py
    ```

## Building Executable
To build the executable file using PyInstaller and the spec file

```bash
uv run pyinstaller ./atlottery.spec
```
- This will create the executable in the `dist` folder.
- Make sure the `atlottery.spec` file is properly configured with resource paths and build options.

## License  
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  
