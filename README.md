# squatdetect
Detect packages which might have been typosquatted based on string similarity level calculated from a dataset of popular packages.

```
usage: squatdetect.py [-h] [--type [{pip}]] [--packages PACKAGES [PACKAGES ...]]
                      [--confidence {1,2,3,4,5,6,7,8,9}]

Detect packages which might have been typosquatted based on string similarity
level calculated from a dataset of popular packages.
It can be coupled with a shell alias/function for pip/pip3 to prevent installing
typosquatted packages. No magic, just stdlib :)

For example:

function pip3 {
~/.local/bin/squatdetect.py --packages "${@: -1}" | grep 'might be impersonating' && return
$(which pip3) "$@"
}

options:
  -h, --help            show this help message and exit
  --type [{pip}]        Package type
  --packages PACKAGES [PACKAGES ...]
                        Package(s) to check, if no packages are specified, all installed packages
                        will be checked
  --confidence {1,2,3,4,5,6,7,8,9}
                        Level of confidence to be set. Default: 7
```

### Example

```
python3 squatdetect.py --packages baeutifulsoup4
**baeutifulsoup4** might be impersonating beautifulsoup4 (92.857143% similar)
**baeutifulsoup4** might be impersonating beautifulsoup (88.888889% similar)
```

with shell override to prevent on installation:

```
$ pip3 install baeutifulsoup4
**baeutifulsoup4** might be impersonating beautifulsoup4 (92.857143% similar)
**baeutifulsoup4** might be impersonating beautifulsoup (88.888889% similar)
$
```

### Supported package types

`pip`: The dataset is based on https://pypistats.org/ (`pip.json`)
