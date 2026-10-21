"""
Instagram Automation Repost Remover
Universal Open-Source Edition
Ultra-fast, accurate automated repost removal with live in-browser HUD and terminal stats.
Works for any Instagram account.

💡 INTERNET SPEED NOTICE:
"Adjust mode into your internet speed!"
Recommended: SAFE Mode — Use Safe mode if your internet is slow to prevent timeouts or rate limits.
"""

import sys
import os
import time
import json
import traceback
from pathlib import Path

# Ensure dependencies are available
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
except ImportError:
    print("\n[!] Selenium not found. Installing selenium...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def print_banner(speed_mode="SAFE", target_url=""):
    banner = f"""
{Colors.CYAN}{Colors.BOLD}======================================================================
  INSTAGRAM REPOST REMOVER - AUTOMATION ENGINE
======================================================================{Colors.ENDC}
{Colors.YELLOW}Speed Mode  :{Colors.ENDC} {speed_mode} {Colors.GREEN}(Recommended: SAFE Mode){Colors.ENDC}
{Colors.YELLOW}Notice      :{Colors.ENDC} Adjust mode into your internet speed!
{Colors.CYAN}💡 Tip       :{Colors.ENDC} Use Safe mode if your internet is slow.
{Colors.YELLOW}Target URL  :{Colors.ENDC} {target_url if target_url else "(Auto-detected from logged in account)"}
{Colors.YELLOW}Engine      :{Colors.ENDC} Selenium Chrome + In-Page V8 Execution + Live HUD
======================================================================
"""
    print(banner)

def get_config_path():
    return Path(__file__).parent / "config.json"

def load_config():
    config_path = get_config_path()
    default_config = {
        "target_url": "",
        "speed_mode": "SAFE",
        "delays_ms": {
            "TURBO": {
                "click_delay": 200,
                "modal_delay": 250,
                "next_delay": 200
            },
            "FAST": {
                "click_delay": 450,
                "modal_delay": 500,
                "next_delay": 400
            },
            "SAFE": {
                "click_delay": 1500,
                "modal_delay": 1800,
                "next_delay": 1500
            }
        },
        "max_reposts_to_remove": 0,
        "headless": False
    }
    
    if not config_path.exists():
        save_config(default_config)
        return default_config
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # Ensure keys exist
            for k, v in default_config.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
    except Exception:
        return default_config

def save_config(config):
    try:
        config_path = get_config_path()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"[!] Warning: Could not save config.json: {e}")

