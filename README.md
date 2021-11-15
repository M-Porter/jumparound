# jumparound

Quickly jump around between your projects.

## Installation

`jumparound` is part of the `m-porter/tap` brew cask.

1. `brew tap m-porter/tap`
2. `brew install m-porter/tap/jumparound`

## Usage

`jumparound` can be used on its own or as a part of other scripts. The most common usage is in
conjunction with `cd`.

```
cd "$(jumparound to)"
```

or

```
j() {
    cd "$(jumparound to)" || return
}
```

You can also source the shell script in `bin/jumparound.sh`. If you may already have a function `j` on your system, you can specify your own function name for jumparound by exporting `JUMPAROUND_FUNC`.


## Development

### Setup

* Have python `poetry` installed.
* Clone this repository.
* Run `make setup`

### Generate `resource` blocks for the brew Formula

* `poetry run ./scripts/gen-formula.py`

### Using the `scripts/hooks/`

* `./scripts/setup-hooks.sh`
