from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="police-forensics-ai",
    version="1.0.0",
    author="Gorang Singhal",
    author_email="gorang.singhal06@gmail.com",
    description="An enterprise-grade, secure evidence extraction system for law enforcement using Dual-Licensing GANs and LLM routing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GorangSinghal/PoliceForensicsAI",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cyber-terminal=app:main",
        ],
    },
)
