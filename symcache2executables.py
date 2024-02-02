import os
import sys
import argparse
import pathlib
import subprocess
import typing


# ordered in priority, as we should really stop once we find all the executables
EXECUTABLE_EXTENSIONS = (".dll", ".exe")
EXECUTABLE_SEARCH_PATHS = ( 
    "C:\\Windows\\System32",
    "C:\\Windows\\SysWOW64",
#     "C:\\Program Files",
#     "C:\\Program Files (x86)"
)

def where(path : str, pattern : str, recursive : bool = True) -> typing.List[pathlib.Path]:
    """ Wrapper for the Windows where command """
    if recursive:
        cmd = ["where", "/r", path, pattern]
    else:
        cmd = ["where", path + ':' + pattern]
    
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise FileNotFoundError(f"Could not find {pattern}")
    
    return [pathlib.Path(p) for p in result.stdout.splitlines()]

def symcache2symbols(symcache_path : pathlib.Path) -> list:
    """From a Visual Studio 22 symbol cache directory, return a list of symbols"""
    
    symbols = []
    
    for file in symcache_path.iterdir():
        if file.suffix == ".pdb":
            symbols.append(file)
            
    return symbols

def find_executables(symbols : list) -> list:
    """From a list of symbols, search for and return a list of executables"""
    
    found_symbols = []
    executables = []
    for search_path in EXECUTABLE_SEARCH_PATHS:
        for symbol in symbols:
            if symbol.stem in found_symbols:
                continue
            
            pattern = symbol.stem + ".*"
            try:
                results = where(search_path, pattern)
                for result in results:
                    if result.suffix in EXECUTABLE_EXTENSIONS:
                        executables.append(result)
                        found_symbols.append(symbol.stem)
                        print(f"INFO: Found {result} in {search_path}")
            except FileNotFoundError:
                print(f"INFO: Could not find {pattern} in {search_path}")
                continue
            
        # early exit if we have found all the executables
        if len(executables) == len(symbols):
            print("INFO: Found all executables - exiting early")
            break

    return executables

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find executables from a Visual Studio 22 symbol cache directory. If SYMBOL_CACHE environment variable is set and symchk is found, arguments are not needed and this dialog will be skipped.")
    parser.add_argument("symcache_path", type=pathlib.Path,  help="Path to the Visual Studio 22 symbol cache directory")
    parser.add_argument("-o", "--output", type=pathlib.Path, default="executables.txt", help="Output file for executables")
    parser.add_argument()
    return parser.parse_args()

def get_args() -> argparse.Namespace:
    
    if len(sys.argv) > 1:
        args = parse_args()
    
    elif "SYMBOL_CACHE" in os.environ and os.path.isdir(os.environ["SYMBOL_CACHE"]):
        args = argparse.Namespace(
            symcache_path=pathlib.Path(os.environ["SYMBOL_CACHE"]), 
            output=pathlib.Path("executables.txt")
        )

    else:
        args = parse_args()
        
    return args
        
def main():
    args = get_args()
    symbols = symcache2symbols(args.symcache_path)
    executables = find_executables(symbols)
        
    with open(args.output, "w") as f:
        for executable in executables:
            f.write(str(executable) + "\n")
            
    print(f"INFO: Wrote {len(executables)} executables to {args.output}")
    
    if len(symbols) > len(executables): print(f"WARN: {len(symbols) - len(executables)} symbols were not found")
    
if __name__ == "__main__":
    # either SYMBOL_CACHE or args[1] should exist as directory
    main()