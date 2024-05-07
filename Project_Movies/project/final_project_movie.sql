/* 1- What is the data structure? What information do we have available for movies?

Display the (whole) movies table.*/

select * from movies;

/* 2 - In the movies table there is a field called movieId. Sometimes we will not need this field for the analysis.

Display only title and genres of the first 10 entries from the movies table that is sorted alphabetically (starting from A) by the movie titles.*/

select genres , title from movies where title like 'A%' order by title limit 10;

/* 3 - How many movies do we have the data for?

Display the total row count */

select count(*) from movies;

/* 4- Display first 10 pure Drama movies. Only Drama is in the genre column.
   Display the count of pure Drama movies.*/

select * from movies where genres = 'Drama' limit 10;
select count(genres) from movies where genres= 'Drama';

/* 5- Display the count of drama movies that can also contain other genres.*/
select count(*) from movies where genres ilike '%Drama%';

/* 6- Display the count of movies don’t have drama (in any combination) as assigned genre*/
select count(*) from movies where genres != 'Drama';

/* 7-Display the count of movies that were released in 2003.*/
select count(*) from movies where movieyear = '2003';

/* 8- Find all movies with a year lower 1910.*/
select count(*) from movies where movieyear < '1910';

/*9- Retrieve all Star Wars movies from the movie table*/
select * from movies where title ilike '%Star Wars%'


/*Display the total row count of the ratings table.*/
select count(*)  from ratings;

/* Display the total count of different genres combinations in the movies table. */
select count(genres) from movies;
select * from ratings;
select * from movies;

/*Display unique tags for movie with id equal 60756. Use tags table.*/
select distinct tag from tags where movieid = '60756';

/*Display the count of movies in the years 1990-2000 using the movies table. Display year and movie_count.*/
select year, movieid  from movies where year between 1990 and 2000;

/*Display the year where most of the movies in the database are from.*/
select year, count(*) as movie_count from movies
group by year order by movie_count desc limit 1;

/*Display 10 movies with the most ratings. Use ratings table. Display movieid, count_movie_ratings*/
select movieid,  count(*)  as count_movie_ratings from ratings
group by movieid order by count_movie_ratings DESC limit 10;
select * from ratings

/*Display the top 10 highest rated movies by average that have at least 50 ratings. Display the movieid, average rating and rating count. Use the ratings table.*/
select movieid, count(rating), avg(rating)  as average_rating from ratings
group by movieid having count(rating) >50  order by average_rating  limit 10;

/*Create a view that is a table of only movies that contain drama as one of it’s genres. Display the first 10 movies in the view.*/
create view style_view1 as select * from movies  where genres ilike '%Drama%' limit 10;
select * from style_view1
3:15
Display the total row count of the ratings table.*/
select count(*)  from ratings;

/* Display the total count of different genres combinations in the movies table. */
select count(genres) from movies;
select * from ratings;
select * from movies;

/*Display unique tags for movie with id equal 60756. Use tags table.*/
select distinct tag from tags where movieid = '60756';

/*Display the count of movies in the years 1990-2000 using the movies table. Display year and movie_count.*/
select year, movieid  from movies where year between 1990 and 2000;

/*Display the year where most of the movies in the database are from.*/
select year, count(*) as movie_count from movies
group by year order by movie_count desc limit 1;

/*Display 10 movies with the most ratings. Use ratings table. Display movieid, count_movie_ratings*/
select movieid,  count(*)  as count_movie_ratings from ratings
group by movieid order by count_movie_ratings DESC limit 10;
select * from ratings

/*Display the top 10 highest rated movies by average that have at least 50 ratings. Display the movieid, average rating and rating count. Use the ratings table.*/
select movieid, count(rating), avg(rating)  as average_rating from ratings
group by movieid having count(rating) >50  order by average_rating  limit 10;

/*Create a view that is a table of only movies that contain drama as one of it’s genres. Display the first 10 movies in the view.*/
create view style_view1 as select * from movies  where genres ilike '%Drama%' limit 10;
select * from style_view1


/*1-Using a JOIN display 5 movie titles with the lowest imdb ids*/

create table movies_title_imd as(
SELECT movies.title as movie_title , movie_links.imdbId as imdbId
FROM movies
full join movie_links
using (movieid)
);

select movie_title from movies_title_imd order by imdbId limit 5;


/*2-Display the count of drama movies*/

select count(genres) from movies where genres= 'Drama';

/*3-Using a JOIN display all of the movie titles that have the tag fun*/

SELECT movies.title as movie_title, movie_tags.tag as tag
FROM movies
full JOIN movie_tags 
using(movieid)
WHERE tag ilike '%fun%';


/*4-Using a JOIN find out which movie title is the first without a tag*/

