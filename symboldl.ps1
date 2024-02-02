# Usage: symboldl.ps1 <executable>
# Note: if the auto generated symbols are still present, the symbols will not be downloaded again!
$executable = $args[0]

# check for executable
if ($executable -eq $null -or $executable -eq "" -or -not (Test-Path $executable)) {
    echo "Usage: symboldl.ps1 <executable>"
    exit 1
}

# check SYMSTORE_PATH environment variable
if ($env:SYMSTORE_PATH -eq $null -or $env:SYMSTORE_PATH -eq "") {
    echo "SYMSTORE_PATH environment variable not set"
    exit 1
}

# check for symchk.exe, either as SYMCHK environment variable or in default location
$symchk = $env:SYMCHK
if ($symchk -eq $null -or $symchk -eq "" -or -not (Test-Path $symchk)) {
    $symchk = "C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe"
    if (-not (Test-Path $symchk)) {
        echo "symchk.exe not found"
        exit 1
    }
}

# download symbols
$symbol_server = "https://msdl.microsoft.com/download/symbols"
$cmd = "& `"$symchk`" /r `"$executable`" /s `"$symbol_server`" /od /oc `"$env:SYMSTORE_PATH`""

Invoke-Expression $cmd