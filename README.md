# MPT Indicators

A project of [Money, Politics and Transparency](http://moneypoliticstransparency.org).

## Chunks

Some of the words shown on the website are stored in a file called chunks.json, whose contents are saved to the database. To initialize an install with this copy, run `python manage.py loaddata data/chunks.json`.

## Static Assets

### Setup

1. `npm install -g bower grunt`
1. `python manage.py bower install`
1. `npm install`

### Develop

Run `grunt` to only watch for file changes or `python manage.py gruntserver` to
watch for changes AND run the Django dev server.
