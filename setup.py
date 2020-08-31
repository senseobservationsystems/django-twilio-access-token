import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-twilio-access-token",
    version="0.0.4",
    author="Panji Y. Wiwaha",
    author_email="panjiyudasetya@gmail.com",
    description="A Django app to generate Twilio access token for particular Twilio services.",
    keywords=['django', 'twilio', 'access', 'token'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/senseobservationsystems/django-twilio-access-token/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'django',
        'djangorestframework',
        'drf-rw-serializers',
        'python-dateutil',
        'twilio'
    ]
)
