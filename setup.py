from setuptools import setup, find_packages


setup(
    name='django-constructor-forms',
    version='0.0.1',
    description='Django application for constructing many feedback forms.',
    long_description=open('README.md').read(),
    author='Anton Larkin',
    author_email='toxicwar94@yandex.ru',
    license='MIT',
    url='',
    include_package_data=True,
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[]
)
