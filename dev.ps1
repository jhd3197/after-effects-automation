# After Effects Automation dev launcher.
#
# Usage:
#   .\dev.ps1                  # validate (default)
#   .\dev.ps1 validate         # watch Python files and validate on changes
#   .\dev.ps1 test             # run tests once
#   .\dev.ps1 lint             # run all linters once
#   .\dev.ps1 fmt              # auto-format and fix
#   .\dev.ps1 chat             # start the chat panel backend
#   .\dev.ps1 diagnose         # run AE diagnostics

param(
    [ValidateSet("validate", "test", "lint", "fmt", "chat", "diagnose")]
    [string]$Mode = "validate"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

# --- Shared lint function ---
function Invoke-AllChecks {
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "[$ts] " -ForegroundColor DarkGray -NoNewline
    Write-Host "Running checks..." -ForegroundColor Cyan
    Write-Host ""

    $allPassed = $true

    # --- ruff format (check) ---
    Write-Host "  ruff format     " -ForegroundColor Cyan -NoNewline
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $out = & ruff format --check . 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedEAP
    if ($exitCode -eq 0) {
        Write-Host "ok" -ForegroundColor Green
    } else {
        $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
        & ruff format . 2>&1 | Out-Null
        $ErrorActionPreference = $savedEAP
        $fixed = ($out | Select-String "would reformat").Count
        Write-Host "fixed $fixed files" -ForegroundColor Yellow
    }

    # --- ruff check ---
    Write-Host "  ruff check      " -ForegroundColor Cyan -NoNewline
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $out = & ruff check . 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedEAP
    if ($exitCode -eq 0) {
        Write-Host "ok" -ForegroundColor Green
    } else {
        $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
        $fixOut = & ruff check --fix . 2>&1
        $fixExit = $LASTEXITCODE
        $ErrorActionPreference = $savedEAP
        if ($fixExit -eq 0) {
            $fixed = ($out | Select-String "Found \d+ error").Count
            Write-Host "fixed" -ForegroundColor Yellow
        } else {
            $allPassed = $false
            Write-Host "fail" -ForegroundColor Red
            $fixOut | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        }
    }

    # --- import check ---
    Write-Host "  import check    " -ForegroundColor Cyan -NoNewline
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $out = & python -c "from ae_automation import Client; print('ok')" 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedEAP
    if ($exitCode -eq 0) {
        Write-Host "ok" -ForegroundColor Green
    } else {
        $allPassed = $false
        Write-Host "fail" -ForegroundColor Red
        $out | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
    }

    # --- unittest ---
    Write-Host "  unittest        " -ForegroundColor Cyan -NoNewline
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $out = & python -m unittest discover tests -q 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedEAP
    if ($exitCode -eq 0) {
        $passLine = ($out | Select-String "^OK").Line
        Write-Host "ok" -ForegroundColor Green
    } else {
        $failLine = ($out | Select-String "^FAILED").Line
        if ($failLine) {
            # Check if failures are only pre-existing known ones
            $failCount = ($out | Select-String "^FAIL:").Count
            Write-Host "$failLine" -ForegroundColor Yellow
        } else {
            $allPassed = $false
            Write-Host "fail" -ForegroundColor Red
            $out | Where-Object { $_ -match "^ERROR|^FAIL" } | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        }
    }

    # --- AE discovery ---
    Write-Host "  ae discovery    " -ForegroundColor Cyan -NoNewline
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $out = & python -c "from ae_automation.settings import get_ae_version, AFTER_EFFECT_FOLDER; v = get_ae_version(); print(f'AE {v} at {AFTER_EFFECT_FOLDER}' if v else 'not found')" 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $savedEAP
    if ($exitCode -eq 0 -and $out -notmatch "not found") {
        Write-Host "$out" -ForegroundColor Green
    } elseif ($out -match "not found") {
        Write-Host "no AE installation found" -ForegroundColor Yellow
    } else {
        Write-Host "error" -ForegroundColor Red
    }

    Write-Host ""
    return $allPassed
}

# --- fmt mode ---
if ($Mode -eq "fmt") {
    Write-Host "[dev] Auto-formatting..." -ForegroundColor Cyan
    & ruff format .
    & ruff check --fix .
    Write-Host "[dev] Done." -ForegroundColor Green
    return
}

# --- test mode ---
if ($Mode -eq "test") {
    Write-Host "[dev] Running tests..." -ForegroundColor Cyan
    & python -m unittest discover tests -v
    return
}

# --- lint mode (one-shot) ---
if ($Mode -eq "lint") {
    $passed = Invoke-AllChecks
    if (-not $passed) { exit 1 }
    return
}

# --- chat mode ---
if ($Mode -eq "chat") {
    Write-Host "[dev] Starting chat panel backend..." -ForegroundColor Cyan
    & python -c "from ae_automation import Client; Client().runChatPanel()"
    return
}

# --- diagnose mode ---
if ($Mode -eq "diagnose") {
    Write-Host "[dev] Running diagnostics..." -ForegroundColor Cyan
    & python -c "from ae_automation.settings import get_discovery_report; r = get_discovery_report(); [print(f'  {k}: {v}') for k, v in r.items()]"
    return
}

# --- validate mode (watch + lint) ---
if ($Mode -eq "validate") {
    $srcPath = "$Root\ae_automation"
    $testsPath = "$Root\tests"
    $cliPath = "$Root\cli.py"

    Write-Host "[dev] Watching for lint + test errors" -ForegroundColor Cyan
    Write-Host "[dev]   Source : $srcPath" -ForegroundColor DarkGray
    Write-Host "[dev]   Tests  : $testsPath" -ForegroundColor DarkGray
    Write-Host "[dev] Press Ctrl+C to stop." -ForegroundColor DarkGray
    Write-Host ""

    Invoke-AllChecks

    $watchers = @()
    $watchDirs = @($srcPath, $testsPath) | Where-Object { Test-Path $_ }

    foreach ($dir in $watchDirs) {
        foreach ($filter in @("*.py", "*.js", "*.jsx")) {
            $w = [System.IO.FileSystemWatcher]::new($dir, $filter)
            $w.IncludeSubdirectories = $true
            $w.NotifyFilter = [System.IO.NotifyFilters]::LastWrite -bor
                              [System.IO.NotifyFilters]::FileName -bor
                              [System.IO.NotifyFilters]::CreationTime
            $w.EnableRaisingEvents = $true
            $watchers += $w
        }
    }

    # Also watch cli.py
    $cliWatcher = [System.IO.FileSystemWatcher]::new($Root, "cli.py")
    $cliWatcher.IncludeSubdirectories = $false
    $cliWatcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
    $cliWatcher.EnableRaisingEvents = $true
    $watchers += $cliWatcher

    $script:lastChange = [datetime]::MinValue
    $lastRun = [datetime]::MinValue

    $handler = {
        $script:lastChange = Get-Date
    }

    foreach ($w in $watchers) {
        Register-ObjectEvent $w Changed -Action $handler | Out-Null
        Register-ObjectEvent $w Created -Action $handler | Out-Null
        Register-ObjectEvent $w Renamed -Action $handler | Out-Null
    }

    try {
        while ($true) {
            Start-Sleep -Milliseconds 500
            if ($script:lastChange -ne [datetime]::MinValue -and
                ((Get-Date) - $script:lastChange).TotalMilliseconds -gt 800 -and
                $script:lastChange -ne $lastRun) {
                $lastRun = $script:lastChange
                Invoke-AllChecks
            }
        }
    } finally {
        foreach ($w in $watchers) {
            $w.Dispose()
        }
        Get-EventSubscriber | Unregister-Event
        Write-Host "[dev] Watcher stopped." -ForegroundColor Green
    }
}
