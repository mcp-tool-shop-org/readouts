# Cut off a voice that is still reading.
$pidFile = Join-Path $PSScriptRoot "speaker.pid"
if (Test-Path $pidFile) {
    $oldId = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($oldId) {
        Stop-Process -Id ([int]$oldId) -Force -ErrorAction SilentlyContinue
    }
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}
