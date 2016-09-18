## NewsFlash
All your daily news from all your favorite sources, compiled into one place and summarized for easy consumption.

NewsFlash brings you news from all the top news sites such as CNN, NBC, HuffingtonPost and brings them directly to your NewsFlash dashboard. It groups similar stories together so you don't have to read the same article twice, unless you want a more unbiased view. Additionally, each article is summarized to only a few short lines, to make the most of your precious time.

There's also customization options so that you can filter out any sources that you don't like (or don't agree with) or any news categories you're simply not interested in!

# Setup on Mac only
We don't have a dedicated server, unforunately. You will have to run your own server.

cd into your chosen directory.

```
$ git clone https://github.com/jiwon85/hackthenorth.git

$ cd hackthenorth

$ source setup.sh
```

Everything should now be installed. To run the server, run:
```
$ python news_site/manage.py runserver
```

Now the host should be running. To use the site, go to localhost:8000

Thanks for reading.

