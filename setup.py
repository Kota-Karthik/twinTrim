from setuptools import setup, find_packages

setup(
    name='twinTrim',  # Name of the package
    version='0.1.1',  # Version number
    description='A CLI tool to find and delete duplicate files in a directory.',  # Short description
    long_description=open('README.md').read(),  # Readme for long description
    long_description_content_type='text/markdown',  # Type of long description
    author='Kota-Karthik',  # Author name
    author_email='kotakarthik2307@gmail.com',  # Author's email
    url='https://github.com/kota-karthik/twinTrim',  # URL of the project
    packages=find_packages(),  # Automatically finds and includes all packages
    install_requires=[  # Dependencies
        'click>=8.0',
        'tqdm>=4.66.5',
        'mkdocs>=1.6.1',
        'mkdocs-material>=9.5.44',
    ],
    extras_require={  # Optional dependencies for development
        'dev': [
            'pytest>=8.3.3',
            'pytest-mock>=3.14.0',
        ],
    },
    classifiers=[  # Classifiers to help PyPI users find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Minimum Python version
    entry_points={  # CLI tool entry point
        'console_scripts': [
            'twinTrim=twinTrim.main:cli',  # Adjusted entry point based on Poetry
        ],
    },
)
