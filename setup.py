from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="after-effects-automation",
    version='0.0.2',
    author="Juan Denis",
    author_email="juan@vene.co",
    description="A Python tool for automating Adobe After Effects workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhd3197/after-effects-automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv>=0.19.0",
        "pyautogui>=0.9.53",
        "pydirectinput>=1.0.4",
        "pywinauto>=0.6.8",
        "pandas>=1.3.0",
        "pydantic>=1.8.2",
        "jsmin>=3.0.0",
        "mutagen>=1.45.1",
        "moviepy>=1.0.3",
        "flask>=2.0.0",
        "werkzeug>=2.0.0"
    ],
    package_data={
        "ae_automation": [
            "mixins/js/*.js",
            "mixins/js/*.jsx",
            "mixins/videoEditor/*"
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ae-automate=ae_automation.run:main",
            "ae-editor=app:main"
        ],
    }
)
