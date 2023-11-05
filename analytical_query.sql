
-- top 100 popular restaurant
SELECT restaurant.name,
       review.reviews_nr as reviews,
       review.rating,
       category.category
FROM restaurant
JOIN review ON restaurant.gid = review.gid
JOIN category ON review.category_id = category.category_id
ORDER By reviews DESC
LIMIT 100;

-- to 100 chain restaurant
SELECT restaurant.name,
       review.reviews_nr as reviews,
       review.rating,
       category.category
FROM restaurant
JOIN review ON restaurant.gid = review.gid
JOIN category ON review.category_id = category.category_id
ORDER By reviews DESC
LIMIT 100;

-- full sigle table
CREATE or REPLACE christgett.full_table AS (
    SELECT re.name,
           ca.category,
           pr.price_level,
           f.rating,
           f.reviews_nr as reviews,
           cl.cluster,
           ch.name_chain,
           lo.province,
           lo.region
    FROM review f
    JOIN restaurant re ON f.gid = re.gid
    JOIN category ca ON f.category_id = ca.category_id
    JOIN price_level pr ON f.price_level_id = pr.price_level_id
    JOIN cluster cl ON f.cluster_id = cl.cluster_id
    LEFT JOIN chain ch ON f.chain_id = ch.chain_id
    JOIN location lo ON f.location_id = lo.location_id
);