from setuptools import setup

setup(
    name='userempathetic',
    version='0.1',
    packages=['src', 'src.simulated', 'src.simulated.simulatedData', 'src.userempathetic', 'src.userempathetic.utils',
              'src.userempathetic.metrics', 'src.userempathetic.metrics.microMetrics',
              'src.userempathetic.metrics.sessionMetrics', 'src.userempathetic.testing', 'src.userempathetic.nodeClass',
              'src.userempathetic.clustering', 'src.userempathetic.clustering.clusterings',
              'src.userempathetic.dataParsing', 'src.userempathetic.clusterClass', 'src.userempathetic.sessionClass',
              'src.userempathetic.sessionParser', 'src.userempathetic.sessionParser.sessionizers',
              'src.userempathetic.featureExtractor', 'src.userempathetic.featureExtractor.features',
              'src.userempathetic.featureExtraction', 'src.userempathetic.sessionComparator',
              'src.userempathetic.groundTruthLabeling'],
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
