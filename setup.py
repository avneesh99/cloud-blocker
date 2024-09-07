from setuptools import setup, find_packages

setup(
    name="cloud_blocker",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for blocking cloud IP addresses",
    long_description="sd",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cloud-blocker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)