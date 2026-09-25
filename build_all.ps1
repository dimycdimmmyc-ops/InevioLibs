<#
.SYNOPSIS
    Builds the entire Inevio ecosystem:
    spore-net, spore-bridge, supernode, sporerecon, inevio-stealth.
#>
param(
    [switch]$SkipTests,
    [switch]$Exe
)

$ErrorActionPreference = "Stop"
$root = (Get-Item $PSScriptRoot).FullName
$dist = Join-Path $root "dist"

New-Item -ItemType Directory -Path $dist -Force | Out-Null

$packages = @(
    @{ Name = "spore-net";      Path = (Join-Path $root "spore-net");      HasTests = $false },
    @{ Name = "spore-bridge";   Path = (Join-Path $root "spore-bridge");   HasTests = $true  },
    @{ Name = "supernode";      Path = (Join-Path $root "supernode");      HasTests = $true  },
    @{ Name = "sporerecon";     Path = (Join-Path $root "sporerecon");     HasTests = $true  },
    @{ Name = "inevio-stealth"; Path = (Join-Path $root "inevio-stealth"); HasTests = $true  }
)

foreach ($p in $packages) {
    Write-Host ""
    Write-Host "=====================================================" -ForegroundColor Yellow
    Write-Host "  BUILD: $($p.Name)" -ForegroundColor Yellow
    Write-Host "=====================================================" -ForegroundColor Yellow

    if (-not (Test-Path $p.Path)) {
        Write-Host "  SKIP: path not found: $($p.Path)" -ForegroundColor Red
        continue
    }

    Push-Location $p.Path

    try {
        if ($p.HasTests -and -not $SkipTests) {
            Write-Host "  == TESTS ==" -ForegroundColor Cyan
            py -m unittest discover -s tests -v
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  TESTS FAILED for $($p.Name)" -ForegroundColor Red
                Pop-Location
                continue
            }
        }

        Write-Host "  == WHEEL ==" -ForegroundColor Cyan
        py -m pip wheel . --no-deps -w $dist
    }
    finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  DONE. Packages in $dist" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Get-ChildItem $dist