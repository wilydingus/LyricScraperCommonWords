# LyricScraperCommonWords
Given the name of a music artist scrapes the genius website for the amount of songs specified and returns their k most used words

I utilized the genius API to help provide an artist object that could give me a list of their most popular songs. Then I used selenium to scrape the lyrics from the top x songs. Next I utilized Counter to find which songs are most 

Just go to https://docs.genius.com/ take the string to the right of  "Authentication: Bearer" and sub that in where "KEY" is in my python code.

Then to run the main program just fill in the artist_common_words(artist_name, song_count, word_count) demo function with your preffered artist, the amount of songs you want it to check, and how many of the common words do you want to see