# JavaScript code injected into the page for ultra-fast DOM manipulation and live HUD
IN_PAGE_AUTOMATION_SCRIPT = r"""
(function() {
    if (window.__repostRemoverActive) {
        console.log("[RepostRemover] Already initialized.");
        return;
    }
    window.__repostRemoverActive = true;

    // Configuration passed or default
    const config = window.__repostRemoverConfig || {
        speed_mode: "SAFE",
        delays: { click_delay: 1500, modal_delay: 1800, next_delay: 1500 },
        max_remove: 0
    };

    window.__repostRemoverStats = {
        status: "RUNNING",
        removed_count: 0,
        current_action: "Initializing...",
        is_paused: false,
        error_msg: null,
        completed: false
    };

    // Create stylish Floating HUD
    const existingHud = document.getElementById("ig-repost-remover-hud");
    if (existingHud) existingHud.remove();

    const hud = document.createElement("div");
    hud.id = "ig-repost-remover-hud";
    hud.innerHTML = `
        <div style="
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 999999;
            background: rgba(18, 18, 18, 0.95);
            backdrop-filter: blur(12px);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            border-radius: 16px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.15);
            padding: 16px 20px;
            width: 320px;
            user-select: none;
            transition: all 0.3s ease;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: #00ff88; box-shadow: 0 0 8px #00ff88;" id="ig-hud-dot"></div>
                    <span style="font-weight: 700; font-size: 14px; letter-spacing: 0.5px; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">REPOST REMOVER</span>
                </div>
                <span id="ig-hud-mode" style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; color: #00e5ff;">SAFE 🛡️</span>
            </div>
            
            <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; margin-bottom: 10px; text-align: center;">
                <div style="font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 1px;">Reposts Removed</div>
                <div id="ig-hud-count" style="font-size: 36px; font-weight: 800; color: #00ff88; line-height: 1.1; margin: 4px 0;">0</div>
                <div id="ig-hud-status" style="font-size: 12px; color: #ddd; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Starting automation...</div>
            </div>

            <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <button id="ig-hud-pause-btn" style="
                    flex: 1;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 8px;
                    background: #2a2a2a;
                    color: white;
                    font-size: 12px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.2s;
                ">Pause</button>
                <button id="ig-hud-speed-btn" style="
                    flex: 1;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 8px;
                    background: #333;
                    color: white;
                    font-size: 12px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background 0.2s;
                ">Mode: SAFE</button>
            </div>

            <div style="font-size: 10px; color: #aaa; text-align: center; line-height: 1.3;">
                💡 Adjust mode into your internet speed.<br>
                <span style="color: #00e5ff; font-weight: 600;">Recommended: Safe Mode</span> if internet is slow.
            </div>
        </div>
    `;
    document.body.appendChild(hud);

    const countEl = document.getElementById("ig-hud-count");
    const statusEl = document.getElementById("ig-hud-status");
    const pauseBtn = document.getElementById("ig-hud-pause-btn");
    const speedBtn = document.getElementById("ig-hud-speed-btn");
    const modeEl = document.getElementById("ig-hud-mode");
    const dotEl = document.getElementById("ig-hud-dot");

    // Initialize labels based on starting mode
    const initialMode = config.speed_mode || "SAFE";
    if (speedBtn) speedBtn.innerText = "Mode: " + initialMode;
    if (modeEl) {
        modeEl.innerText = initialMode + (initialMode === "TURBO" ? " ⚡" : (initialMode === "FAST" ? " 🚀" : " 🛡️"));
        modeEl.style.color = (initialMode === "TURBO" ? "#ffeb3b" : (initialMode === "FAST" ? "#ff9800" : "#00e5ff"));
    }

    function updateHud(statusText, removedDelta = 0) {
        if (removedDelta > 0) {
            window.__repostRemoverStats.removed_count += removedDelta;
            if (countEl) countEl.innerText = window.__repostRemoverStats.removed_count;
        }
        if (statusText) {
            window.__repostRemoverStats.current_action = statusText;
            if (statusEl) statusEl.innerText = statusText;
        }
    }

    pauseBtn.addEventListener("click", () => {
        window.__repostRemoverStats.is_paused = !window.__repostRemoverStats.is_paused;
        if (window.__repostRemoverStats.is_paused) {
            pauseBtn.innerText = "Resume";
            pauseBtn.style.background = "#00ff88";
            pauseBtn.style.color = "#000";
            dotEl.style.background = "#ffbb00";
            dotEl.style.boxShadow = "0 0 8px #ffbb00";
            updateHud("Paused by user");
        } else {
            pauseBtn.innerText = "Pause";
            pauseBtn.style.background = "#2a2a2a";
            pauseBtn.style.color = "#fff";
            dotEl.style.background = "#00ff88";
            dotEl.style.boxShadow = "0 0 8px #00ff88";
            updateHud("Resuming...");
        }
    });

    const speedModes = ["SAFE", "FAST", "TURBO"];
    const speedDelays = {
        "SAFE":  { click_delay: 1500, modal_delay: 1800, next_delay: 1500 },
        "FAST":  { click_delay: 450, modal_delay: 500, next_delay: 400 },
        "TURBO": { click_delay: 200, modal_delay: 250, next_delay: 200 }
    };
    let currentSpeedIdx = speedModes.indexOf(initialMode);
    if (currentSpeedIdx === -1) currentSpeedIdx = 0;

    speedBtn.addEventListener("click", () => {
        currentSpeedIdx = (currentSpeedIdx + 1) % speedModes.length;
        const modeName = speedModes[currentSpeedIdx];
        config.speed_mode = modeName;
        config.delays = speedDelays[modeName];
        speedBtn.innerText = "Mode: " + modeName;
        modeEl.innerText = modeName + (modeName === "TURBO" ? " ⚡" : (modeName === "FAST" ? " 🚀" : " 🛡️"));
        modeEl.style.color = (modeName === "TURBO" ? "#ffeb3b" : (modeName === "FAST" ? "#ff9800" : "#00e5ff"));
        updateHud("Switched to " + modeName + " mode");
    });

    const sleep = (ms) => new Promise(r => setTimeout(r, ms));

    // Reliable trusted-like click dispatcher that triggers React listeners
    function triggerRealClick(element) {
        if (!element) return;
        const rect = element.getBoundingClientRect();
        const clientX = rect.left + rect.width / 2;
        const clientY = rect.top + rect.height / 2;
        const opts = { bubbles: true, cancelable: true, view: window, clientX, clientY };
        
        element.dispatchEvent(new PointerEvent('pointerdown', opts));
        element.dispatchEvent(new MouseEvent('mousedown', opts));
        element.dispatchEvent(new PointerEvent('pointerup', opts));
        element.dispatchEvent(new MouseEvent('mouseup', opts));
        element.dispatchEvent(new MouseEvent('click', opts));
        if (typeof element.click === 'function') {
            element.click();
        }
    }

    // Dismiss common prompts ("Not Now", "Cancel")
    async function dismissPopups() {
        const dismissKeywords = ["Not Now", "Not now", "Cancel"];
        const buttons = Array.from(document.querySelectorAll('button, div[role="button"]'));
        for (const btn of buttons) {
            const text = (btn.innerText || "").trim();
            if (dismissKeywords.includes(text)) {
                triggerRealClick(btn);
                await sleep(200);
            }
        }
    }

    // Main Automation Loop
    async function runRemoverLoop() {
        console.log("[RepostRemover] Loop started at speed: " + config.speed_mode);
        console.log("[RepostRemover] 💡 Tip: Adjust mode into your internet speed. Safe mode recommended for slow connections.");
        updateHud("Starting Repost Remover...");
        await dismissPopups();

        let consecutiveFails = 0;
        let lastRemovedPostHref = null;

        while (true) {
            while (window.__repostRemoverStats.is_paused) {
                await sleep(500);
            }

            if (config.max_remove > 0 && window.__repostRemoverStats.removed_count >= config.max_remove) {
                updateHud(`Reached target of ${config.max_remove} reposts removed!`);
                window.__repostRemoverStats.completed = true;
                break;
            }

            // 1. Are we currently inside a post modal?
            let modal = document.querySelector('div[role="dialog"], article[role="presentation"]');

            if (!modal) {
                // We are on the reposts grid page.
                updateHud("Scanning reposts grid...");
                let gridLinks = Array.from(document.querySelectorAll('main a[href*="/p/"], main a[href*="/reel/"]'));

                if (lastRemovedPostHref) {
                    gridLinks = gridLinks.filter(a => a.getAttribute('href') !== lastRemovedPostHref);
                }

                if (gridLinks.length === 0) {
                    updateHud("Scrolling down for more reposts...");
                    const prevScrollY = window.scrollY;
                    window.scrollBy(0, 1000);
                    await sleep(800);

                    gridLinks = Array.from(document.querySelectorAll('main a[href*="/p/"], main a[href*="/reel/"]'));
                    if (gridLinks.length === 0 && window.scrollY === prevScrollY) {
                        consecutiveFails++;
                        if (consecutiveFails >= 3) {
                            const pageText = document.body.innerText || '';
                            if (pageText.includes("No Reposts Yet") || pageText.includes("No reposts yet") || consecutiveFails >= 4) {
                                updateHud("✅ All reposts have been removed!");
                                window.__repostRemoverStats.completed = true;
                                if (dotEl) dotEl.style.background = "#00e5ff";
                                break;
                            }
                        }
                        await sleep(1000);
                        continue;
                    }
                }

                consecutiveFails = 0;
                const firstPost = gridLinks[0];
                if (!firstPost) {
                    await sleep(500);
                    continue;
                }

                lastRemovedPostHref = firstPost.getAttribute('href');
                updateHud("Opening repost item...");
                triggerRealClick(firstPost);
                await sleep(config.delays.modal_delay);
                modal = document.querySelector('div[role="dialog"], article[role="presentation"]');
            }

            // 2. Locate and click Repost removal trigger
            let removedThisItem = false;

            // Strategy A: The Repost attribution badge / purple circle on the media
            // Instagram overlays a circle with fill="#7638FA" or small repost svg (width <= 23)
            const purpleCircle = document.querySelector('circle[fill="#7638FA"]');
            const mediaRepostSvg = Array.from(document.querySelectorAll('svg')).find(s => {
                const aria = (s.getAttribute('aria-label') || '').toLowerCase();
                const title = (s.querySelector('title')?.textContent || '').toLowerCase();
                if (!aria.includes('repost') && !title.includes('repost')) return false;
                const rect = s.getBoundingClientRect();
                return rect.width <= 23 && rect.width > 0;
            });

            const repostBadge = purpleCircle 
                ? (purpleCircle.closest('[role="button"]') || purpleCircle.closest('div') || purpleCircle.parentElement) 
                : (mediaRepostSvg ? (mediaRepostSvg.closest('[role="button"]') || mediaRepostSvg.closest('div') || mediaRepostSvg.parentElement) : null);

            if (repostBadge) {
                updateHud("Clicking Repost attribution badge...");
                triggerRealClick(repostBadge);
                await sleep(config.delays.click_delay);

                // Now look for the "Delete" button inside the opened popover / dialog ("You reposted this. Delete")
                const allElements = Array.from(document.querySelectorAll('*'));
                const deleteBtn = allElements.find(el => {
                    const txt = (el.innerText || '').trim();
                    return txt === 'Delete' && el.tagName !== 'SCRIPT' && el.offsetWidth > 0;
                });

                if (deleteBtn) {
                    updateHud("Clicking Delete to remove repost...");
                    triggerRealClick(deleteBtn);
                    await sleep(config.delays.click_delay);

                    // Check if confirmation modal appeared (e.g. "Delete Repost? Delete / Cancel")
                    const confirmDelBtn = Array.from(document.querySelectorAll('*')).find(el => {
                        const txt = (el.innerText || '').trim().toLowerCase();
                        return (txt === 'delete' || txt === 'remove') && el.tagName !== 'SCRIPT' && el.offsetWidth > 0;
                    });
                    if (confirmDelBtn && confirmDelBtn !== deleteBtn) {
                        triggerRealClick(confirmDelBtn);
                        await sleep(config.delays.click_delay);
                    }

                    removedThisItem = true;
                    updateHud("Repost removed! 🎯", 1);
                }
            }

            // Strategy B: Action Bar Repost Button fallback
            if (!removedThisItem) {
                const actionRepostSvg = Array.from(document.querySelectorAll('svg[aria-label="Repost"]')).find(s => {
                    const rect = s.getBoundingClientRect();
                    return rect.width >= 23 && rect.y > 500;
                });

                if (actionRepostSvg) {
                    const actionBtn = actionRepostSvg.closest('[role="button"], button') || actionRepostSvg.parentElement;
                    updateHud("Clicking Action Bar Repost button...");
                    triggerRealClick(actionBtn);
                    await sleep(config.delays.click_delay);

                    // Check for confirmation popover/menu ("Remove", "Remove repost", "Undo repost", "Delete")
                    const confirmBtn = Array.from(document.querySelectorAll('button, [role="button"]')).find(b => {
                        const txt = (b.innerText || '').trim().toLowerCase();
                        return ['remove', 'remove repost', 'undo repost', 'delete', 'remove from reposts'].includes(txt);
                    });

                    if (confirmBtn) {
                        updateHud("Confirming removal...");
                        triggerRealClick(confirmBtn);
                        await sleep(config.delays.click_delay);
                    }

                    removedThisItem = true;
                    updateHud("Repost removed! 🎯", 1);
                }
            }

            // 3. Move to next post or close modal
            updateHud("Navigating to next item...");
            const nextBtn = document.querySelector(
                'div[role="dialog"] button svg[aria-label="Next"], ' +
                'div[role="dialog"] svg[aria-label="Next"], ' +
                'button[aria-label="Next"]'
            )?.closest('button, [role="button"]');

            if (nextBtn) {
                triggerRealClick(nextBtn);
                await sleep(config.delays.next_delay);
            } else {
                // Dispatch ArrowRight
                document.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'ArrowRight',
                    code: 'ArrowRight',
                    bubbles: true
                }));
                await sleep(config.delays.next_delay);

                // Close modal
                const closeBtn = document.querySelector(
                    'div[role="dialog"] button svg[aria-label="Close"], ' +
                    'button svg[aria-label="Close"], ' +
                    'svg[aria-label="Close"]'
                )?.closest('button, [role="button"]');

                if (closeBtn) {
                    triggerRealClick(closeBtn);
                } else {
                    document.dispatchEvent(new KeyboardEvent('keydown', {
                        key: 'Escape',
                        code: 'Escape',
                        bubbles: true
                    }));
                }
                await sleep(config.delays.modal_delay);
            }
        }
    }

    runRemoverLoop().catch(err => {
        console.error("[RepostRemover Error]", err);
        window.__repostRemoverStats.error_msg = err.toString();
        window.__repostRemoverStats.status = "ERROR";
        updateHud("Error: " + err.message);
    });
})();
"""

