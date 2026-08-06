with source as (
    select * from {{ source('chicago_raw', 'crimes') }}
),

cleaned as (
    select
        id,
        case_number,
        cast(date as timestamp) as crime_date,
        block,
        iucr,
        primary_type,
        description,
        location_description,
        arrest,
        domestic,
        beat,
        district,
        ward,
        community_area,
        fbi_code,
        cast(x_coordinate as float) as x_coordinate,
        cast(y_coordinate as float) as y_coordinate,
        cast(year as int) as year,
        cast(updated_on as timestamp) as updated_on,
        cast(latitude as float) as latitude,
        cast(longitude as float) as longitude,
        row_number() over (partition by id order by cast(date as timestamp) desc) as rn
    from source
    where id is not null
)

select
    id,
    case_number,
    crime_date,
    block,
    iucr,
    primary_type,
    description,
    location_description,
    arrest,
    domestic,
    beat,
    district,
    ward,
    community_area,
    fbi_code,
    x_coordinate,
    y_coordinate,
    year,
    updated_on,
    latitude,
    longitude
from cleaned
where rn = 1