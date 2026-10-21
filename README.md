# ⚡ Instagram Repost Remover - Automated Mass Cleanup

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15%2B-orange.svg)](https://www.selenium.dev/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)

An intelligent, high-performance automation tool designed to bulk remove reposts from **Instagram Web** automatically. Features automated login detection, auto-username resolution, live in-browser HUD dashboard, and customizable speed profiles.

---

> ### 💡 Internet Speed & Mode Recommendation
> **"Adjust mode into your internet speed!"**
>
> - 🛡️ **Recommended: SAFE Mode** — **Use Safe mode if your internet is slow.** Slower connections need extra time for Instagram's popups, modals, and network requests to finish. SAFE mode prevents timeouts, missed buttons, and action blocks.
> - 🚀 **FAST Mode** — Balanced pacing for regular, stable broadband connections.
> - ⚡ **TURBO Mode** — Maximum velocity execution. Recommended only for high-speed fiber internet with ultra-low latency.

---

## 🌟 Key Features

- 👤 **Universal & Multi-User**: Works for any Instagram account. Automatically detects the authenticated user and navigates directly to their `/reposts/` tab.
- 🛡️ **Safe & Rate-Limit Conscious**: Includes built-in delays and safe pacing to protect your account from temporary Instagram restrictions.
- 🔄 **Auto-Login Detection**: Launches a dedicated Chrome browser and detects authentication automatically without requiring you to store your password in plain text.
- 💾 **Persistent Session**: Keeps your session cached in a local `chrome_user_data` profile. Log in once, and future runs start immediately.
- 📊 **Real-Time In-Browser HUD**: Displays a floating cyberpunk-styled control widget directly inside Instagram:
  - Live removal counter
  - Real-time status tracker
  - **Pause / Resume** toggle
  - **Speed Mode Switcher** (`SAFE 🛡️`, `FAST 🚀`, `TURBO ⚡`)
- 📜 **Infinite Scroll Engine**: Automatically scrolls down and dynamically fetches older reposts until your repost grid is completely cleared.
- 🎯 **Multi-Strategy Selectors**: Built with multiple selector layers (attribution badges, SVG paths, confirm dialogs) ensuring stability across Instagram UI updates.

---

## 📁 Repository Structure

```text
├── repost_remover.py          # Core Python automation engine (Selenium + in-page V8 injection)
├── run.bat                    # 1-Click launcher for Windows users
├── config.json                # User settings (Speed mode, custom delays, limits)
├── browser_console_script.js  # 100% Zero-install script for Chrome DevTools Console
├── requirements.txt           # Python dependency specifications
├── .gitignore                 # Protects private cookies and session files from git
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- [Google Chrome](https://www.google.com/chrome/) installed.
- [Python 3.8+](https://www.python.org/downloads/) installed (make sure to check **"Add Python to PATH"** during setup).

---

### Option 1: One-Click Runner on Windows (`run.bat`) — Easiest

1. Clone or download this repository:
   ```bash
   git clone https://github.com/mrifadh27/AutoInstaRepostRemover.git
   cd AutoInstaRepostRemover
   ```
2. Double-click **`run.bat`**.
3. It will verify Python, install `selenium` if needed, and prompt you:
   - Enter your **Instagram ID / Username** (e.g. `mrifadh_27`), or just press **Enter** to auto-detect it after logging in!
4. **Log in to Instagram** in the opened Chrome window.
5. The tool will open your reposts tab and start removing reposts automatically!

---

### Option 2: Command Line (Windows, macOS, Linux)

1. Clone the repository and install requirements:
   ```bash
   git clone https://github.com/mrifadh27/AutoInstaRepostRemover.git
   cd AutoInstaRepostRemover
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python repost_remover.py
   ```
3. Enter your Instagram ID when prompted (or press Enter to auto-detect after login).

---

### Option 3: Browser Console Script (Zero Python / No Installation)

If you don't want to install Python:

1. Open **Google Chrome** and log in to [Instagram](https://www.instagram.com/).
2. Navigate to your Reposts page:
   ```text
   https://www.instagram.com/<your_username>/reposts/
   ```
3. Press **`F12`** (or right-click anywhere and click **Inspect**).
4. Click on the **Console** tab.
5. Open [`browser_console_script.js`](./browser_console_script.js), copy the entire content, paste it into the console, and press **Enter**.
6. The floating HUD will appear and begin removing reposts!

---

## ⚙️ Configuration (`config.json`)

You can customize the automation behavior by modifying `config.json`:

```json
{
    "target_url": "",
    "speed_mode": "SAFE",
    "delays_ms": {
        "SAFE": {
            "click_delay": 1500,
            "modal_delay": 1800,
            "next_delay": 1500
        },
        "FAST": {
            "click_delay": 450,
            "modal_delay": 500,
            "next_delay": 400
        },
        "TURBO": {
            "click_delay": 200,
            "modal_delay": 250,
            "next_delay": 200
        }
    },
    "max_reposts_to_remove": 0,
    "headless": false
}
```

### Configuration Options:
| Setting | Description | Default |
| :--- | :--- | :--- |
| **`target_url`** | Reposts page URL. If left empty (`""`), the script **automatically discovers** your username once you log in. | `""` |
| **`speed_mode`** | Automation pace (`"SAFE"`, `"FAST"`, `"TURBO"`). **SAFE mode is recommended**, especially if your internet connection is slow. | `"SAFE"` |
| **`max_reposts_to_remove`** | Maximum items to remove (`0` removes everything until the tab is empty). | `0` |
| **`headless`** | Set to `true` to run Chrome without a visible window (only do this after logging in at least once). | `false` |

---

## 🎛️ Live In-Page HUD

When running, a floating control box is attached to the bottom-right corner of Instagram:

- **Reposts Removed Counter**: Real-time tally of successfully removed reposts.
- **Live Status**: Micro-actions being performed (e.g. clicking badges, dismissing dialogs, navigating).
- **Pause / Resume**: Click anytime to pause operations if you want to inspect a post.
- **Mode Toggle**: Click the mode button to dynamically cycle between `SAFE`, `FAST`, and `TURBO` on the fly.
- **Speed Guide Tip**: Reminds you to match your speed mode to your current internet connection.

---

## 🔒 Privacy & Security

- **Your credentials stay 100% private**: You never enter your password into the script, command line, or configuration files.
- **Local Storage**: Your login cookies are kept locally in the `chrome_user_data/` folder on your own computer.
- **Git Protection**: The provided `.gitignore` automatically prevents `chrome_user_data/` and session tokens from ever being uploaded or committed to GitHub.

---

## ❓ Troubleshooting & FAQ

### Q: Instagram says "Please wait a few minutes before trying again"
> **Answer**: Instagram has temporary rate limits for rapid actions.
> - Switch to **`SAFE`** mode using the in-page HUD or in `config.json`.
> - Pause the script for 10–15 minutes and resume.

### Q: The script opened Instagram, but didn't open my reposts tab?
> **Answer**: Ensure you completed the login in the opened Chrome window. If two-factor authentication (2FA) or "Save Login Info" prompts appear, accept or dismiss them. Once you are authenticated, the script will automatically detect your username and proceed.

### Q: Can I run this in the background?
> **Answer**: Yes. Once you have logged in once, you can set `"headless": true` in `config.json`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
