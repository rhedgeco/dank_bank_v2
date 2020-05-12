from setuptools import setup

setup(
    name='dank_bank_v2',
    version='1.0.0',
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "cachecontrol",
        'google',
        'requests',
        'falcon',
        'httpie',
        'pytest'
    ]
)
