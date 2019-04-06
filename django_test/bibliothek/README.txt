Verify django installed :
    D:\python\django_test>py -3 -m django --version
    2.2

Create skeleton project files, run in DOS cmd:
    django-admin.exe startproject bibliothek

Check it:
    D:\python\django_test\bibliothek>py manage.py check
    System check identified no issues (0 silenced).

Create the 'catalog' app:
    D:\python\django_test\bibliothek>py manage.py startapp catalog

Then register the app's Config class in the project settings, and map urls to views.
Run a DB migration before trying to start it up, to remove some build warnings..
Because the initial project setup included models (domain object classes) supporting admin functionality.

NOTE: Need to do this EACH TIME domain models are altered :-

    py manage.py makemigrations
        No changes detected
    py manage.py migrate
        Operations to perform:
          Apply all migrations: admin, auth, contenttypes, sessions
        Running migrations:
          Applying contenttypes.0001_initial... OK
          ...cut...
          Applying sessions.0001_initial... OK

NOTE: To enable admin account need to run:
    py manage.py createsuperuser
