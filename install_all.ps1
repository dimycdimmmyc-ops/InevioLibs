Get-ChildItem "E:\InevioLibs\dist\*.whl" | ForEach-Object {
    python -m pip install $_.FullName --force-reinstall
}
Write-Host "Библиотеки установлены в текущий Python" -ForegroundColor Green
