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
