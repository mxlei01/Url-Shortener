[![Build Status](https://travis-ci.org/mxlei01/Url-Shortener.svg)](https://travis-ci.org/mxlei01/Url-Shortener)
[![Code Health](https://landscape.io/github/mxlei01/Facebook-Group-Sentiment-Analysis/master/landscape.svg?style=flat)](https://landscape.io/github/mxlei01/Facebook-Group-Sentiment-Analysis/master)
[![Coverage Status](https://coveralls.io/repos/mxlei01/Url-Shortener/badge.svg?branch=master&service=github)](https://coveralls.io/github/mxlei01/Url-Shortener?branch=master)
[![Code Climate](https://codeclimate.com/github/mxlei01/Url-Shortener/badges/gpa.svg)](https://codeclimate.com/github/mxlei01/Url-Shortener)

# url-shortener

[![Join the chat at https://gitter.im/mxlei01/Url-Shortener](https://badges.gitter.im/mxlei01/Url-Shortener.svg)](https://gitter.im/mxlei01/Url-Shortener?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
A server side application that shortens url

# How To Use
<p>
	<b> URL: http://localhost:8888/url_gen </b>
	<br>
	- Effect: will generate a shortened_url
	<br>
	- For example, www.google.com will be mapped to http://localhost:8888/url_shortener/XXXXXX
	<br>
	- Returns: {"original_url":url, "shorted_url":url}
</p>

<p>
	<b> http://localhost:8888/url_gen?change=text </b>
	<br>
	- Effect: will generate a shortened_url with text as it's last path
	<br>
	- For example, www.google.com will be mapped to http://localhost:8888/url_shortener/XXXXXX
	<br>
	- Returns: {"original_url":url, "shorted_url":url}
</p>

<p>
	<b> http://localhost:8888/url_info?url_shortened=http://localhost:8888/url_shortener/XXXXXX </b>
	<br>
	- Effect: will search for the usage of the shortened_url
	<br>
	- Returns : {"count":int}
</p>

<p>
	<b> http://localhost:8888/url_shortener/XXXXXX </b>
	<br>
	- Effect: will return the original url that is going to be access
	<br>
	- Returns : {"original_url":url}
</p>

<p>
	<b> http://localhost:8888/url_latest_100 </b>
	<br>
	- Effect: will return the latest 100 shortened urls
	<br>
	- Returns : {"latest_100_shortened_urls":[{"shortened_url":url, "date":date}, ...multiple if any]}
</p>

<p>
	<b> http://localhost:8888/url_top_10_domain_30_days </b>
	<br>
	- Effect: will return the top 10 shortened domains in the last 30 days
	<br>
	Returns : {"top_10_domain_30_days":[{"domain":url, "count":int}, ...multiple if any]}
</p>

# Implementation
Backend Framework : Python Tornado and Momoko
<br>
Url Shortener : Uses random number generator to shorten a url
