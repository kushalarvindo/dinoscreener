<div align="center">
  <h1>🦕 Dinoscreener</h1>
  <p><strong>A stunning, ultra-minimalist modern rotary clock screensaver for Windows.</strong></p>
</div>

<br />

<div align="center">
  <img src="https://raw.githubusercontent.com/kushalarvindo/screensaver/main/screenshot.png" alt="Dinoscreener Screenshot" width="800">
</div>

## ✨ Features & Architecture

Dinoscreener is built natively using **Python** and **PyQt6**. It leverages powerful graphics engines to render 60 FPS antialiased shapes, drawing the interface using complex `QPainter` geometry rather than loading static images.

### 🎨 Clock Modes

Dinoscreener V2 features three distinct, meticulously crafted clock styles. Switch between them instantly using the **Up/Down arrow keys**!

| Mode | Description |
|---|---|
| **Modern Rotary Clock** | A dual-ring rotary interface. Calculates exact rotation angles using trigonometry for a seamless spinning wheel effect. The opacity of each number fades gracefully based on distance from the exact time. |
| **Classic Fliqlo** | A retro mechanical flip-clock style! The flip animation utilizes scaling to visually compress the numbers, giving a 3D perspective effect as the card falls. |
| **Chrome Dino Game** | A beautiful, ambient auto-playing Chrome Dino game! Features authentic sprite rendering, exact gravity physics, randomly generated cacti/crows, and day/night clouds. Time is displayed cleanly at the top. |

- **Ambient Lighting System**: Subtle, color-shifting ambient orbs float in the background. These are drawn using `QRadialGradient`, and their coordinates drift organically using trigonometric phase shifts over a 15-second loop.
- **System Integrations**: 
  - Dynamic local weather display ☀️
  - Real-time battery tracking with custom charging icons 🔋 (Using Windows `ctypes.windll.kernel32.GetSystemPowerStatus`)
- **Native GUI Settings**: Configure everything visually straight from the Windows Screen Saver panel! The settings window itself applies Windows 11's transparent **Mica** material natively to its background via `DwmSetWindowAttribute`.

---

## ⌨️ Controls & Keyboard Shortcuts

While the screensaver is running, you can use these keyboard shortcuts to modify it in real time:

- **`Arrow Up` / `Arrow Down`**: Toggle between the Modern Rotary, Classic Fliqlo, and Chrome Dino clock styles.
- **`Spacebar` / `Windows Key`**: Toggle the background Ambient Lighting orbs on or off.
- **`+` (Plus) / `-` (Minus)**: Scale the size of the Fliqlo flip clock up or down.
- **`Ctrl + Z`**: If you enabled "Screenshot Mode" (Strict Exit) in the settings, moving your mouse will no longer close the screensaver. You must press this exact keybind to close it and return to your desktop.

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

<div align="center">
  <p>Built with ❤️ using Python & PyQt6</p>
</div>
