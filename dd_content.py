import csv
import random
from urllib import request
import json
import datetime




def get_random_quote(quotes_file='D:\Python\Project\Project\end\quotes.csv'):
    try: # load motivational quotes from csv file
        with open(quotes_file,'r') as f:
            reader = csv.reader(f,delimiter='|')
            quotes = [{'quote':word[1] , 'author' : word[0]} for word in reader]
    except Exception as e:  # use a default quote to help things turn out for the best
        quotes = [{'quote' : 'Imagination is more important than knowledge.', 'author' : 'Confucius'}]

    return random.choice(quotes)

def get_weather_forecast(coords={'lat':26.9167 ,'lon' : 75.8167 }):
    try: # retrieve forecast for specified coordinates
        api_key = '****************************' # replace with your own OpenWeatherMap API key
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {'city': data['city']['name'], # city name
                    'country': data['city']['country'], # country name
                    'periods': list()} # list to hold forecast data for future periods

        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        
        return forecast

    except Exception as e:
        print(e) 


def get_wikipedia_article():
    try: # retrieve random Wikipedia article
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}

    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    ##### test get_random_quote() #####
    print('\nTesting quote generation...')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    quote = get_random_quote(quotes_file = None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    ##### test get_weather_forecast() #####
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')
    
    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')