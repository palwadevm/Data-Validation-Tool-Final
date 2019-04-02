from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='DataValidationTool',
      version='2.2.0',
      description='Data Validation Tool For Automated Data Validations',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 3.6',
          "Operating System :: OS Independent",
      ],
      keywords='Data Validation Tool',
      author='Vaijnath Palwade',
      author_email='palwadevm@gmail.com',
      license='Synechron Technologies',
      packages=find_packages(),
      install_requires=['PyQt5', 'PyOdbc', 'cx-Oracle', 'PyHive', 'wheel', 'thrift'],
      package_data={
          '': ['Resources/backend/*.*', 'Resources/backend/File2File/*.*', 'Resources/backend/HadoopHive2File/*.*', 'Resources/backend/MongoDB2HadoopHive/*.*', 'Resources/backend/SQLServer2HadoopHive/*.*', 'Resources/backend/SQLServer2MongoDB/*.*',
               'DataValidationTool/application/guiWindows/icons/*.*']
      },
      include_package_data=True,
      zip_safe=False
      )
