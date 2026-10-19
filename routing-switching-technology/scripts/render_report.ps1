param(
    [string]$Job = "",
    [string]$Docx = "",
    [string]$OutDir = "",
    [string]$Pdftoppm = "",
    [int]$Dpi = 100
)

# Preferred: render.json {"docx": "...", "outdir": "...", "pdftoppm": "...", "dpi": 100}
# Paths must live in the JSON because this console mangles non-ASCII argv.
if ($Job) {
    $spec = Get-Content -LiteralPath $Job -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $Docx) { $Docx = [string]$spec.docx }
    if (-not $OutDir) { $OutDir = [string]$spec.outdir }
    if (-not $Pdftoppm) { $Pdftoppm = [string]$spec.pdftoppm }
    if ($spec.dpi) { $Dpi = [int]$spec.dpi }
}

$Docx = [string]$Docx
$OutDir = [string]$OutDir
$Pdftoppm = [string]$Pdftoppm

if (-not $Docx) { throw "Missing -Docx or job.docx" }
if (-not $OutDir) { $OutDir = [string](Join-Path (Split-Path -Parent $Docx) "_render") }

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
# Cast Join-Path output: passing its PSObject wrapper to Word COM can hang.
$pdf = [string](Join-Path $OutDir "report.pdf")
if (Test-Path -LiteralPath $pdf) { Remove-Item -LiteralPath $pdf -Force }

Write-Output "opening: $Docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.AutomationSecurity = 3
try {
    $document = $word.Documents.Open($Docx, $false, $true)
    Write-Output "opened; exporting..."
    # SaveAs2 works reliably with modern Word; legacy SaveAs([ref]...) can
    # throw "Cannot convert ... psobject" or hang on some installs.
    $document.SaveAs2($pdf, 17)
    $document.Close($false)
}
finally {
    $word.Quit()
}
Write-Output "pdf done: $pdf"

if (-not $Pdftoppm) {
    $command = Get-Command pdftoppm.exe -ErrorAction SilentlyContinue
    if ($command) {
        $Pdftoppm = $command.Source
    }
    else {
        # Shallow, predictable locations only: a full -Recurse over the runtime
        # cache can take minutes.
        $candidate = Get-ChildItem -Path `
            "$env:USERPROFILE\.cache\codex-runtimes\*\dependencies\native\poppler\Library\bin\pdftoppm.exe", `
            "$env:USERPROFILE\.cache\codex-runtimes\*\*\dependencies\native\poppler\Library\bin\pdftoppm.exe" `
            -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($candidate) { $Pdftoppm = $candidate.FullName }
    }
}
if (-not $Pdftoppm) {
    throw "pdftoppm.exe not found. Set pdftoppm in the job file."
}

$pages = Join-Path $OutDir "pages"
New-Item -ItemType Directory -Path $pages -Force | Out-Null
& $Pdftoppm -r $Dpi -png $pdf (Join-Path $pages "page")

$pageCount = (Get-ChildItem -LiteralPath $pages -Filter "*.png" | Measure-Object).Count
Write-Output "pdf:   $pdf"
Write-Output "pages: $pageCount -> $pages"
