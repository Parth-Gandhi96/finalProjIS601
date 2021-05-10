select * from movieData;


# Top 10 most profited movies in last 50 years
select t.film_title,t.worldwide_gross,t.film_budget,(t.worldwide_gross-t.film_budget)*100/t.film_budget as profit
from movieData t order by profit desc limit 10;

# IMDB range wise avg movie profit
select
       (t.imdb)-1 as a,
       (t.imdb) as b,
       round(avg((t.worldwide_gross-t.film_budget)*100/t.film_budget)) as avg_profit
from (select *,ceil(imdb_rating) as imdb from movieData) t
group by t.imdb;

# fetching all the genores
select * from (
        (select distinct (genre_1) from movieData where genre_1 is not null) union
        (select distinct (genre_2) from movieData where genre_2 is not null) union
        (select distinct (genre_3) from movieData where genre_3 is not null)) a;

# Genre wise movie's avg collections:
select
        (t.genre_1) as genre,
        round(avg((t.worldwide_gross-t.film_budget)*100/t.film_budget)) as avg_profit,
        count(*) as count
from movieData t
group by t.genre_1;
