from setuptools import setup, find_packages
setup(
        name='trans-prof-email-writer',
        version='0.0.1a0',
        packages=find_packages(),
        scripts=['write_letters.py'],
        install_requires=[
            'jinja2>=2.4',
            'jsonschema>=0.3',
            'pyyaml>=3.10'
        ],

        author='Kinsey Favre',
        author_email='iyunkateus@gmail.com',
        license='GPL',
        url='https://github.com/kinstalinist/trans-prof-email-writer'

)
