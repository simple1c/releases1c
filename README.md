# releases1c
Package manager for release.1c.ru, ver: 0.2.1

# Installation

## Install package

```
pip install --upgrade agent1c_metrics
```

# Usage

## Get info

### Get list of available packages 
```
python -m releases1c info
```

### Get info about versions for package

```
python -m releases1c info Platform83
```

### Get list of files for provided version and package

```
python -m releases1c info Platform83 8.3.23.1912
```

### Get list of mirrors for provided package, version and filetype

```
python -m releases1c info Platform83 8.3.23.1912 setuptc.rar
```

# Contribution

## Install package in editable mode

```
pip install -e .
```

## Change version (major/minor/patch)

```
bumpver update --patch
```

## Build and publish the package

```
poetry publish --build
```