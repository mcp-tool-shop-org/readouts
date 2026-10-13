# Read text aloud with Kokoro neural TTS, falling back to Windows SAPI5.
# Zed tasks pass -Text or -Clipboard.
param(
    [string]$Text = "",
    [switch]$Clipboard
)

$ErrorActionPreference = "Stop"

$pidFile = Join-Path $PSScriptRoot "speaker.pid"
if (Test-Path $pidFile) {
    $oldId = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($oldId -and [int]$oldId -ne $PID) {
        Stop-Process -Id ([int]$oldId) -Force -ErrorAction SilentlyContinue
    }
}
Set-Content -Path $pidFile -Value $PID

if ($Clipboard) {
    $Text = Get-Clipboard -Raw
} elseif ([string]::IsNullOrWhiteSpace($Text)) {
    $Text = $env:ZED_SELECTED_TEXT
    if ([string]::IsNullOrWhiteSpace($Text)) {
        $Text = Get-Clipboard -Raw
    }
}

if ([string]::IsNullOrWhiteSpace($Text)) {
    Write-Output "Nothing to read. Select some text, or copy a reply, then try again."
    exit 1
}

# Drop fence markers so a copied code block is listenable.
$Text = $Text -replace '```+', ' '

$voice = if ($env:ZED_SPEAK_VOICE) { $env:ZED_SPEAK_VOICE } else { "af_heart" }
$rate = 0
if ($env:ZED_SPEAK_RATE -match '^-?\d+$') {
    $rate = [int]$env:ZED_SPEAK_RATE
    if ($rate -lt -10) { $rate = -10 }
    if ($rate -gt 10)  { $rate = 10 }
}

# If voice looks like a legacy Windows voice, use the old path.
$useLegacy = $voice -like "Microsoft*"

if (-not $useLegacy) {
    $tempWav = $null
    $tempTxt = $null
    $pyFile = $null
    try {
        $speed = 1.0 + ($rate / 20.0)
        $tempWav = Join-Path $env:TEMP "zed_speak_$PID.wav"
        $tempTxt = Join-Path $env:TEMP "zed_speak_$PID.txt"
        $pyFile  = Join-Path $PSScriptRoot "kokoro_gen.py"

        # Write text to a temp file so we don't have to escape it for Python.
        Set-Content -Path $tempTxt -Value $Text -Encoding UTF8

        # Ensure the Python helper exists.
        if (-not (Test-Path $pyFile)) {
            $pySrc = @'
import sys, warnings
warnings.filterwarnings('ignore')
from kokoro import KPipeline
import soundfile as sf

text_file = sys.argv[1]
voice      = sys.argv[2]
speed      = float(sys.argv[3])
wav_file   = sys.argv[4]

with open(text_file, 'r', encoding='utf-8') as f:
    text = f.read()

pipeline = KPipeline(lang_code='a')
generator = pipeline(text, voice=voice, speed=speed)
for i, (gs, ps, audio) in enumerate(generator):
    sf.write(wav_file, audio, 24000)
    break
'@
            Set-Content -Path $pyFile -Value $pySrc -Encoding UTF8
        }

        $pyProc = Start-Process -FilePath "python" -ArgumentList "`"$pyFile`"", "`"$tempTxt`"", "`"$voice`"", $speed, "`"$tempWav`"" -Wait -PassThru -NoNewWindow
        if ($pyProc.ExitCode -ne 0) {
            throw "Kokoro generation exited with code $($pyProc.ExitCode)"
        }

        if (-not (Test-Path $tempWav)) {
            throw "Kokoro did not produce a WAV file"
        }

        $player = New-Object System.Media.SoundPlayer $tempWav
        $player.PlaySync()
    } catch {
        Write-Warning "Kokoro failed ($($_.Exception.Message)). Falling back to Windows voice."
        $useLegacy = $true
    } finally {
        if ($tempWav -and (Test-Path $tempWav)) { Remove-Item $tempWav -Force -ErrorAction SilentlyContinue }
        if ($tempTxt -and (Test-Path $tempTxt)) { Remove-Item $tempTxt -Force -ErrorAction SilentlyContinue }
    }
}

if ($useLegacy) {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

    $installed = @($synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name })
    if ($installed -contains $voice) {
        $synth.SelectVoice($voice)
    }

    $synth.Rate = $rate
    try {
        $synth.Speak($Text)
    } finally {
        $synth.Dispose()
    }
}

if ((Get-Content $pidFile -ErrorAction SilentlyContinue) -eq "$PID") {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}
