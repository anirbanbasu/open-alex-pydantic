<!-- ![GitHub commits since latest release](https://img.shields.io/github/commits-since/anirbanbasu/open-alex-pydantic/latest)
 [![PyPI](https://img.shields.io/pypi/v/open-alex-pydantic?label=pypi%20package)](https://pypi.org/project/open-alex-pydantic/#history)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/open-alex-pydantic?label=pypi%20downloads)](https://pypi.org/project/open-alex-pydantic/) -->

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=3776ab&labelColor=e4e4e4)](https://www.python.org/downloads/release/python-3120/) [![pytest](https://github.com/anirbanbasu/open-alex-pydantic/actions/workflows/uv-pytest-coverage.yml/badge.svg)](https://github.com/anirbanbasu/open-alex-pydantic/actions/workflows/uv-pytest-coverage.yml) [![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/anirbanbasu/open-alex-pydantic/badge)](https://scorecard.dev/viewer/?uri=github.com/anirbanbasu/open-alex-pydantic)

# Open Alex Pydantic

Open Alex API data structures as Pydantic classes.

## Usage

Don't use it unless you know what you're doing as this is a _very_ work-in-progress project!

```python
from open_alex_pydantic.entities import WorkParsingError, parse_work

try:
	work = parse_work(payload)
except WorkParsingError as exc:
	# Domain-level parse contract for invalid payloads.
	print(exc)
	print(exc.cause)
```
