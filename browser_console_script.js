/**
 * Instagram Repost Remover - Browser Console Automation Script
 * Clean, Universal & Open-Source (Can be run on any Instagram account)
 * 
 * 💡 INTERNET SPEED RECOMMENDATION:
 * "Adjust mode into your internet speed!"
 * Recommended: SAFE Mode — Use Safe mode if your internet is slow to prevent timeouts,
 * skipped items, or Instagram rate limits.
 * 
 * HOW TO USE:
 * 1. Open Google Chrome and log in to your Instagram account.
 * 2. Navigate to your Reposts page: https://www.instagram.com/<your_username>/reposts/
 * 3. Press F12 (Inspect) -> Click on the "Console" tab.
 * 4. Paste this entire code into the Console and press Enter.
 * 5. The in-page HUD will appear and begin removing reposts safely!
 */

(function() {
    if (window.__repostRemoverActive) {
        console.log("%c[InstaRepostRemover] Automation is already running!", "color: yellow; font-size: 14px;");
        return;
    }
    window.__repostRemoverActive = true;

    // Configuration - Default Recommended: SAFE Mode
    const config = {
        speed_mode: "SAFE", // "SAFE", "FAST", or "TURBO"
        delays: {
            SAFE:  { click_delay: 1500, modal_delay: 1800, next_delay: 1500 },
            FAST:  { click_delay: 500, modal_delay: 650, next_delay: 500 },
            TURBO: { click_delay: 300, modal_delay: 400, next_delay: 350 }
        },
        max_remove: 0 // 0 = remove all
    };

    let activeDelays = config.delays[config.speed_mode];

    window.__repostRemoverStats = {
        status: "RUNNING",
        removed_count: 0,
        current_action: "Initializing...",
        is_paused: false,
        error_msg: null,
        completed: false
    };

    // Inject Floating HUD Widget
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

    function updateHud(statusText, removedDelta = 0) {
        if (removedDelta > 0) {
            window.__repostRemoverStats.removed_count += removedDelta;
            if (countEl) countEl.innerText = window.__repostRemoverStats.removed_count;
        }
        if (statusText) {
            window.__repostRemoverStats.current_action = statusText;
            if (statusEl) statusEl.innerText = statusText;
            console.log(`%c[RepostRemover] ${statusText}`, "color: #00ff88; font-weight: bold;");
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
    let currentSpeedIdx = 0;

    speedBtn.addEventListener("click", () => {
        currentSpeedIdx = (currentSpeedIdx + 1) % speedModes.length;
        const modeName = speedModes[currentSpeedIdx];
        config.speed_mode = modeName;
        activeDelays = config.delays[modeName];
        speedBtn.innerText = "Mode: " + modeName;
        modeEl.innerText = modeName + (modeName === "TURBO" ? " ⚡" : (modeName === "FAST" ? " 🚀" : " 🛡️"));
        modeEl.style.color = (modeName === "TURBO" ? "#ffeb3b" : (modeName === "FAST" ? "#ff9800" : "#00e5ff"));
        updateHud("Switched to " + modeName + " mode");
    });

    const sleep = (ms) => new Promise(r => setTimeout(r, ms));

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

    async function runRemoverLoop() {
        console.log("%c[RepostRemover] Automation Started!", "color: #00ff88; font-size: 16px; font-weight: bold;");
        console.log("%c💡 TIP: Adjust mode into your internet speed! Use SAFE mode if your internet is slow.", "color: #00e5ff; font-size: 13px; font-weight: bold;");
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

            let modal = document.querySelector('div[role="dialog"], article[role="presentation"]');

            if (!modal) {
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
                await sleep(activeDelays.modal_delay);
                modal = document.querySelector('div[role="dialog"], article[role="presentation"]');
            }

            let removedThisItem = false;

            // Strategy A: Repost attribution badge (purple circle or small repost icon on media)
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
                await sleep(activeDelays.click_delay);

                // Look for 'Delete' button in the opened popover ("You reposted this. Delete")
                const allElements = Array.from(document.querySelectorAll('*'));
                const deleteBtn = allElements.find(el => {
                    const txt = (el.innerText || '').trim();
                    return txt === 'Delete' && el.tagName !== 'SCRIPT' && el.offsetWidth > 0;
                });

                if (deleteBtn) {
                    updateHud("Clicking Delete to remove repost...");
                    triggerRealClick(deleteBtn);
                    await sleep(activeDelays.click_delay);

                    const confirmDelBtn = Array.from(document.querySelectorAll('*')).find(el => {
                        const txt = (el.innerText || '').trim().toLowerCase();
                        return (txt === 'delete' || txt === 'remove') && el.tagName !== 'SCRIPT' && el.offsetWidth > 0;
                    });
                    if (confirmDelBtn && confirmDelBtn !== deleteBtn) {
                        triggerRealClick(confirmDelBtn);
                        await sleep(activeDelays.click_delay);
                    }

                    removedThisItem = true;
                    updateHud("Repost removed! 🎯", 1);
                }
            }

            // Strategy B: Action Bar Repost Button
            if (!removedThisItem) {
                const actionRepostSvg = Array.from(document.querySelectorAll('svg[aria-label="Repost"]')).find(s => {
                    const rect = s.getBoundingClientRect();
                    return rect.width >= 23 && rect.y > 500;
                });

                if (actionRepostSvg) {
                    const actionBtn = actionRepostSvg.closest('[role="button"], button') || actionRepostSvg.parentElement;
                    updateHud("Clicking Action Bar Repost button...");
                    triggerRealClick(actionBtn);
                    await sleep(activeDelays.click_delay);

                    const confirmBtn = Array.from(document.querySelectorAll('button, [role="button"]')).find(b => {
                        const txt = (b.innerText || '').trim().toLowerCase();
                        return ['remove', 'remove repost', 'undo repost', 'delete', 'remove from reposts'].includes(txt);
                    });

                    if (confirmBtn) {
                        updateHud("Confirming removal...");
                        triggerRealClick(confirmBtn);
                        await sleep(activeDelays.click_delay);
                    }

                    removedThisItem = true;
                    updateHud("Repost removed! 🎯", 1);
                }
            }

            // Advance to next or close modal
            updateHud("Navigating to next item...");
            const nextBtn = document.querySelector(
                'div[role="dialog"] button svg[aria-label="Next"], ' +
                'div[role="dialog"] svg[aria-label="Next"], ' +
                'button[aria-label="Next"]'
            )?.closest('button, [role="button"]');

            if (nextBtn) {
                triggerRealClick(nextBtn);
                await sleep(activeDelays.next_delay);
            } else {
                document.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'ArrowRight',
                    code: 'ArrowRight',
                    bubbles: true
                }));
                await sleep(activeDelays.next_delay);

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
                await sleep(activeDelays.modal_delay);
            }
        }
    }

    runRemoverLoop().catch(err => {
        console.error("[RepostRemover Error]", err);
        updateHud("Error: " + err.message);
    });
})();
