# SIPPAS Website made in "No frills, no hassle" mode

Since the website site will have low to medium traffic, I decided to opt for the following stack:

- Flask > [website](http://flask.pocoo.org/)
- SQLite >  [website](https://sqlite.org/)
- UIkit > [website](https://getuikit.com/)

*see the requirements.txt for other flask-related libs*

Flask and UIkit are frameworks that I like, so their choice comes with no surprise. 
On the other hand, I decided to give SQLite a try and see if a dynamic blog-type website based on it (many readers, few writers) can sustain a low/medium traffic-load with no hiccups.

Some optimizations were made in the production environment, most notably a "filesystem" caching mechanism and the delegation of the blog search feature to [Algolia](https://www.algolia.com/)

Currently, the site is hosted on a [Digital Ocean](https://www.digitalocean.com/) 5$ droplet with Ubuntu 18.04 LTS, Ngnix and Gunicorn.

Here's the link [https://www.sippas.info](https://www.sippas.info).