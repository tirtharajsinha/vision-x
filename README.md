# Vision - X

## Domain - Generic image processing and recognition

### [Visit application](https://tirtharajsinha.pythonanywhere.com/)

<br>

> vision - X is a computer Vision project deployable on web ,totally based on <b>opencv-python</b> and <b>django-python</b> framework.<br>

## Project Requirements

- Programing Language : python3
- core Backend frameworks/packages : Django, numpy, opencv, pillow , sqlite3 etc.
- Tools : IDE - Pycharm | Text Editor - VS Code
- version control system : git | remote-repository-platform : github.com
- Database : SQLite3
- Hosting platform : [pythonanywhere.com](https://pythonanywhere.com)

## Download codebase in local mechine

```
git clone https://github.com/tirtharajsinha/vision-x.git
```

-- OR --<br>
If you have ssh connection then only

```
git clone git@github.com:tirtharajsinha/vision-x.git
```

## Installing python dependencies

```
cd vision-x
```

In windows

```
python install -r requirements.txt
```

In linux

```
python3 install -r requirements.txt
```

## Run application

find where the `manage.py` file is located.<br>
It should be in the `vision-x/vision` directory.<br>
If you locate the `manage.py` then open a terminal in that location.

In windows

```
python manage.py runserver
```

In linux

```
python3 manage.py runserver
```

## Contribution

Contributors are always welcome. Make sure your contribution add some value.
We belive in quality not quantity.

## upstream the local repository with remote repository

### Add upstream repository

```
git remote add upstream https://github.com/tirtharajsinha/vision-x.git
```

### Upstream your repository

```
git fetch upstream
git checkout main
git merge upstream/main

```

## In case you get messed up with your repo

first add upstream repository. then run below commands.

```
git reset --hard origin/main
git fetch upstream
git checkout main
git merge upstream/main
```

## other notes

1. use it in virtual environment(virtualenv) to get get rid of GPU related worning/error.
2. Always run ` python manage.py collectstatic` before deploying in production server.
3. Put codebase in the virtual environment in the production server.
4. Read the full documentation of the hosting platform before you are using.

## Documentation of some populer platform in case you need

1. pythonanywhere.com :

   - [Docs of hosting](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
   - [docs for managing static files](https://help.pythonanywhere.com/pages/DjangoStaticFiles)
   - [docs for media file mapping](https://docs.djangoproject.com/en/dev/topics/files/)

2. Heroku

   - [Docs of hosting](https://www.analyticsvidhya.com/blog/2020/10/step-by-step-guide-for-deploying-a-django-application-using-heroku-for-free/)
   - [docs for managing static files](https://devcenter.heroku.com/articles/django-assets)

   - [docs for database](https://dev.to/giftedstan/heroku-how-to-deploy-a-django-app-with-postgres-in-5-minutes-5lk#:~:text=This%20post%20is%20step%20by,project%20folder%20in%20the%20terminal.)

<br>

<p style="float:right;">Developed by Tirtharaj Sinha<a href="https://github.com/tirtharajsinha"> @tirtharajsinha</a>.<br></p>
