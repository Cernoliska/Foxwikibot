# script/example.py

def run(session, api_url, get_csrf):
    user = input("Target: ").strip()
    reason = input("Rollback reason: ").strip() or "Rollback otomatis FoxWikiBot"
    token = get_csrf()

    r = session.post(api_url, data={
        "action": "rollback",
        "user": user,
        "token": token,
        "summary": reason,
        "format": "json"
    }).json()

    if "error" in r:
        print("Gagal rollback:", r["error"])
    else:
        print("Rollback berhasil untuk", user)
