<div align="center">
  <h1>🦕 Dinoscreener</h1>
  <p><strong>A stunning, ultra-minimalist modern rotary clock screensaver for Windows.</strong></p>
</div>

<br />

<div align="center">
  <img src="https://raw.githubusercontent.com/kushalarvindo/screensaver/main/screenshot.png" alt="Dinoscreener Screenshot" width="800">
</div>

## ✨ Features

- **Modern Rotary Interface**: A smooth, elegant dual-ring rotary clock design.
- **Ambient Lighting**: Subtle, color-shifting ambient orbs float in the background.
- **System Integrations**: 
  - Dynamic local weather display ☀️
  - Real-time battery tracking with custom charging icons 🔋
- **Interactive Toggles**: Press spacebar to toggle ambient backgrounds on/off.
- **Screenshot Mode**: True "Strict Exit" support, allowing you to lock the screensaver on-screen purely for screenshots without mouse movements interrupting it.
- **Native GUI Settings**: Configure everything visually straight from the Windows Screen Saver panel!

---

## 🚀 Quick Setup (Pre-Compiled)

1. Navigate to the [Releases](#) tab (or just download the `Dinoscreener.scr` file directly from this repository).
2. Right-click on **`Dinoscreener.scr`**.
3. Select **Install**.
4. The Windows Screen Saver Settings panel will open. Click **Settings...** to customize your accent colors and toggles!

> [!WARNING]
> **Windows Defender False Positive**
> Because `Dinoscreener.scr` is compiled into a single executable using PyInstaller, Windows Defender might incorrectly flag it as a virus (commonly `Trojan:Win32/Wacatac.B!ml`). 
> **This is a notorious false positive.** The source code is entirely open, and you can compile it yourself if you prefer. To bypass this, simply click the notification, select **Allow on device**, and click **Start Actions**.

---

## 🛠️ How to Compile it Yourself

If you'd prefer to build the `.scr` file yourself from the source code rather than using the pre-compiled version, follow these simple steps:

### Prerequisites
- Python 3.10+
- `pip` installed

### Build Steps
1. **Clone the repository**:
   ```cmd
   git clone https://github.com/kushalarvindo/screensaver.git
   cd screensaver
   ```
2. **Install the required dependencies**:
   ```cmd
   pip install PyQt6 pyinstaller
   ```
3. **Compile the executable**:
   Use PyInstaller to bundle the Python script into a single, windowless `.exe` file.
   ```cmd
   pyinstaller --noconsole --onefile --name "Dinoscreener" screensaver.py
   ```
4. **Convert to `.scr`**:
   Once the build completes, navigate to the newly created `dist/` folder and rename the extension!
   ```cmd
   cd dist
   ren Dinoscreener.exe Dinoscreener.scr
   ```
5. **Install**: Right-click `Dinoscreener.scr` and select **Install**.

---

## ⚙️ Configuration Options
Clicking the **Settings...** button in the Windows Screen Saver dialog lets you configure:
- **Accent Color**: Pass any Hex code (e.g. `#8F96BF`, `#FF5733`) to instantly reskin the UI.
- **Show Weather & Battery**: Toggle the extra information line on or off. The layout will dynamically re-center itself!
- **Screenshot Mode**: When enabled, the screensaver will *only* close if you explicitly press `Ctrl+Z`. Moving the mouse or mashing keys won't close it. 

<div align="center">
  <p>Built with ❤️ using Python & PyQt6</p>
</div>
