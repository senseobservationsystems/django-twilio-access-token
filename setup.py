import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-twilio-access-token",
    version="0.0.1",
    author="Panji Y. Wiwaha",
    author_email="panjiyudasetya@gmail.com",
    description="A Django app to generate Twilio access token for particular services.",
    keywords=['django', 'twilio', 'access', 'token'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django',
        'djangorestframework',
        'twilio'],
    python_requires='>=3.6',
)
