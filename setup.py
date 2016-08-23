from setuptools import setup

setup(
    name='userempathetic',
    version='0.1',
    packages=['src', 'src.simulatedData', 'src.utils',
        'src.metrics', 'src.metrics.sessionMetrics', 'src.metrics.nodeMetrics',
        'src.testing', 'src.nodeClass',
        'src.clustering', 'src.clustering.clusterings',
        'src.clustering.clusterings.userclusterings',
        'src.clustering.clusterings.sessionclusterings',
        'src.dataParsing', 'src.clusterClass', 'src.sessionClass',
        'src.sessionParser', 'src.sessionParser.sessionizers',
        'src.featureExtractor', 'src.featureExtractor.features',
        'src.featureExtraction', 'src.sessionComparator',
        'src.groundTruthLabeling', 'src.view', 'src.simulatedData'],

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
