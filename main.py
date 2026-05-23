import argparse
import time
import httpx

API_BASE = "https://client.ind.freefiremobile.com/api/v1"

def login_guest(uid, password):
    """Submits the exact msdk credentials straight to Garena's authentication servers"""
    url = f"{API_BASE}/login/guest"
    headers = {"Content-Type": "application/json", "User-Agent": "FFClient/1.104.X"}
    payload = {
        "guest_uid": uid,
        "guest_password": password,
        "device_model": "HeadlessLinuxVM"
    }
    try:
        with httpx.Client() as client:
            res = client.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                print(f"[{uid}] Silent Authentication Success.")
                return res.json().get("session_key")
            print(f"[{uid}] Login Denied. Code: {res.status_code}")
    except Exception as e:
        print(f"Network error handling login for {uid}: {e}")
    return None

def send_guild_request(session_key, guild_id, uid):
    """Sends a silent join request payload straight to your target guild endpoint"""
    url = f"{API_BASE}/guild/apply"
    headers = {"Authorization": f"Bearer {session_key}", "Content-Type": "application/json"}
    payload = {"target_guild_uid": int(guild_id), "application_message": "Silent Bot Worker Entry"}
    try:
        with httpx.Client() as client:
            res = client.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                print(f"[{uid}] Guild Application sent successfully to Guild: {guild_id}.")
            else:
                print(f"[{uid}] Application pending/rejected. Code: {res.status_code}")
    except Exception as e:
        print(f"Request dropped for {uid}: {e}")

def queue_clash_squad(session_key, uid):
    """Simulates loading into a Clash Squad matchmaking match payload data block"""
    url = f"{API_BASE}/match/queue"
    headers = {"Authorization": f"Bearer {session_key}", "Content-Type": "application/json"}
    payload = {"game_mode": 2, "match_type": "Clash_Squad", "action": "start"}
    try:
        with httpx.Client() as client:
            res = client.post(url, json=payload, headers=headers)
            if res.status_code == 200:
                print(f"[{uid}] Clash Squad match initialized successfully.")
    except Exception as e:
        print(f"Matchmaking failure for {uid}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--guild", required=True)
    parser.add_argument("--uid1", required=True)
    parser.add_argument("--pass1", required=True)
    parser.add_argument("--uid2", required=True)
    parser.add_argument("--pass2", required=True)
    args = parser.parse_args()

    print("--- STEP 1: INITIALIZING GUEST SESSIONS ---")
    sess1 = login_guest(args.uid1, args.pass1)
    sess2 = login_guest(args.uid2, args.pass2)

    print("\n--- STEP 2: DISPATCHING SILENT GUILD JOIN REQUESTS ---")
    if sess1: send_guild_request(sess1, args.guild, args.uid1)
    if sess2: send_guild_request(sess2, args.guild, args.uid2)

    print("\n--- STEP 3: RE-ROUTING TO CONTINUOUS MATCH LOOPS ---")
    print("Action Required: Open your phone game client and ACCEPT both accounts into the guild now.")
    
    # Simulates continuous 4-minute matches to cycle daily glory values safely
    for match_round in range(1, 11):
        print(f"\nCycling Match Automation Loop #{match_round}")
        if sess1: queue_clash_squad(sess1, args.uid1)
        if sess2: queue_clash_squad(sess2, args.uid2)
        time.sleep(240) # Wait 4 minutes for match completion

    print("\nDaily automated session processing complete. Shutting down cloud container runner.")