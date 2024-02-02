I wanted offline versions of the symbols for Visual Studio 2022. 

The scripts assume that 
1. `symchk` is installed at the default location (`C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe`)
2. The `SYMSTORE_PATH` environment variable is set to the path of the symbol store, i.e. one managed by visual studio.
3. The `SYMCACHE_PATH` environment variable is set to the path of the symcache folder, for unmanaged symbols.


# symcache2executables.py
This script will search for all executables matching the symbol files in the symcache folder, then write the results to a file.

## Usage
`python3 symcache2executables.py <path to symcache folder> --output <output file>`
OR set the `SYMBOL_CACHE` environment variable to the path of the symcache folder and run the script without any arguments.

# symboldl.ps1
This script utilises the `symchk` tool to download the symbols to `SYMBOL_CACHE` for a given executable.
## Usage
`.\symboldl.ps1 <path to executable>`

or, for iterating through `executables.txt`

`ForEach ($exe in Get-Content .\executables.txt) { .\symboldl.ps1 $exe }`
