from setuptools import setup, find_packages

setup(
    name='tse_py',
    version='0.1',
    description='A Python Module to Access Tehran Stock Exchange Historical and Real-Time Data',
    author='Sajad Kiyani',
    author_email='skm.kiani@email.com',
    url='https://github.com/sajjadkiani/tse_py',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        'certifi==2023.7.22',
        'charset-normalizer==3.2.0',
        'idna==3.4',
        'numpy==1.25.2',
        'pandas==2.0.3',
        'python-dateutil==2.8.2',
        'pytz==2023.3',
        'requests==2.31.0',
        'six==1.16.0',
        'tzdata==2023.3',
        'urllib3==2.0.4',
        'persiantools==3.0.1',
    ]
)