SELECT movies.title as movie_title, movie_tags.tag as tag
FROM movies
full JOIN movie_tags 
using(movieid)
WHERE tag is null 
order by movieid
limit 1;

/*5-Using a JOIN display the top 3 genres and their average rating*/

SELECT movies.genres as movie_genres, AVG(movie_ratings.rating) as average_rating
FROM movies
JOIN movie_ratings
using(movieid)
GROUP BY genres
ORDER BY average_rating DESC
LIMIT 3;


/*6-Using a JOIN display the top 10 movie titles by the number of ratings*/

SELECT movies.title as movie_title, count(rating) as number_ratings
FROM movies
JOIN movie_ratings
using (movieid)
GROUP BY movie_title
ORDER BY number_ratings DESC
LIMIT 10;

/*7-Using a JOIN display all of the Star Wars movies in order of average rating where the film was rated by at least 40 users*/
SELECT movies.title as movie_title, avg(movie_ratings.rating) as average_rating
FROM movies
JOIN movie_ratings
using(movieid)
WHERE title LIKE 'Star Wars%'
GROUP BY movie_title
HAVING COUNT(userid) >= 40
ORDER BY average_rating DESC;



/*8-Create a derived table from one or more of the above queries*/
create table Starwars_movies as (SELECT movies.title as movie_title, avg(movie_ratings.rating) as average_rating
FROM movies
JOIN movie_ratings
using(movieid)
WHERE title LIKE 'Star Wars%'
GROUP BY movie_title
HAVING COUNT(userid) >= 40
ORDER BY average_rating desc);

select * from Starwars_movies






--Number of movies released each 
SELECT movieyear, COUNT(*) AS num_movies
FROM movies
GROUP BY movieyear
ORDER BY movieyear;


--Average movie rating

SELECT AVG(rating) AS avg_rating
FROM movie_ratings;

--Top 10 best rated movies

SELECT movies.title as movie_title, count(rating) as number_ratings
FROM movies
JOIN movie_ratings
using (movieid)
GROUP BY movie_title
ORDER BY number_ratings DESC
LIMIT 10;


--Top 10 genres and their average rating 

SELECT movies.genres as movie_genres, AVG(movie_ratings.rating) as average_rating
FROM movies
JOIN movie_ratings
using(movieid)
GROUP BY genres
ORDER BY average_rating DESC
LIMIT 10;

--Count of Comedy/Horror movies: 

select count(genres) from movies where genres ilike '%Crime%';
select count(genres) from movies where genres ilike '%Horror%';
select count(genres) from movies where genres ilike '%Action%';

--Average rating of Comedy/Horror/Drama movies:

SELECT movies.genres as movie_genres, AVG(movie_ratings.rating) as average_rating
FROM movies
JOIN movie_ratings
using(movieid)
WHERE movies.genres IN ('Crime', 'Horror', 'Action')
GROUP BY genres
ORDER BY average_rating DESC;



--Top 10 genres and their average rating 

SELECT movie_tags.tag as movie_tagss, AVG(movie_ratings.rating) as average_rating
FROM movie_tags
JOIN movie_ratings
using(movieid)
GROUP BY tag
ORDER BY average_rating DESC
LIMIT 10;


--Average rating of a couple tags movies:

SELECT movie_tags.tag as movie_tagss, AVG(movie_ratings.rating) as average_rating
FROM movie_tags
JOIN movie_ratings
using(movieid)
WHERE tag IN ('nonsense', 'Ryan Reynolds', 'Emilia Clarke', 'Samuel L. Jackson')
GROUP BY tag
ORDER BY average_rating DESC;


-- count of those tags: 
select count(tag) from movie_tags where tag ilike '%Samuel L. Jackson%';
select count(tag) from movie_tags where tag ilike '%Ryan Reynolds%';
select count(tag) from movie_tags where tag ilike '%Quentin Tarantino%';


--year with most movies from Quentin Tarantino: 


SELECT movies.movieyear, COUNT(*) AS num_movies
FROM movies
JOIN movie_tags
using (movieid)
WHERE tag ilike '%Quentin Tarantino%'
GROUP BY movieyear
ORDER BY num_movies DESC
LIMIT 10;


--create new range column 

drop table if exists average_table;
create table average_table as( 
SELECT
    movies.title as movie_title,
    AVG(movie_ratings.rating) as avg_movie_rating
    from movies
    join movie_ratings
    using(movieid)
    group by (movie_title))
    limit 1000;
   
    select * from average_table
    
 SELECT *, CASE
				WHEN avg_movie_rating > 4 THEN 'very good'
				WHEN avg_movie_rating between 3 and 4 then 'good'
				ELSE 'bad'
		  END AS rating_range
FROM average_table;