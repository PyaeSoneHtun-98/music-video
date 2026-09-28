param(
    [string]$SheetId = '',
    [switch]$SkipExisting
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$trackerPath = Join-Path $root 'production/shot-list.csv'
$rows = @(Import-Csv -LiteralPath $trackerPath)

# All approved combined sheets are 1672 x 941. Their gutters occupy x=832..839
# and y=468..472. Each clean quadrant is exactly 832 x 468 (16:9).
$expectedWidth = 1672
$expectedHeight = 941
$frameWidth = 832
$frameHeight = 468
$panels = @(
    @{ Number = '01'; X = 0; Y = 0 },
    @{ Number = '02'; X = 840; Y = 0 },
    @{ Number = '03'; X = 0; Y = 473 },
    @{ Number = '04'; X = 840; Y = 473 }
)

$processed = 0
foreach ($row in $rows) {
    if ($SheetId -and $row.sheet_id -ne $SheetId) { continue }
    if ($row.status -ne 'ready' -or $row.first_frame -or
        -not $row.storyboard.EndsWith('.png', [System.StringComparison]::OrdinalIgnoreCase)) {
        continue
    }

    $sourcePath = Join-Path $root $row.storyboard
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Missing approved sheet: $sourcePath"
    }

    $source = [System.Drawing.Bitmap]::new($sourcePath)
    try {
        if ($source.Width -ne $expectedWidth -or $source.Height -ne $expectedHeight) {
            throw "$($row.sheet_id): expected ${expectedWidth}x${expectedHeight}, got $($source.Width)x$($source.Height)"
        }

        foreach ($panel in $panels) {
            $shotId = "$($row.sheet_id)-$($panel.Number)"
            $relative = "frames/$shotId-input.png"
            $outputPath = Join-Path $root $relative
            if (Test-Path -LiteralPath $outputPath) {
                if (-not $SkipExisting) {
                    throw "Output exists; will not overwrite: $outputPath"
                }
                $existing = [System.Drawing.Image]::FromFile($outputPath)
                try {
                    if ($existing.Width -ne $frameWidth -or $existing.Height -ne $frameHeight) {
                        throw "Existing output has wrong dimensions: $outputPath"
                    }
                }
                finally { $existing.Dispose() }
                continue
            }

            $rectangle = [System.Drawing.Rectangle]::new(
                [int]$panel.X, [int]$panel.Y, $frameWidth, $frameHeight
            )
            $frame = $source.Clone($rectangle, $source.PixelFormat)
            try { $frame.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png) }
            finally { $frame.Dispose() }
            Write-Output "$shotId <- $($row.storyboard)"
        }
    }
    finally { $source.Dispose() }

    $row.first_frame = "frames/$($row.sheet_id)-01-input.png"
    $processed++
}

if ($SheetId -and $processed -eq 0) {
    throw "No ready combined sheet needing extraction matched $SheetId"
}

if ($processed -gt 0) {
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add('sheet_id,start_seconds,end_seconds,title,status,storyboard,first_frame')
    foreach ($row in $rows) {
        $lines.Add(($row.sheet_id, $row.start_seconds, $row.end_seconds, $row.title,
                    $row.status, $row.storyboard, $row.first_frame) -join ',')
    }
    [System.IO.File]::WriteAllLines(
        $trackerPath, $lines, [System.Text.UTF8Encoding]::new($false)
    )
}

Write-Output "Prepared $processed combined sheets."
