import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.rollingstone.com/music/music-lists/100-greatest-artists-147446/the-band-2-88489/'

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run the browser in headless mode (optional)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



driver.get(url)

# Give the JavaScript time to load and render the content
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

divs = soup.find_all('div', class_='c-gallery-vertical__slide-wrapper')

artist_titles = []

for div in divs:
    artist_name = div.find('h2', class_='c-gallery-vertical-album__title')
    
    if artist_name:
        artist_name_text = artist_name.get_text(strip=True)
        artist_titles.append(artist_name_text)

print(artist_titles)

#['Talking Heads', 'Carl Perkins', 'Curtis Mayfield', 'R.E.M.', 'Diana Ross and the Supremes', 'Lynyrd Skynyrd', 'Nine Inch Nails', 'Booker T. and the MGs', 'Guns n’ Roses', 'Tom Petty', 'Carlos Santana', 'The Yardbirds', 'Jay-Z', 'Gram Parsons', 'Tupac Shakur', 'Black Sabbath', 'James Taylor', 'Eminem', 'Creedence Clearwater Revival', 'The Drifters', 'Elvis Costello', 'The Four Tops', 'The Stooges', 'Beastie Boys', 'The Shirelles', 'Eagles', 'Hank Williams', 'Radiohead', 'AC/DC', 'Frank Zappa', 'The Police', 'Jackie Wilson', 'The Temptations', 'Cream', 'Al Green', 'The Kinks', 'Phil Spector', 'Tina Turner', 'Joni Mitchell', 'Metallica', 'The Sex Pistols', 'Aerosmith', 'Parliament and Funkadelic', 'Grateful Dead', 'Dr. Dre', 'Eric Clapton', 'Howlin’ Wolf', 'The Allman Brothers Band', 'Queen', 'Pink Floyd', 'The Band', 'Elton John', 'Run-DMC', 'Patti Smith', 'Janis Joplin', 'The Byrds', 'Public Enemy', 'Sly and the Family Stone', 'Van Morrison', 'The Doors', 'Simon and Garfunkel', 'David Bowie', 'John Lennon', 'Roy Orbison', 'Madonna', 'Michael Jackson', 'Neil Young', 'The Everly Brothers', 'Smokey Robinson and the Miracles', 'Johnny Cash', 'Nirvana', 'The Who', 'The Clash', 'Prince', 'The Ramones', 'Fats Domino', 'Jerry Lee Lewis', 'Bruce Springsteen', 'U2', 'Otis Redding', 'Bo Diddley', 'The Velvet Underground', 'Marvin Gaye', 'Muddy Waters', 'Sam Cooke', 'Stevie Wonder', 'Led Zeppelin', 'Buddy Holly', 'The Beach Boys', 'Bob Marley', 'Ray Charles', 'Aretha Franklin', 'Little Richard', 'James Brown', 'Jimi Hendrix', 'Chuck Berry', 'The Rolling Stones', 'Elvis Presley', 'Bob Dylan', 'The Beatles']