def setup_chrome_driver(headless=False):
    """Configures Chrome with a persistent user data directory so login is saved."""
    user_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "chrome_user_data"))
    os.makedirs(user_data_dir, exist_ok=True)
    
    options = Options()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    
    print(f"{Colors.BLUE}[*] Launching Chrome with dedicated profile at:{Colors.ENDC} {user_data_dir}")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver

def check_logged_in(driver):
    """Checks if the user is currently logged into Instagram."""
    try:
        curr_url = driver.current_url.lower()
        if "accounts/login" in curr_url:
            return False
        
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}
        if 'sessionid' in cookies and cookies['sessionid']:
            return True
        
        nav_elements = driver.find_elements(By.XPATH, "//nav | //*[@aria-label='Home'] | //*[@aria-label='Direct messaging'] | //*[@aria-label='New post']")
        if len(nav_elements) > 0:
            return True
            
        return False
    except Exception:
        return False

def wait_for_user_login(driver):
    """Prompts the user to log in if not already logged in, polling until login succeeds."""
    print(f"{Colors.CYAN}[*] Navigating to Instagram to check authentication...{Colors.ENDC}")
    driver.get("https://www.instagram.com/")
    time.sleep(3)
    
    if check_logged_in(driver):
        print(f"{Colors.GREEN}[✓] Active login session found!{Colors.ENDC}")
        return True
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}======================================================================{Colors.ENDC}")
    print(f"{Colors.YELLOW}{Colors.BOLD} >>> ACTION REQUIRED: PLEASE LOG IN TO INSTAGRAM IN THE CHROME WINDOW <<<{Colors.ENDC}")
    print(f"{Colors.YELLOW} Please log in manually (username/password or Facebook / 2FA).")
    print(f" Your login session will be SAVED securely in your local browser profile!")
    print(f" Waiting for login completion...{Colors.ENDC}")
    print(f"{Colors.YELLOW}{Colors.BOLD}======================================================================{Colors.ENDC}\n")
    
    while True:
        time.sleep(2)
        if check_logged_in(driver):
            print(f"\n{Colors.GREEN}{Colors.BOLD}[✓] Login successful! Detected authenticated session.{Colors.ENDC}")
            time.sleep(1)
            return True

