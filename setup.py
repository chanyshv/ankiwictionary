from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ankiwiktionary",
    version="0.0.1b",
    packages=find_namespace_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        'ankiwiktionary.card_styles': ['*.html'],
    },
    include_package_data=True,
    install_requires=[
        'lxml>=4.6.2',
        'yarl>=1.6.3',
        'Jinja2>=2.11.2',
        'click>=7.1.2',
        'colorama>=0.4.4',
    ],
    entry_points={
        'console_scripts': [
            'ankiwiktionary=ankiwiktionary.cli:main'
        ]},
    author='Damir Chanyshev',
    author_email='hairygeek@yandex.com',
    description='Anki cards generating from Wiktionary pages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='anki card generation wiktionary russian',
    project_urls={
        "Bug Tracker": "https://github.com/hairygeek/ankiwiktionary",
        "Documentation": "https://github.com/hairygeek/ankiwiktionary",
        "Source Code": "https://github.com/hairygeek/ankiwiktionary",
    }
)
