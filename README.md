# jumparound

Quickly jump around between your projects.

## Installation

`jumparound` is part of the `m-porter/tap` brew cask.

1. `brew tap m-porter/tap`
2. `brew install m-porter/tap/jumparound`

## Usage

`jumparound` can be used on its own or as a part of other scripts. The most common usage is in
conjunction with `cd`.

When installing with `brew`, helper scripts are installed. They can be sourced so you don't have to do any other manual setup.
```sh
source "$(brew --prefix jumparound)/jumparound.sh"
# jumparound shortcut is "j"
```

If you may already have a function `j` on your system, you can specify your own function name for jumparound by exporting `JUMPAROUND_FUNC`.
```sh
export JUMPAROUND_FUNC="ja"
source "$(brew --prefix jumparound)/jumparound.sh"
# jumparound shortcut is now "ja"
```

## Development

### Setup

* Have python `poetry` installed.
* Clone this repository.
* Run `make setup`

### Generate `resource` blocks for the brew Formula

* `poetry run ./scripts/gen-formula.py`

### Using the `scripts/hooks/`

* `./scripts/setup-hooks.sh`
