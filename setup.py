from setuptools import find_packages, setup


requirements = [
    "wheel>=0.38.4",
    "oauthlib==3.2.2",
    "pytest>=5",
    "pytest-timeout",
    "pytest-django",
]

setup(
    name="rest-client-for-shipping-company",
    version="1.1.0",
    author="Devskiller",
    author_email="support@devskiller.com",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=requirements,
    test_suite="test",
    tests_require=requirements,
    setup_requires=["pytest-runner"],
)
