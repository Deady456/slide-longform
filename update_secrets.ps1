# Update GitHub Secrets untuk semua channel
# Jalankan SETELAH yt_auth.py selesai untuk semua channel

$channels = @(
    @{repo="konten-1"; user="Deady456"},
    @{repo="konten-2"; user="Deady456"},
    @{repo="konten3"; user="Deady456"},
    @{repo="konten4"; user="Deady456"},
    @{repo="konten5"; user="Deady456"},
    @{repo="konten6"; user="Deady456"}
)

$credDir = "yt_credentials"

foreach ($ch in $channels) {
    $repo = $ch.repo
    $user = $ch.user
    $clientFile = "$credDir/${repo}_client_b64.txt"
    $tokenFile = "$credDir/${repo}_token_b64.txt"

    if (-not (Test-Path $clientFile) -or -not (Test-Path $tokenFile)) {
        Write-Warning "Skip $repo - file credentials tidak ditemukan"
        continue
    }

    $clientB64 = Get-Content $clientFile -Raw | ForEach-Object { $_.Trim() }
    $tokenB64 = Get-Content $tokenFile -Raw | ForEach-Object { $_.Trim() }

    Write-Host "Updating $user/$repo ..." -ForegroundColor Cyan

    # Set CLIENT_SECRET_B64
    gh secret set CLIENT_SECRET_B64 --repo "$user/$repo" --body "$clientB64" 2>&1 | Out-Null
    if ($?) { Write-Host "  CLIENT_SECRET_B64 ✅" -ForegroundColor Green }

    # Set TOKEN_B64
    gh secret set TOKEN_B64 --repo "$user/$repo" --body "$tokenB64" 2>&1 | Out-Null
    if ($?) { Write-Host "  TOKEN_B64 ✅" -ForegroundColor Green }
}

Write-Host "`nSelesai! Semua secret telah diupdate." -ForegroundColor Yellow
