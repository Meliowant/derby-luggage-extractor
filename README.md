I've been looking for the luggae for my trip abroad. So I found 
a [nice shop](http://derby.ua), but their search filter frustrated me so much.

So, I used [scrapy](https://scrapy.org/) to crawl their luggage offers, store
it in CSV file and process further manually. This repo is not a shiny one, but
the work has been done.

# How to use it

- Clone it
- Install virtual env with scrapy:
    ```
        $ python -m venv venv
        $ . venv/bin/activate
        $ pip install scrapy
    ```
- Run `scrapy crawl "derby-luggage"`
