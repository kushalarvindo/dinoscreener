<div align="center">
  <h1>🦕 Dinoscreener</h1>
  <p><strong>A stunning, ultra-minimalist modern clock screensaver suite for Windows & Linux.</strong></p>
  <p>Featuring <strong>Modern Rotary</strong>, <strong>Classic Flip Clock</strong>, and <strong>Chrome Dino Runner</strong> with custom typography & sprite imports.</p>
</div>

<br />

<div align="center">
  <img src="screenshots/dino.gif" alt="Dinoscreener Screenshot" width="800">
</div>

---

## ✨ Features & Architecture

Dinoscreener is built natively using **Python** and **PyQt6**. It renders buttery-smooth 60 FPS antialiased graphics drawn using vector `QPainter` geometry and real-time physics.

### 🎨 Clock Modes

Dinoscreener features three distinct, meticulously crafted clock styles. Switch between them instantly using the **Up/Down arrow keys** or via the interactive settings dialog!

| Mode | Description | Preview |
|---|---|---|
| **Modern Rotary** | A dual-ring rotary interface calculating exact rotation angles using trigonometry for a seamless spinning wheel effect with optional Weather & Battery telemetry. | <img src="screenshots/Screenshot (Modern Rotary).png" width="260" alt="Rotary Clock"> |
| **Classic Flip Clock** | A retro mechanical flip-clock style utilizing 3D perspective scaling to visually compress flip tiles, customizable scaling, and leading zero toggles. | <img src="screenshots/Screenshot (Flip Clock).png" width="260" alt="Flip Clock"> |
| **Chrome Dino Game** | An authentic auto-playing Chrome Dino runner with accurate gravity physics, procedurally generated obstacles, and custom typography/sprites. | <img src="screenshots/Screenshot (Chrome Dino Game).png" width="260" alt="Dino Game"> |

---

### 🎛️ Modern Spatial Settings Studio

<div align="center">
  <img src="screenshots/Screenshot (Settings UI).png" alt="Settings UI" width="700">
</div>

- **16:9 Authentic Widescreen Preview**: Real-time live canvas displaying exact font scaling, sprite styling, and visual luminance before applying.
- **Collapsible Mode Switcher Pill**: A minimalist capsule indicator that automatically expands on hover into a floating segmented pill switcher with comfortable vertical padding.
- **Windows 11 Dynamic Accent Color**: Automatically reads your Windows 11 accent color (`DWM / AccentColorMenu`) and harmonizes buttons, sliders, duotone icons, and checkboxes with your desktop theme.
- **Custom Typography & Sprite Engine**: Simply **drag and drop** any `.ttf` / `.otf` font file or `.png` / `.jpg` sprite image directly onto the window to customize clock numbers or character sprites. Revert anytime with one click.
- **Ambient Lighting Mode**: Soft, silky background glow orbs that can be toggled via the settings menu or instantly with the **Spacebar**.
- **Tactile Luminance & Scale Controls**: Full-width brightness slider (10% to 100%) and interactive scale slider with tactile `-` / `+` micro-adjusters.
- **OLED Burn-in Protection**: Automatic subtle pixel-shifting algorithm prevents burn-in on OLED and AMOLED panels.
- **Independent Telemetry & Weather Feeds**: Toggle Weather and Battery displays independently (centered alone or joined with a separator dot), and toggle between Celsius (`°C`) and Fahrenheit (`°F`).
- **Strict Exit & System Intercepts**:
  - **Lock Screen on Exit (`Ctrl + Z`)**: Keeps the screensaver active even on mouse movement; requires `Ctrl + Z` to unlock.
  - **Ignore Media Keys**: Prevents volume knobs or Spotify track changes from prematurely closing the screensaver.
  - **Windows Key Guard**: Disables the Windows key to prevent accidental taskbar pops.

---

## ⌨️ Controls & Keyboard Shortcuts

While the screensaver is running, you can use these keyboard shortcuts to modify it in real time:

- **`Spacebar`**: Toggle Ambient Mode glow orbs (or restart Dino game after Game Over).
- **`Arrow Up` / `Arrow Down`**: Toggle between Flip Clock, Rotary Modern, and Chrome Dino clock styles.
- **`+` (Plus) / `-` (Minus)**: Scale the clock size up or down in real time.
- **`Ctrl + Z`**: Unlock / exit the screensaver when "Lock Screen on Exit" (Strict Exit) is enabled.

---

## 🚀 Quick Setup (Pre-Compiled)

### 🪟 Windows Setup
1. Download the latest **`Dinoscreener.scr`** (or `Dinoscreener.exe`) from the [Releases](https://github.com/kushalarvindo/dinoscreener/releases) page.
2. Right-click on **`Dinoscreener.scr`**.
3. Select **Install**.
4. The Windows Screen Saver Settings dialog will open. Click **Settings...** to customize your modes, fonts, and display preferences!

> [!WARNING]
> **Windows Defender False Positive**  
> Because `Dinoscreener.scr` is compiled into a standalone executable using PyInstaller without an expensive commercial code-signing certificate, Windows Defender might occasionally flag it as an unrecognized binary (`Trojan:Win32/Wacatac.B!ml`).  
> **This is a false positive.** The entire codebase is open source and transparent. You can inspect the source code or compile it yourself using the instructions below. To allow it, select **Allow on device** in Windows Security.

### 🐧 Linux Setup
1. Download **`dinoscreener-linux-x86_64.tar.gz`** from the [Releases](https://github.com/kushalarvindo/dinoscreener/releases) page.
2. Extract the archive and run the installer:
   ```bash
   tar -xzvf dinoscreener-linux-x86_64.tar.gz
   cd dinoscreener
   chmod +x install-linux.sh
   ./install-linux.sh
   ```
3. Launch **Dinoscreener** from your application menu, or run from the command line:
   - `./dinoscreener` or `dinoscreener --settings` $\rightarrow$ Opens the visual settings studio.
   - `dinoscreener --fullscreen` or `dinoscreener -s` $\rightarrow$ Launches the screensaver directly in fullscreen.

---

## 🛠️ How to Compile It Yourself

If you prefer building the binary directly from source:

### Prerequisites
- Python 3.10+
- `pip` package manager

### Windows Build Steps
```cmd
git clone https://github.com/kushalarvindo/dinoscreener.git
cd dinoscreener
pip install PyQt6 pillow pyinstaller
pyinstaller Dinoscreener.spec --noconfirm
copy /y dist\Dinoscreener.exe Dinoscreener.scr
```

### Linux Build Steps
```bash
git clone https://github.com/kushalarvindo/dinoscreener.git
cd dinoscreener
pip install PyQt6 pillow pyinstaller
pyinstaller --noconfirm --onefile --windowed --add-data "Bungee-Regular.ttf:." --add-data "app_icon.png:." --name dinoscreener screensaver.py
chmod +x dist/dinoscreener
./dist/dinoscreener --settings
```

---

<div align="center">
  <p>Crafted with precision using Python & PyQt6</p>
</div>
