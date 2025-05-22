from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import os
import base64
import shutil
import random
import string
from seleniumbase import SB
from seleniumbase import config as sb_config
from fake_headers import Headers

app = FastAPI()
output_folder = "result_image"
os.makedirs(output_folder, exist_ok=True)

class Prompt(BaseModel):
    prompt: str

def generate_image(prompt: str):
    # User-Agent
    headers = Headers(browser="chrome", os="win", headers=True).generate()
    sb_config.settings.USER_AGENT = headers["User-Agent"]

    # Profil random
    profile_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    user_data_path = os.path.join(os.getcwd(), "chrome_profiles", profile_id)
    if os.path.exists(user_data_path):
        shutil.rmtree(user_data_path, ignore_errors=True)

    sb_config.settings.CHROME_OPTIONS_LIST = [
        f"--user-data-dir={user_data_path}",
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--disable-popup-blocking",
        "--start-maximized",
        "--mute-audio",
    ]

    try:
        with SB(uc=True, headed=False, headless=True) as sb:
            sb.uc_open_with_reconnect("https://magicstudio.com/ai-art-generator/", 4)
            sb.wait_for_element_visible("//textarea[contains(@id, 'desc')]", timeout=15)
            sb.type("//textarea[contains(@id, 'desc')]", prompt)
            sb.click("#prompt-box > div > button")

            sb.wait_for_element_visible('//*[@id="__next"]/div/main/div[1]/div/img', timeout=120)
            img_src = sb.get_attribute('//*[@id="__next"]/div/main/div[1]/div/img', "src")

            if img_src.startswith("data:image"):
                header, encoded = img_src.split(",", 1)
                file_ext = header.split("/")[1].split(";")[0]
                filename = f"generated_{uuid.uuid4().hex}.{file_ext}"
                filepath = os.path.join(output_folder, filename)

                # Save file
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(encoded))

                # return base64
                return {
                    "status": "success",
                    "image_base64": encoded,
                    "mime_type": header.split(":")[1].split(";")[0],
                    "filename": filename,
                }
            else:
                return {"status": "failed", "message": "Format gambar tidak didukung"}
    except Exception as e:
        return {"status": "failed", "message": f"{type(e).__name__}: {e}"}

@app.post("/generate")
def generate(prompt: Prompt):
    return generate_image(prompt.prompt)