def extract_username_from_session(driver):
    """
    Attempts to detect the logged-in Instagram username directly from the browser DOM.
    Returns username string if found, otherwise None.
    """
    try:
        username = driver.execute_script("""
            try {
                // Method 1: Check sidebar navigation profile link
                const links = Array.from(document.querySelectorAll('a[href^="/"]'));
                for (const link of links) {
                    const href = link.getAttribute('href') || '';
                    const match = href.match(/^\\/([a-zA-Z0-9._]+)\\/?$/);
                    if (!match) continue;
                    const uname = match[1].toLowerCase();
                    const reserved = ['explore', 'reels', 'direct', 'stories', 'accounts', 'your_activity', 'saved', 'archive', 'settings', 'more', 'legal', 'about', 'help', 'privacy'];
                    if (reserved.includes(uname)) continue;

                    const hasAvatar = !!link.querySelector('img[alt*="profile"], img[alt*="Profile"]');
                    const text = (link.innerText || '').trim().toLowerCase();
                    if (hasAvatar || text === 'profile' || text.includes('profile')) {
                        return match[1];
                    }
                }
                
                // Method 2: Check window._sharedData
                if (window._sharedData && window._sharedData.config && window._sharedData.config.viewer) {
                    return window._sharedData.config.viewer.username;
                }

                // Method 3: Any navigation link matching single-segment path with avatar
                for (const link of links) {
                    const href = link.getAttribute('href') || '';
                    const match = href.match(/^\\/([a-zA-Z0-9._]+)\\/?$/);
                    if (!match) continue;
                    const uname = match[1].toLowerCase();
                    const reserved = ['explore', 'reels', 'direct', 'stories', 'accounts', 'your_activity', 'saved', 'archive', 'settings', 'more', 'legal', 'about', 'help', 'privacy'];
                    if (!reserved.includes(uname) && link.querySelector('img, svg')) {
                        return match[1];
                    }
                }
            } catch(e) {}
            return null;
        """)
        if username and isinstance(username, str) and len(username) > 0:
            return username.strip().strip('/')
    except Exception:
        pass
    return None

