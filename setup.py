from setuptools import setup, find_packages


# Files to be included in the distribution
packages = find_packages()

# Dependences
install_requires = [
    'requests',
]

# Setup configuration
setup(
    name='alanube',
    version='0.0.2',
    author='Wilmer Martinez',
    author_email='info@wilmermartinez.dev',
    description='Library to establish connections with the Alanube API.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wilmerm/alanube-python',
    license='MIT',
    packages=packages,
    install_requires=install_requires,
    keywords=[
        'alanube',
        'api',
        'dgii',
        'ncf',
        'electronic billing',
        'electronic bill',
        'billing',
        'bill',
        'invoice',
        'erp',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
