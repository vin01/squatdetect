# squatdetect
Detect packages which might have been typosquatted based on string similarity level calculated from a dataset of popular packages.

```
usage: squatdetect.py [-h] [--type [{pip,gem}]] [--packages PACKAGES [PACKAGES ...]]
                      [--confidence {1,2,3,4,5,6,7,8,9}]

Detect packages which might have been typosquatted based on string similarity
level calculated from a dataset of popular packages.
It can be coupled with shell aliases/functions to prevent installing
typosquatted packages which might happen just because we often mistype.
No magic, just stdlib :)

For example:

function pip3 {
if [[ -n "$1" ]] && [[ "$1" = 'install' ]]; then
  ~/.local/bin/squatdetect.py --packages "${@: -1}" | grep 'might be impersonating' && return
fi
$(which pip3) "$@"
}

function gem {
if [[ -n "$1" ]] && [[ "$1" = 'install' ]]; then
  ~/.local/bin/squatdetect.py --packages "${@: -1}" --type gem | grep 'might be impersonating' && return
fi
$(which gem) "$@"
}

options:
  -h, --help            show this help message and exit
  --type [{pip,gem}]    Package type. Default: pip
  --packages PACKAGES [PACKAGES ...]
                        Package(s) to check, if no packages are specified, all installed packages will be checked
  --confidence {1,2,3,4,5,6,7,8,9}
                        Level of confidence to be set. Default: 8
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

- `pip`: The dataset is based on https://pypistats.org/ (`pip.json`)
- `gem`: The dataset is based on weekly dumps from https://rubygems.org/pages/data


### Misc

- https://blog.phylum.io/pypi-malware-replaces-crypto-addresses-in-developers-clipboard
- https://blog.reversinglabs.com/blog/mining-for-malicious-ruby-gems
- https://medium.com/checkmarx-security/typosquatting-attack-on-requests-one-of-the-most-popular-python-packages-3b0a329a892d
