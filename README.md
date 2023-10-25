# releases1c
Package manager for release.1c.ru, ver: 1.0.0

# Installation

Install package

```
pip install --upgrade agent1c_metrics
```

# Usage

## Set authentication environment

Windows:

```
set RELEASES1C_USERNAME=<username>
set RELEASES1C_PASSWORD=<password>
```

Linux, Mac:

```
export RELEASES1C_USERNAME=<username>
export RELEASES1C_PASSWORD=<password>
```

## Get info

Get list of available packages 

```
python -m releases1c info
```

Get info about versions for package

```
python -m releases1c info Platform83
```

Get list of files for provided version and package

```
python -m releases1c info Platform83 8.3.23.1912
```

Get list of mirrors for provided package, version and filetype

```
python -m releases1c info Platform83 8.3.23.1912 setuptc.rar
```

## Download

Download file by its filetype into corrent folder

```
python -m releases1c info Platform83 8.3.23.1912 setuptc.rar .
```

# Contribution

Install package in editable mode

```
pip install -e .
```

Change version (major/minor/patch)

```
bumpver update --patch
```

Build and publish the package

```
poetry publish --build
```