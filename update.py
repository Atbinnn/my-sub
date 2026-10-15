import base64
import os
import urllib.parse
import requests

SUB_URL = os.environ.get("SUB_URL")

if not SUB_URL:
    raise ValueError("SUB_URL secret not found!")

headers = {
    "User-Agent": "v2rayNG/1.8.5"
}

response = requests.get(SUB_URL, headers=headers, timeout=15)
content = response.text.strip()

user_info = response.headers.get("subscription-userinfo", "")
info_dict = {}
if user_info:
    for part in user_info.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            try:
                info_dict[k.lower()] = int(v)
            except ValueError:
                pass

total_bytes = info_dict.get("total", 0)
upload_bytes = info_dict.get("upload", 0)
download_bytes = info_dict.get("download", 0)
used_bytes = upload_bytes + download_bytes
remaining_bytes = max(0, total_bytes - used_bytes)

if total_bytes > 0:
    rem_gb = remaining_bytes / (1024 ** 3)
    traffic_title = f"📊 Remaining: {rem_gb:.2f} GB"
else:
    traffic_title = "📊 Remaining: Unlimited"

traffic_dummy = f"vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?security=none&encryption=none&type=tcp#{traffic_title}"
telegram_dummy = "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?security=none&encryption=none&type=tcp#✈️ Telegram: @AtbiNNN"

try:
    decoded = base64.b64decode(content).decode("utf-8")
    lines = decoded.splitlines()
except Exception:
    lines = content.splitlines()

filtered_lines = [traffic_dummy, telegram_dummy]

for line in lines:
    line = line.strip()
    if not line:
        continue

    decoded_line = urllib.parse.unquote(line)

    if "👇" in decoded_line or "🔗" in decoded_line:
        continue

    filtered_lines.append(line)

output_text = "\n".join(filtered_lines)

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write(output_text)
