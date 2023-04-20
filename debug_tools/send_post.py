import requests
import json


if __name__ == "__main__":
    url = "http://localhost:9000/webhook/card"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {
        "encrypt": "OXFPQeZXKOA9+tr5FjRR/uws2d9MMEhCrMde+oTe/l/Fe7XqiNqjWVt8dY/AzonGWetpUoExw026Ou6pa3jtQbK/ByMw6/RfhX1akLNbzPn1mqqGyrYF6WxkUccorA0qOns7gx8soi3Vq9r2d/Y/CdW+GXo3R2IemKOffs181fjIbIuUBgbSnPtQMm8Tg4TL"
    }

    r = requests.post(url, headers=headers, json=data)
    print(r.status_code)
    print(r.text)
