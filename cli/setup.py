from setuptools import setup, find_packages

setup(
    name="security-monitor-cli",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'security-monitor=security_monitor:cli',
        ],
    },
)
