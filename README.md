# MC_Scraper
A scrapy, selenium, PhantomJS based scraper for MC

First of all setup your MySQL server. Lets assume that you have created a database "pyScraper".

The associated table creation statement for this project can be found in "cTable.txt".

Now you would need Python 2.7.* and the following packages:

<ul>
<li>python-dev</li>
<li>python-setuptools</li>
<li>python-mysqldb</li>
</ul>

Use you package manager to install those. Now, you will have access to the command "easy_install". Use that to install 
"pip" (Python package manager)

<strong>*sudo easy_install pip*</strong>

Now use "pip" to install "scrapy"

<strong>*sudo -H pip install scrapy*</strong>

Finally you would also need to install "phantomjs". Its basically a headless browser that speeds up the entire
process manifold.

Version 1.9.* would work. But, if you can download and install PhantomJS 2.0 from source (Beware, it takes a long
long time to build as it uses WebKit internally, which has tons of files) then it can be utilized with the
LM_Scraper as well.

Version 2.0 is HTML5 compliant and wouldn't pop up an exception when we try to "click" a link. This project 
needs just needs buttons to be clicked, so 1.9.* versions would work just fine. I have also plugged in code to
use the Firefox driver by default in LM_Scraper. So, its alright if you go with version 1.9.* as well.

Finally you need to plug in your database related info in <strong>"metrosCubicos/pipelines.py" (Line11)</strong>.
Thats it!!

Now simply run:
<strong>scrapy crawl mcspider > output 2>&1<strong>

Depending on your bandwidth it will take between 1-2 days to crawl the entire website.

In case a particular listing hasn't been added to the database, the relevant information can be found in "output". 
Don't forget to check it out in the end.
