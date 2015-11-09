[![Build Status](https://travis-ci.org/mxlei01/Url-Shortener.svg)](https://travis-ci.org/mxlei01/Url-Shortener)

# url-shortener
A server side application that shortens url

# How To Use
URL: http://localhost:8888/url_gen
<br>
- Effect: will generate a shortened_url
<br>
- For example, www.google.com will be mapped to http://localhost:8888/url_shortener/XXXXXX
<br>
- Returns: {"original_url":url, "shorted_url":url}
<br><br><br>
http://localhost:8888/url_gen?change=text => will generate a shortened_url with text as it's last path
<br>
for example, www.google.com will be mapped to http://localhost:8888/url_shortener/XXXXXX
<br>
Returns: {"original_url":url, "shorted_url":url}
<br><br>
http://localhost:8888/url_info?url_shortened=http://localhost:8888/url_shortener/XXXXXX => will search for the usage of the shortened_url
<br>
Returns : {"count":int}
<br><br>
http://localhost:8888/url_shortener/XXXXXX => will return the original url that is going to be access
<br>
Returns : {"original_url":url}
<br><br>
http://localhost:8888/url_latest_100 => will return the latest 100 shortened urls
<br>
Returns : {"latest_100_shortened_urls":[{"shortened_url":url, "date":date}, ...]}
<br><br>
http://localhost:8888/url_top_10_domain_30_days => will return the top 10 shortened domains in the last 30 days
<br>
Returns : {"top_10_domain_30_days":[{"domain":url, "count":int}, ...]}


# Implementation
Backend Framework : Python Tornado and Momoko
<br>
Url Shortener : Uses random number generator to shorten a url
