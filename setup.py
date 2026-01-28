from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="after-effects-automation",
    version='0.0.3',
    author="Juan Denis",
    author_email="juan@vene.co",
    description="A unified video automation platform for Adobe After Effects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhd3197/after-effects-automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=0.19.0",
        "pyautogui>=0.9.53",
        "pydirectinput>=1.0.4",
        "pywinauto>=0.6.8",
        "python-slugify>=5.0.0",
        "Pillow>=8.0.0",
        "jsmin>=3.0.0",
        "mutagen>=1.45.1",
        "moviepy>=1.0.3",
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "werkzeug>=2.0.0",
        "psutil>=5.8.0"
    ],
    extras_require={
        "window-detection": ["pygetwindow>=0.0.9"],
    },
    package_data={
        "ae_automation": [
            "py.typed",
            "mixins/js/*.js",
            "mixins/js/*.jsx",
            "mixins/videoEditor/dist/**/*",
            "mixins/videoEditor/dist/*",
            "mixins/videoEditor/script.js"
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ae-automation=cli:main",
            # Legacy aliases for backward compatibility
            "ae-automate=cli:main",
        ],
    }
)
