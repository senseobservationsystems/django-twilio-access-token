
# django-twilio-access-token

This is a Django application that can be used to generate Twilio access token for particular services, such as Voice, Chat, and Video.

## Prerequisite

### Twilio

We use Twilio client for [python](https://www.twilio.com/docs/libraries/python#install-the-library) to generate an access token for Twilio services. To make the package works on your project, you need to install Twilio client either through [pip](https://pip.pypa.io/en/stable/) command;

```
pip install twilio
```

or simply add Twilio on your `requirements.txt`

```
twilio~=6.32.0
```

### Twilio keys

In order to make the package works with your django project, you need to define the Twilio keys inside your project `settings.py`, for example:
```
TWILIO_ACCOUNT_SID = 'PUT_YOUR_TWILIO_ACCOUNT_SID_HERE'  # You can find Twilio Account SID at the top right section of this page https://www.twilio.com/console/

TWILIO_VIDEO_API_KEY_SID = 'PUT_YOUR_TWILIO_VIDEO_API_KEY_SID_HERE'  # You can obtain these keys by creating it through https://www.twilio.com/console/video/project/api-keys/
TWILIO_VIDEO_API_KEY_SECRET = 'PUT_YOUR_TWILIO_VIDEO_API_KEY_SECRET_HERE'
```

Or see the `test_project/test_app/settings.py` if you need to know more.

## How to run the test project

To try out the package, you can run our test application by following these steps:
1. Ensure pip installed on your local machine. If you don't have it, you can follow the installation guide [here](https://pip.pypa.io/en/stable/installing/).
2. Open terminal and go to the root directory of where the package live, for instance: `$ cd Documents/py-projects/django-twilio-access-token`.
3. Run `$ ./scripts/requirement-install.sh` from your command line.
4. Run `$ source venv/bin/activate`.
5. Run `$ python manage.py runserver 0.0.0.0:8000` and enjoy the token API's.

## Get involved!

We are happy to receive bug reports, fixes, documentation enhancements, and other improvements.

Please report bugs via the github [issue tracker](https://github.com/senseobservationsystems/django-twilio-access-token/issues).

Master git repository [django-twilio-access-token](https://github.com/senseobservationsystems/django-twilio-access-token).