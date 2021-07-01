@author : him-caw

CAWStudios Movies Show Booking App
==================================

Framework: Django
DB: Postgres

#To get started with this project:
install Python > 3.8

**create virtual environment**
python -m venev {env name}

and activate virtual environment

{env_name}\Scripts\activate

> Install Required Modules
pip install -r requirements.txt

> Make proper migrations
python manage.py migrate

> To run server use command
python manage.py runserver


API Documentation
=================

1. **Generating Tokens**
>GET api/v1/genToken
    params - username, password

>GET api/v1/refreshToken
    params - refresh 


2. **Registering User**
>POST api/v1/register/
    body should be in json containing
    {
        "username" : <>
        "password" : <>
        "email" : <>
        "first_name" : <>
        "last_name" : <>
    }



*You need to provide Bearer Authentication in below APIs*
>To add Authenctication Add Header Paramater
    Authorization  : Bearer <access_token_retrieved from token api>

3. **Movies API**
>   *To add Movies*
    POST api/v1/movies/
        {
        "movie_name" :  <movie_name string>,
        "genre" : <string>,
        "release_date" : <yyyy-mm-dd>,
        "starring" : <string>,
        "duration" : <in minutes (integer)>
        }
    
> *To Get All Movies*
    GET api/v1/movies/

    You can filter movies using query movie_name
    api/v1/movies?movie_name=<search string>


4. **Cinemas API**
    > *To add Cinemas*
    POST api/v1/cinemas/
        {
        "name": <cinema_name>,
        "address": <address in text>,
        "city": <city in string>,
        "capacity": <integer>
        }

    > *To Get Cinemas*
    GET api/v1/cinemas/

    >Filtering Cinems with query params city
    GET api/v1/cinemas?city=<city string>

5. **ShowTimes API**
    > Adding ShowTimes
    POST api/v1/showtimes/
        {
        "cinema" : <cinema_id>,
        "movie" : <movie_id>,
        "show_time" : '2021-06-26 13:00:00',
        "end_time" : '2021-06-26 18:00:00',
        "total_seats" : <integer>,
        "ticket_price" : <float>
        }

    > Get showtimes
    GET api/v1/showtimes/

    >Filtering showTimes
    GET api/v1/showtimes?cine_id=<cinema_id>
    GET api/v1/showtimes?movie_id=<movie_id>

    *You can use multiple query parameters

6. **Ongoing Shows**
    > Get all ongoing shows
     GET api/v1/ongoing_shows

     >Filtering ongoing shows on basis of city and movie
     GET api/v1/ongoing_shows?cine_city=<cinema_city>
     GET api/v1/ongoing_shows?movie=<movie_string>

     *You can use multiple query parameters

7. **Booking API**
    > Making Booking 
    POST api/v1/booking/
        {
        "person_name" : <string>,
        "qty": <integer>,
        "show": <show_id>
        }

    >Retrieving Booking
    GET api/v1/booking?book_id=<bookid>

8 **Get show details based on city and movie**
    >Get all shows with cinema details and movie details
    GET api/v1/get_shows/

    >Filtering shows on basis of city and movie
     GET api/v1/get_shows?city=<cinema_city>
     GET api/v1/get_shows?movie=<movie_string>

     *You can use multiple query parameters