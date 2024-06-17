from setuptools import find_packages, setup

setup(
    name='api_emissions_tracker',
    packages=find_packages(),
    package_data={'api_emissions_tracker': ['emission_factors.json']},
    install_requires=['openai', 'mockai@git+https://github.com/borisruf/mockai'],
    version='0.1.0',
    description='Estimates emissions linked to AI cloud services.',
    long_description='A Python library that estimates the carbon emissions linked to cloud-based API services, such as AI cloud services, for demonstration purposes.',
    author='Boris Ruf',
    url='https://github.com/borisruf/api_emissions_tracker'
)