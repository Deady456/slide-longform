import base64, json, sys, os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def main():
    if len(sys.argv) < 2:
        print("Usage: python yt_auth.py <nama_channel>")
        print("Contoh: python yt_auth.py konten-2")
        sys.exit(1)

    channel = sys.argv[1]
    secret_path = "client_secret.json"

    if not os.path.exists(secret_path):
        print(f"ERROR: {secret_path} tidak ditemukan. Letakkan client_secret.json dari Google Cloud Console di folder ini.")
        sys.exit(1)

    print(f"\n=== AUTENTIKASI UNTUK CHANNEL: {channel} ===\n")
    print("Browser akan terbuka. Login dengan akun YouTube yang punya channel ini.")
    print("Setelah login, izinkan akses 'Manage your YouTube videos'.\n")

    flow = InstalledAppFlow.from_client_secrets_file(secret_path, SCOPES)
    creds = flow.run_local_server(port=8080)

    client_b64 = base64.b64encode(open(secret_path, "rb").read()).decode()
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    token_b64 = base64.b64encode(json.dumps(token_data).encode()).decode()

    print(f"\n=== HASIL untuk {channel} ===\n")
    print(f"CLIENT_SECRET_B64 (copy ini ke GitHub Secrets):")
    print(client_b64)
    print(f"\nTOKEN_B64 (copy ini ke GitHub Secrets):")
    print(token_b64)

    # Simpan ke file
    out_dir = "yt_credentials"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/{channel}_client_b64.txt", "w") as f:
        f.write(client_b64)
    with open(f"{out_dir}/{channel}_token_b64.txt", "w") as f:
        f.write(token_b64)
    print(f"\nJuga disimpan ke folder {out_dir}/")

if __name__ == "__main__":
    main()
