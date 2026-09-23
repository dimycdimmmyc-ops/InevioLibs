param([switch]$Exe, [switch]$SkipTests)
$root = "E:\InevioLibs"
New-Item -ItemType Directory -Path "$root\dist" -Force | Out-Null
foreach ($lib in @("supernode","sporerecon","stealth")) {
    Push-Location "$root\$lib"
    if (-not $SkipTests) {
        Write-Host "== TEST $lib ==" -ForegroundColor Cyan
        python -m unittest discover -s tests -v
    }
    Write-Host "== WHEEL $lib ==" -ForegroundColor Cyan
    python -m pip wheel . --no-deps -w "$root\dist"
    Pop-Location
}
if ($Exe) {
    foreach ($lib in @("supernode","sporerecon","stealth")) {
        Push-Location "$root\$lib"
        python -m PyInstaller --onefile --name "$lib-cli" "$lib\__main__.py"
        Copy-Item "dist\$lib-cli.exe" "$root\dist\" -Force
        Pop-Location
    }
}
Write-Host "ГОТОВО: wheel (и .exe) в E:\InevioLibs\dist" -ForegroundColor Green
