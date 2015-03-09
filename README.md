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

This scraper is based on PhantomJS 1.9.8. PhantomJS 2.0 isn't stable yet.

<strong>URL Collection:</strong>

The relevant code is included in "metrosCubicosUrls" directory. You can run it using <strong>python getUrls.py</strong>

Lets assume it has 60,000 listings in total. This website displays 15 listings per page. So, in total there are 4000 pages.

Take a look at this line in "getUrls.py"

<code>
`HANDLE_MAX_NUM_PAGES_PER_PASS = 1500`
</code>

It will split up the URL collection into three parts (part0.py, part1.py, part2.py) now. Each part will hold 1500 x 15 = 22,500 listings 
at max. These parts are created using the included template. I have already run this once, obtained the parts and fed them to the 
spider. 

<strong>How?</strong>

You need to copy the generated parts (part*.py) to "metrocCubicos/spiders" directory and then make a few changes to the spider itself.
Take a look at the following set of lines:

<code>
import part0<br>
import part1<br>
import part2<br><br>
start_urls = part0.getStartURLS()+part1.getStartURLS()+part2.getStartURLS()
</code>

Basically, I have included all the urls in this run and will be rendered by a single broswer. You can speed up the process some more,
running the same spider with different "start_urls".

<strong>Spider 1:</strong>

<code>
import part0<br>
start_urls = part0.getStartURLS()
</code>

<strong>Spider 2:</strong>

<code>
import part1<br>
start_urls = part1.getStartURLS()
</code>

<strong>Spider 3:</strong>

<code>
import part2<br>
start_urls = part2.getStartURLS()
</code>

Please do keep in mind that PhantomJS eats up a lot of memory. Finally you need to plug in your database related info in <strong>
"metrosCubicos/pipelines.py" (Line11)</strong>.

You also need to make sure to provide the path to the phantomjs executable and unblock the port (65,000 in our case). Take a look 
at the following set of lines:

<code>
PORT = 65000<br>
`self.driver = webdriver.PhantomJS(executable_path='../Phantomjs_1.9.8/phantomjs', service_args=['--load-images=no'], port=PORT)`
</code>

Now simply run:
<strong>scrapy crawl mcspider > output 2>&1</strong>

Depending on your bandwidth it will take between 1-2 days to crawl the entire website.

In case a particular listing hasn't been added to the database, the relevant information can be found in "output". 
Don't forget to check it out in the end.
