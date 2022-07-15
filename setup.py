from setuptools import find_packages, setup

setup(
    name='jupyter-cloud-scoped-creds',
    version='0.0.1',
    url='https://github.com/scottyhq/jupyter-cloud-scoped-creds',
    license='Apache 2',
    author='Scott Henderson, Yuvi Panda',
    description='Server extension to get temporary cloud credentials from jupterhub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['jupyter_server>=1.10.1', 'tornado'],
    data_files=[
        ('etc/jupyter/jupyter_server_config.d', ['./jupyter_server_config.d/jupyter_cloud_scoped_creds.json']),
        ('etc/jupyter/jupyter_notebook_config.d', ['./jupyter_notebook_config.d/jupyter_cloud_scoped_creds.json'])
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
