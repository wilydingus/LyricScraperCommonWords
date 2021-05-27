import re
import time
import requests

from selenium import webdriver



driver = webdriver.Chrome() # replace Chrome with your preferred browser


api_key = 'KEY'

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + api_key}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response

# Get song url's from a Genius.com artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    print('Found {} songs by {}'.format(len(songs), artist_name))
    return songs

#return lyrics to the song with given url
def scrape_lyrics(url):
    driver.get(url)

    #allow time to load before attempt scraping
    time.sleep(5)

    #get the title of song and lyrics from the html with selenium
    lyrics = driver.find_element_by_xpath("//*[@id=\"application\"]/main/div[2]/div[3]")

    #turn lyrics into string
    lyrics = lyrics.text
    lyrics = lyrics.lower()

    #remove identifiers like chorus, verse, etc with regex identifying bracketed items
    lyrics = re.sub(r'[(\[].*?[)\]]', '', lyrics)

    #remove everything but letters and white space
    lyrics = re.sub(r'[^a-z\s]', '', lyrics)

    return lyrics

#count most common words given string and print top k with their frequencies
def print_k_most_common_words(lyrics, k):
    from collections import Counter

    # split() returns list of all the words in the string
    split_it = lyrics.split()

    # Pass the split_it list to instance of Counter class.
    Counter = Counter(split_it)

    # most_common() produces k frequently encountered
    # input values and their respective counts.
    most_occur = Counter.most_common(k)

    print(most_occur)
    print()

#main function, given name of artists checks the ammount specified of top songs and returns their most used words
def artist_common_words(artist_name, song_count, word_count):
    urls = request_song_url(artist_name, song_count)
    lyrics = ''
    for url in urls:
        lyrics += scrape_lyrics(url)
    print_k_most_common_words(lyrics, word_count)



# DEMO
#check three of the artist Liily's songs and return the top 20 most used words from them
artist_common_words('Liily', 3, 20)