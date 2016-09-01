from setuptools import setup, find_packages

setup(
    name='userempathetic',
    version='0.1',
    packages=find_packages(),
    url='',
    license='',
    author='Sebastian Galvez, Constanza Escobar, Pablo Reszczynski',
    author_email='sebastian.galvez@ing.uchile.cl',
    description='Prototipo de clustering de sesiones y usuarios.',
    install_requires=[
        'pymysql',
        'pyyaml',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'scipy',
        'python-dateutil'
    ],
    dependency_links=[
        'http://scikit-learn.org/stable/developers/advanced_installation.html#advanced-installation'
    ]

)
