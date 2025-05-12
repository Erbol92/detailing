import json
import sys
import requests
SMARTCAPTCHA_SERVER_KEY = "ysc2_T5wAComf2dqR9UoOd9Fb4W1oJOHEFqUnP5IceQZk6ab6b06f"


# request.META['REMOTE_ADDR']
def get_client_ip(request):
    """получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_captcha(token, request):
    resp = requests.post(
        "https://smartcaptcha.yandexcloud.net/validate",
        data={
            "secret": SMARTCAPTCHA_SERVER_KEY,
            "token": token,
            "ip": get_client_ip(request)  # Способ получения IP-адреса зависит от вашего фреймворка и прокси.
        },
        timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
        print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
        return True
    return json.loads(server_output)["status"] == "ok"


# token = "<токен>"  # Например, request.form["smart-token"]
# if check_captcha(token,request):
#     print("Passed")
# else:
#     print("Robot")
