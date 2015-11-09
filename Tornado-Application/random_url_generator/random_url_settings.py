# random_url_settings.py include settings for the random_url_generator.py

# random_base are numbers that we randomly choose when we are building an URL.
# If there are 16 different numbers, and a 6 digit long shortened URLs, then we can build
# 16 million different URLs
random_base = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
               "A", "B", "C", "D", "E", "F"]

# domain_base is a url that we will join with a six digit hash of the a URL to be shortened
#domain_base = "http://mxlei01.com/url_shortener/"
domain_base = "http://localhost:8888/url_shortener/"

# the length of the generated shortened URL digits/letters
length_url = 6