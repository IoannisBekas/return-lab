param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath
)

Add-Type -AssemblyName System.Drawing
[Windows.Globalization.Language,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Media.Ocr,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null

$fullPath = [System.IO.Path]::GetFullPath($ImagePath)
$fileTask = [Windows.Storage.StorageFile]::GetFileFromPathAsync($fullPath)
$file = $fileTask.GetAwaiter().GetResult()

$streamTask = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
$stream = $streamTask.GetAwaiter().GetResult()

$decoderTask = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
$decoder = $decoderTask.GetAwaiter().GetResult()

$bmpTask = $decoder.GetSoftwareBitmapAsync()
$bmp = $bmpTask.GetAwaiter().GetResult()

$lang = New-Object Windows.Globalization.Language("en-US")
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if (-not $engine) {
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
}

$ocrTask = $engine.RecognizeAsync($bmp)
$result = $ocrTask.GetAwaiter().GetResult()

Write-Host "=== OCR RESULTS FOR: $ImagePath ==="
foreach ($line in $result.Lines) {
    Write-Host $line.Text
}