def resolve_target_url(driver, target_url=""):
    """
    Resolves the Instagram reposts URL for the user:
    1. Uses provided target_url if already specified.
    2. Auto-detects logged-in username from the browser session.
    3. Prompts the user in terminal if auto-detection couldn't determine the ID.
    NOTE: Never writes personal username to config.json to keep git repository clean.
    """
    target = (target_url or "").strip()
    
    # Check if target is already valid
    if target and "YOUR_USERNAME" not in target and "instagram.com" in target:
        if not target.endswith("/reposts/") and not target.endswith("/reposts"):
            target = target.rstrip("/") + "/reposts/"
        elif target.endswith("/reposts"):
            target = target + "/"
        return target

    # Try auto-detecting from browser session
    print(f"{Colors.CYAN}[*] Detecting your Instagram username from session...{Colors.ENDC}")
    detected_user = extract_username_from_session(driver)
    
    if detected_user:
        print(f"{Colors.GREEN}[✓] Auto-detected logged-in username:{Colors.ENDC} @{detected_user}")
        target = f"https://www.instagram.com/{detected_user}/reposts/"
    else:
        # Prompt user for ID
        print(f"\n{Colors.YELLOW}[?] Could not auto-detect username from page.")
        print(f"    Please enter your Instagram ID / Username (e.g. john_doe):{Colors.ENDC}")
        user_input = input("Instagram ID: ").strip()
        if "instagram.com" in user_input:
            clean = user_input.split("?")[0].rstrip("/")
            if not clean.endswith("/reposts"):
                target = clean + "/reposts/"
            else:
                target = clean + "/"
        else:
            uname = user_input.replace("@", "").strip()
            target = f"https://www.instagram.com/{uname}/reposts/"

    return target

