import os
import time
import json
import sys
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException

PROFILE_DIR = os.path.join(os.getcwd(), "Profile")
CONFIG_FILE = "settings.json"

def get_config():
    default_config = {
        "threads_link": "https://www.threads.com/",
        "llm_link": "https://chatgpt.com/",
        "prompt": "Твой промпт здесь...",
        "filter_enabled": True,
        "filter_text": "ИИ, автоматизация, Threads"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_config
    return default_config

def save_config(new_data):
    try:
        current = get_config()
        current.update(new_data)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def get_ui_script(config):
    threads_val = config.get("threads_link", "")
    llm_val = config.get("llm_link", "")
    prompt_val = config.get("prompt", "").replace("\n", "\\n").replace("'", "\\'")
    
    filter_enabled = str(config.get("filter_enabled", True)).lower()
    filter_text = config.get("filter_text", "").replace("'", "\\'")

    return f"""
    if (!document.getElementById('bot-ui-root')) {{
        const root = document.createElement('div');
        root.id = 'bot-ui-root';
        document.body.appendChild(root);

        const bottomBar = document.createElement('div');
        bottomBar.style.cssText = 'position: fixed; bottom: 0; left: 0; width: 100%; height: 160px; background: #121212; border-top: 1px solid #333; z-index: 9999990; display: flex; font-family: monospace; box-shadow: 0 -5px 20px rgba(0,0,0,0.8);';

        const logArea = document.createElement('div');
        logArea.id = 'bot-log-area';
        logArea.style.cssText = 'flex: 1; padding: 10px; overflow-y: auto; color: #00ff00; font-size: 12px; border-right: 1px solid #333; background: #000;';

        const controlsArea = document.createElement('div');
        controlsArea.style.cssText = 'width: 200px; padding: 15px; display: flex; flex-direction: column; gap: 10px; justify-content: center; background: #1a1a1a;';

        const btnStart = document.createElement('button');
        btnStart.id = 'bot-btn-start';
        btnStart.innerText = 'СТАРТ';
        btnStart.style.cssText = 'width: 100%; padding: 12px; background: #28a745; color: white; border: none; font-weight: bold; cursor: pointer; border-radius: 4px; font-size: 14px; transition: 0.2s;';

        const btnSettings = document.createElement('button');
        btnSettings.innerText = 'НАСТРОЙКИ';
        btnSettings.style.cssText = 'width: 100%; padding: 10px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; font-size: 12px; transition: 0.2s;';

        controlsArea.appendChild(btnStart);
        controlsArea.appendChild(btnSettings);
        bottomBar.appendChild(logArea);
        bottomBar.appendChild(controlsArea);
        root.appendChild(bottomBar);

        const modalOverlay = document.createElement('div');
        modalOverlay.id = 'bot-settings-modal';
        modalOverlay.style.cssText = 'display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999999; justify-content: center; align-items: center; backdrop-filter: blur(3px);';

        const modalContent = document.createElement('div');
        modalContent.style.cssText = 'background: #222; width: 500px; padding: 25px; border-radius: 8px; border: 1px solid #444; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 15px; color: white; font-family: sans-serif; max-height: 90vh; overflow-y: auto;';

        const title = document.createElement('h3');
        title.innerText = 'Настройки бота';
        title.style.margin = '0 0 10px 0';
        title.style.borderBottom = '1px solid #444';
        title.style.paddingBottom = '10px';
        title.style.color = '#ffffff'; 
        title.style.fontSize = '20px';

        const createInput = (label, value, isArea) => {{
            const wrap = document.createElement('div');
            wrap.style.display = 'flex';
            wrap.style.flexDirection = 'column';
            wrap.style.gap = '5px';
            
            const lbl = document.createElement('label');
            lbl.innerText = label;
            lbl.style.fontSize = '12px';
            lbl.style.color = '#aaa';

            let el;
            if(isArea) {{
                el = document.createElement('textarea');
                el.style.height = '80px';
                el.style.resize = 'vertical';
            }} else {{
                el = document.createElement('input');
            }}
            el.value = value;
            el.style.cssText += 'padding: 8px; background: #333; border: 1px solid #555; color: white; border-radius: 4px; font-family: monospace; outline: none;';
            el.onfocus = () => el.style.borderColor = '#007bff';
            el.onblur = () => el.style.borderColor = '#555';

            wrap.appendChild(lbl);
            wrap.appendChild(el);
            return {{wrap, el}};
        }};

        const createToggleInput = (label, isChecked, textValue) => {{
            const wrap = document.createElement('div');
            wrap.style.display = 'flex';
            wrap.style.flexDirection = 'column';
            wrap.style.gap = '5px';
            wrap.style.marginTop = '5px';
            wrap.style.border = '1px solid #444';
            wrap.style.padding = '10px';
            wrap.style.borderRadius = '4px';

            const headerRow = document.createElement('div');
            headerRow.style.display = 'flex';
            headerRow.style.justifyContent = 'space-between';
            headerRow.style.alignItems = 'center';

            const lbl = document.createElement('label');
            lbl.innerText = label;
            lbl.style.fontSize = '12px';
            lbl.style.color = '#aaa';

            const chk = document.createElement('input');
            chk.type = 'checkbox';
            chk.checked = isChecked;
            chk.style.cursor = 'pointer';
            chk.style.transform = 'scale(1.2)';

            headerRow.appendChild(lbl);
            headerRow.appendChild(chk);

            const txt = document.createElement('input');
            txt.value = textValue;
            txt.style.cssText = 'padding: 8px; background: #333; border: 1px solid #555; color: white; border-radius: 4px; font-family: monospace; outline: none; margin-top: 5px;';
            txt.onfocus = () => txt.style.borderColor = '#007bff';
            txt.onblur = () => txt.style.borderColor = '#555';

            wrap.appendChild(headerRow);
            wrap.appendChild(txt);

            return {{wrap, chk, txt}};
        }};

        const inpThreads = createInput('Threads Link', '{threads_val}', false);
        const inpLLM = createInput('ChatGPT Link', '{llm_val}', false);
        const inpFilter = createToggleInput('Filter (Вкл/Выкл)', {filter_enabled}, '{filter_text}');
        const inpPrompt = createInput('Prompt', '{prompt_val}', true);

        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display: flex; gap: 10px; margin-top: 10px; justify-content: flex-end;';

        const btnSave = document.createElement('button');
        btnSave.innerText = 'Сохранить';
        btnSave.style.cssText = 'padding: 8px 20px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight: bold;';

        const btnCancel = document.createElement('button');
        btnCancel.innerText = 'Отмена';
        btnCancel.style.cssText = 'padding: 8px 15px; background: transparent; color: #aaa; border: 1px solid #555; cursor: pointer; border-radius: 4px;';

        btnRow.appendChild(btnCancel);
        btnRow.appendChild(btnSave);

        modalContent.appendChild(title);
        modalContent.appendChild(inpThreads.wrap);
        modalContent.appendChild(inpLLM.wrap);
        modalContent.appendChild(inpFilter.wrap);
        modalContent.appendChild(inpPrompt.wrap);
        modalContent.appendChild(btnRow);
        modalOverlay.appendChild(modalContent);
        root.appendChild(modalOverlay);

        window.botState = {{
            running: false,
            saveRequested: false,
            newConfig: {{}}
        }};

        btnStart.onclick = function() {{
            window.botState.running = !window.botState.running;
            updateBtnUI();
        }};

        function updateBtnUI() {{
            if (window.botState.running) {{
                btnStart.innerText = 'СТОП';
                btnStart.style.background = '#dc3545';
            }} else {{
                btnStart.innerText = 'СТАРТ';
                btnStart.style.background = '#28a745';
            }}
        }}

        window.forceStop = function() {{
            window.botState.running = false;
            updateBtnUI();
        }};

        btnSettings.onclick = () => modalOverlay.style.display = 'flex';
        btnCancel.onclick = () => modalOverlay.style.display = 'none';

        btnSave.onclick = () => {{
            window.botState.newConfig = {{
                threads_link: inpThreads.el.value.trim(),
                llm_link: inpLLM.el.value.trim(),
                prompt: inpPrompt.el.value,
                filter_enabled: inpFilter.chk.checked,
                filter_text: inpFilter.txt.value.trim()
            }};
            window.botState.saveRequested = true;
            modalOverlay.style.display = 'none';
        }};

        window.addBotLog = function(msg, isError) {{
            const div = document.createElement('div');
            div.innerText = '> ' + msg;
            div.style.marginBottom = '4px';
            if (isError) div.style.color = '#ff4444';
            logArea.appendChild(div);
            logArea.scrollTop = logArea.scrollHeight;
        }};
    }}
    """

def create_auth_html(threads_link, llm_link):
    return f"""
    <div style="background: rgba(0, 0, 0, 0.8); padding: 40px; border: 2px solid #333; border-radius: 10px; text-align: center; box-shadow: 0 0 20px rgba(0,0,0,0.5);">
        <h2 style="margin-top: 0; color: #ff4444;">АВТОРИЗУЙТЕСЬ В:</h2>
        <ul style="list-style: none; padding: 0; font-size: 18px; line-height: 2;">
            <li style="margin-bottom: 10px;"><a href="{threads_link}" target="_blank" style="color: #4da6ff; text-decoration: none; border-bottom: 1px dashed #4da6ff;">{threads_link}</a></li>
            <li><a href="{llm_link}" target="_blank" style="color: #4da6ff; text-decoration: none; border-bottom: 1px dashed #4da6ff;">{llm_link}</a></li>
        </ul>
        <p style="margin-top: 30px; font-weight: bold; font-size: 16px;">А затем закройте браузер.</p>
        <p style="color: #888; margin-top: 20px; font-size: 12px;">Что-бы завершить скрипт, нажмите CTRL+C.</p>
    </div>
    """

def is_profile_empty():
    if not os.path.exists(PROFILE_DIR):
        return True
    return not os.listdir(PROFILE_DIR)

def log_to_browser(driver, msg, is_error=False):
    try:
        safe_msg = msg.replace("'", "\\'").replace("\n", " ")
        err_bool = "true" if is_error else "false"
        driver.execute_script(f"if(window.addBotLog) window.addBotLog('{safe_msg}', {err_bool});")
    except:
        pass

def stop_browser_bot(driver):
    try:
        driver.execute_script("if(window.forceStop) window.forceStop();")
    except:
        pass

def launch_browser():
    config = get_config()
    first_run = is_profile_empty()
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options, use_subprocess=True, version_main=142)
    driver.maximize_window()
    
    bad_urls = ["https://chatgpt.com/", "https://chatgpt.com", "chatgpt.com/", "https://chatgpt.com", "chatgpt.com"]

    try:
        if first_run:
            driver.get("about:blank")
            html_content = create_auth_html(config.get("threads_link"), config.get("llm_link"))
            
            js_code = f"""
            document.body.style.margin = '0';
            document.body.style.padding = '0';
            document.body.style.backgroundColor = '#1a1a1a';
            document.body.style.color = 'white';
            document.body.style.fontFamily = 'monospace';
            document.body.style.height = '100vh';
            document.body.style.display = 'flex';
            document.body.style.alignItems = 'center';
            document.body.style.justifyContent = 'center';
            document.body.innerHTML = arguments[0];
            """
            driver.execute_script(js_code, html_content)
            
            while True:
                try:
                    driver.current_url
                    time.sleep(1)
                except:
                    break
        else:
            t_link = config.get("threads_link", "https://www.threads.com/")
            l_link = config.get("llm_link", "https://chatgpt.com/").replace("'", "\\'")
            
            driver.get(t_link)
            driver.execute_script(f"window.open('{l_link}', '_blank');")
            
            try:
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass

            while True:
                try:
                    script = get_ui_script(config)
                    driver.execute_script(script)
                    
                    state = driver.execute_script("return window.botState;")
                    
                    if state:
                        if state.get("saveRequested"):
                            new_conf = state.get("newConfig", {})
                            save_config(new_conf)
                            config = get_config() 
                            driver.execute_script("window.botState.saveRequested = false;")
                            log_to_browser(driver, "СИСТЕМА: Настройки сохранены и синхронизированы.")

                        if state.get("running"):
                            current_llm = config.get("llm_link", "")
                            if current_llm in bad_urls:
                                log_to_browser(driver, "ОШИБКА: Создайте чат в ChatGPT и введите ссылку в настройках.", True)
                                stop_browser_bot(driver)
                            else:
                                pass

                    time.sleep(1)
                except WebDriverException:
                    break
                except Exception:
                    time.sleep(1)
                
    except Exception:
        pass
    finally:
        try:
            driver.quit()
        except:
            pass

def main_loop():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)

    while True:
        try:
            launch_browser()
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()
        except Exception:
            time.sleep(2)

if __name__ == "__main__":
    main_loop()