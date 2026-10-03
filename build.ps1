# Build script to package plugins into zip files
$pluginsDir = ".\plugins"
$releasesDir = ".\releases"

if (!(Test-Path -Path $releasesDir)) {
    New-Item -ItemType Directory -Path $releasesDir | Out-Null
}

$plugins = Get-ChildItem -Path $pluginsDir -Directory

foreach ($plugin in $plugins) {
    $pluginName = $plugin.Name
    # Read version from manifest
    $manifestPath = Join-Path $plugin.FullName "manifest.json"
    if (Test-Path $manifestPath) {
        $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
        $version = $manifest.version
        $zipName = "$pluginName.zip"
        
        $releaseSubDir = Join-Path $releasesDir "$pluginName-v$version"
        if (!(Test-Path $releaseSubDir)) {
            New-Item -ItemType Directory -Path $releaseSubDir | Out-Null
        }
        
        $zipPath = Join-Path $releaseSubDir $zipName
        if (Test-Path $zipPath) {
            Remove-Item $zipPath
        }
        
        Write-Host "Packaging $pluginName v$version -> $zipPath"
        Compress-Archive -Path "$($plugin.FullName)\*" -DestinationPath $zipPath -Force
    }
}
Write-Host "Done!"
