from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="acs-zeep-client",
    version="1.0.0",
    author="Apollo Tech",
    author_email="marc@apolloglobal.net",
    description="Python client library for ACS ZEEP Backend API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/apollotech/acs-zeep-client",
    project_urls={
        "Bug Reports": "https://gitlab.com/apollotech/acs-zeep-client/-/issues",
        "Source": "https://gitlab.com/apollotech/acs-zeep-client",
        "Documentation": "https://gitlab.com/apollotech/acs-zeep-client/-/blob/main/README.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "acs-zeep-cli=acs_zeep_client.cli:main",
        ],
    },
)
