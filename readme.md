# SIPPAS Website made in "No frills, no hassles" mode

Since the website site will have low to medium traffic, I decided to opt for the following stack:

- Flask > [website](http://flask.pocoo.org/)
- SQLite >  [website](https://sqlite.org/)
- UIkit > [website](https://getuikit.com/)

Flask and UIkit are frameworks that I really like, so their choice comes with no surprise. 
On the other hand, I decided to try SQLite and see if a dynamic website based on it can sustain a low/medium traffic-load with no hiccups.

Some optimizations were made in the production environment, most notably a "filesystem" caching mechanism.

Currently, the site is hosted on a [Digital Ocean](https://www.digitalocean.com/) 5$ droplet with Ubuntu 18.04 LTS, Ngnix and Gunicorn.

Here's the link [https://www.sippas.info](www.sippas.info).