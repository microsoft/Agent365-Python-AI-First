# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

import os
import tomllib
from pathlib import Path

from setuptools import find_packages, setup


def read_pyproject():
    text = Path("pyproject.toml").read_text(encoding="utf-8")
    data = tomllib.loads(text)
    project = data["project"]
    name = project["name"]
    description = project["description"]
    required_py_version = project["requires-python"]
    return name, description, required_py_version


PROJECT_NAME, PROJECT_DESCRIPTION, REQUIRED_PY_VERSION = read_pyproject()

MODULE_NAME = (PROJECT_NAME or "microsoft-agents-a365").replace("-", "_")

# Get version from environment variable set by CI/CD
# This will be set by setuptools-git-versioning in the CI pipeline
VERSION = os.environ.get("AGENT365_PYTHON_SDK_PACKAGE_VERSION", "0.0.0")


# Write the version attr used by [tool.setuptools.dynamic].version
pkg_dir = Path(__file__).parent / MODULE_NAME
pkg_dir.mkdir(parents=True, exist_ok=True)
(pkg_dir / "_version.py").write_text(f'__version__ = "{VERSION}"\n', encoding="utf-8")

# We pass name/description that we just read, so you don't duplicate them.
# Version is provided via the dynamic attr above.
long_desc = Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else ""

setup(
    name=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    python_requires=REQUIRED_PY_VERSION,
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
)