def main():
    config = load_config()
    speed_mode = config.get("speed_mode", "SAFE")
    target_url = config.get("target_url", "").strip()
    
    print_banner(speed_mode=speed_mode, target_url=target_url)
    
    # If target_url is not configured in config.json, prompt the user for their Instagram ID
    if not target_url or "instagram.com" not in target_url:
        print(f"{Colors.CYAN}----------------------------------------------------------------------{Colors.ENDC}")
        print(f"{Colors.YELLOW}[?] Enter your Instagram ID / Username (e.g. john_doe):{Colors.ENDC}")
        print(f"{Colors.CYAN}    (Or press [Enter] to auto-detect from browser after login){Colors.ENDC}")
        user_input = input(f"{Colors.GREEN}Instagram ID > {Colors.ENDC}").strip()
        if user_input:
            if "instagram.com" in user_input:
                clean = user_input.split("?")[0].rstrip("/")
                if not clean.endswith("/reposts"):
                    target_url = clean + "/reposts/"
                else:
                    target_url = clean + "/"
            else:
                uname = user_input.replace("@", "").strip()
                target_url = f"https://www.instagram.com/{uname}/reposts/"
            print(f"{Colors.GREEN}[✓] Target Reposts URL set to:{Colors.ENDC} {target_url}\n")

    
    delays = config.get("delays_ms", {}).get(speed_mode, {
        "click_delay": 1500,
        "modal_delay": 1800,
        "next_delay": 1500
    })
    headless = config.get("headless", False)
    
    driver = None
    try:
        driver = setup_chrome_driver(headless=headless)
        
        # 1. Login flow
        wait_for_user_login(driver)
        
        # 2. Resolve target reposts URL for the current user
        target_url = resolve_target_url(driver, target_url)
        
        # 3. Navigate to the reposts URL
        print(f"{Colors.CYAN}[*] Navigating to target Reposts page:{Colors.ENDC} {target_url}")
        driver.get(target_url)
        time.sleep(4)
        
        # 4. Inject In-Page Automation Engine
        print(f"{Colors.GREEN}[*] Injecting In-Page Automation Engine ({speed_mode} mode)...{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Notice: Adjust mode into your internet speed! (Recommended: SAFE mode if internet is slow){Colors.ENDC}")
        driver.execute_script(f"""
            window.__repostRemoverConfig = {{
                speed_mode: "{speed_mode}",
                delays: {json.dumps(delays)},
                max_remove: {config.get("max_reposts_to_remove", 0)}
            }};
        """)
        driver.execute_script(IN_PAGE_AUTOMATION_SCRIPT)
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}  AUTOMATION IS RUNNING! 🚀{Colors.ENDC}")
        print(f"{Colors.CYAN}  Look at the Chrome window to see the Live HUD counter in real time.{Colors.ENDC}")
        print(f"{Colors.YELLOW}  Tip: Adjust mode into your internet speed using the in-page HUD button.{Colors.ENDC}")
        print(f"{Colors.YELLOW}  Press Ctrl+C in this console anytime to stop safely.{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}\n")
        
        # 5. Monitor loop in terminal
        last_count = 0
        while True:
            time.sleep(1)
            try:
                stats = driver.execute_script("return window.__repostRemoverStats || null;")
                if stats:
                    removed = stats.get("removed_count", 0)
                    action = stats.get("current_action", "")
                    status = stats.get("status", "")
                    completed = stats.get("completed", False)
                    
                    if removed != last_count:
                        last_count = removed
                        print(f"{Colors.GREEN}[✓] Removed Repost #{removed} {Colors.ENDC}| {Colors.CYAN}Successfully deleted from profile!{Colors.ENDC}")
                    
                    if completed:
                        print(f"\n{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}")
                        print(f"{Colors.BOLD}{Colors.GREEN}  DONE! All reposts have been removed successfully! Total: {removed}{Colors.ENDC}")
                        print(f"{Colors.BOLD}{Colors.GREEN}======================================================================{Colors.ENDC}\n")
                        break
                        
                    if status == "ERROR":
                        err = stats.get("error_msg", "Unknown error")
                        print(f"{Colors.RED}[!] Script error encountered: {err}{Colors.ENDC}")
                        break
            except Exception as e:
                if "no such window" in str(e).lower() or "target window already closed" in str(e).lower():
                    print(f"\n{Colors.YELLOW}[*] Chrome window closed by user. Exiting.{Colors.ENDC}")
                    break
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Process interrupted by user. Stopping automation safely...{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal Error: {e}{Colors.ENDC}")
        traceback.print_exc()
    finally:
        print(f"\n{Colors.CYAN}[*] Automation ended. Thanks for using Instagram Repost Remover!{Colors.ENDC}")

if __name__ == "__main__":
    main()
