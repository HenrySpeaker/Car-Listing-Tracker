-- name: get_all_criteria
SELECT * FROM criteria;

-- name: get_criteria_by_info
SELECT * FROM criteria 
WHERE
    (:min_year::integer IS NULL OR min_year=:min_year) AND
    (:max_year::integer IS NULL OR max_year=:max_year) AND
    (:min_price::integer IS NULL OR min_price=:min_price) AND
    (:max_price::integer IS NULL OR max_price=:max_price) AND
    (:max_mileage::integer IS NULL OR max_mileage=:max_mileage) AND
    (:search_distance::integer IS NULL OR search_distance=:search_distance) AND
    (:no_accidents::boolean IS NULL OR no_accidents=:no_accidents) AND
    (:single_owner::boolean IS NULL OR single_owner=:single_owner) AND
    (:user_id::integer IS NULL OR user_id=:user_id) AND    
    (:city_id::integer IS NULL OR city_id=:city_id) AND
    (:model_id::integer IS NULL OR model_id=:model_id) AND
    (:body_style_id::integer IS NULL OR body_style_id=:body_style_id);

-- name: add_criteria!
INSERT INTO criteria (
    min_year,
    max_year,
    min_price,
    max_price,
    max_mileage,
    search_distance,
    no_accidents,
    single_owner,
    user_id,
    city_id,
    model_id,
    body_style_id
)
VALUES
(
    :min_year,
    :max_year,
    :min_price,
    :max_price,
    :max_mileage,
    :search_distance,
    :no_accidents,
    :single_owner,
    :user_id,    
    :city_id,
    :model_id,
    :body_style_id
);

-- name: delete_all_criteria!
DELETE FROM criteria;

-- name: delete_criteria_by_info!
DELETE FROM criteria 
WHERE
    (:min_year::integer IS NULL OR min_year=:min_year) AND
    (:max_year::integer IS NULL OR max_year=:max_year) AND
    (:min_price::integer IS NULL OR min_price=:min_price) AND
    (:max_price::integer IS NULL OR max_price=:max_price) AND
    (:max_mileage::integer IS NULL OR max_mileage=:max_mileage) AND
    (:search_distance::integer IS NULL OR search_distance=:search_distance) AND
    (:no_accidents::boolean IS NULL OR no_accidents=:no_accidents) AND
    (:single_owner::boolean IS NULL OR single_owner=:single_owner) AND
    (:user_id::integer IS NULL OR user_id=:user_id) AND    
    (:city_id::integer IS NULL OR city_id=:city_id) AND
    (:model_id::integer IS NULL OR model_id=:model_id) AND
    (:body_style_id::integer IS NULL OR body_style_id=:body_style_id);