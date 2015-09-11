# Readme #

This is a [cookiecutter](https://github.com/audreyr/cookiecutter) template for [Django](https://www.djangoproject.com/) 1.8 and Python 3.4.  I use it for many of my personal projects.

## Features ##
* [12 factor](http://12factor.net/) app style configuration with [python-dotenv](https://github.com/theskumar/python-dotenv) and [dj-database-url](https://github.com/kennethreitz/dj-database-url).  Modular settings and requirements easily handle differences between development and production.

* Fully functioning local registration and authentication using Django built-in views.

* Pre-configured social authentication for Facebook, Twitter, and Google using [python-social-auth](https://github.com/omab/python-social-auth).

* Modern password hashing with [bcrypt](https://github.com/pyca/bcrypt).

* A custom user model, which can be easily further customized.

* Simplified production ready static file serving with [whitenoise](https://github.com/evansd/whitenoise).

* Modern front-end tooling with [Webpack](http://webpack.github.io/).

* ES 2015 and beyond with [Babel](https://babeljs.io/).

* Tomorrow's CSS today with [cssnext](http://cssnext.io/), powered by [PostCSS](https://github.com/postcss/postcss), the next generation CSS transformer.

* Nicely styled pages with [Bootstrap](http://getbootstrap.com/).

* Efficient database connection pooling with [django-postgrespool](https://github.com/kennethreitz/django-postgrespool).

* Pre-configured file storage for user uploaded media with [Amazon S3](https://aws.amazon.com/s3/) and [django-storages](https://github.com/jschneier/django-storages)

* [Procfile](https://devcenter.heroku.com/articles/procfile) for Heroku deployment.

## Setup ##
1. Get [Python](https://www.python.org/) version 3.4 and setup a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for your project.

2. Get [cookiecutter](https://github.com/audreyr/cookiecutter), run it on this template, then follow the prompts.
  ```shell
  $ pip install cookiecutter
  $ cookiecutter https://github.com/Traviskn/django_starter_template.git
  ```

3. Install your new Django project's development requirements:
  * Install the required python packages:
  ```shell
  $ pip install -r requirements/development.txt
  ```
  * Get [Node](https://nodejs.org/) and install the required JavaScript libraries:
  ```shell
  $ npm install
  ```

4. Create a .env file and fill out the required environment variables. You probably shouldn't track it in version control, so I've added it to the .gitignore for you already.
  * You will need to configure your database and put it's access url in the .env file. If you're on a Mac, I highly recommend [postgres.app](http://postgresapp.com/).
  * You need to head over to the developer consoles for [Facebook](https://developers.facebook.com/), [Twitter](https://apps.twitter.com/), and [Google](https://console.developers.google.com/) to register your app then get tokens and secrets for each provider that you can put into your .env file.  You can enter some dummy values for now if you'd rather do this later.
  * Here's an example .env file you might use for development:
  ```
  DJANGO_SETTINGS_MODULE=mysite.settings.development
  DATABASE_URL=postgres://username:password@host:port/dbname
  TWITTER_KEY=PutYourKeyHere
  TWITTER_SECRET=PutYourSecretHere
  FACEBOOK_KEY=key
  FACEBOOK_SECRET=secret
  GOOGLE_KEY=key
  GOOGLE_SECRET=secret
  ```

5. Take a look at accounts/models.py and make any customizations you need to the User model.

6. Make migrations then run migrations.

7. You will need to run both the Django development server and the Webpack development server. Open up two terminal windows and enter these commands:
  ```shell
  # in the first terminal window
  $ python3 manage.py runserver
  ```
  ```shell
  # in the second terminal window
  $ npm run dev
  ```

8. Now if you head to localhost:8000 in your browser you should be able to see a nice "Hello World!".  You should also be able to sign up for an account and log in and out.  Try editing the javascript or css files and your changes should appear in the browser without a refresh.

9. For deployment you will need to build the static assets with the following command before running collectstatic:
  ```shell
  $ npm run build
  ```
