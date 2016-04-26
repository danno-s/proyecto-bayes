from setuptools import setup

setup(
    name='userempathetic',
    version='0.1',
    packages=['src', 'src.simulated', 'src.simulated.simulatedData', 'src.utils',
              'src.metrics', 'src.metrics.sessionMetrics', 'src.testing', 'src.nodeClass',
              'src.clustering', 'src.clustering.clusterings',
              'src.dataParsing', 'src.clusterClass', 'src.sessionClass',
              'src.sessionParser', 'src.sessionParser.sessionizers',
              'src.featureExtractor', 'src.featureExtractor.features',
              'src.featureExtraction', 'src.sessionComparator',
              'src.groundTruthLabeling'],
    url='',
    license='',
    author='Sebastian Galvez, Constanza Escobar',
    author_email='sebastian.galvez@ing.uchile.cl',
    description='Prototipo de clustering de sesiones y usuarios.',
    install_requires=[
        'mysql-connector-python',
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
