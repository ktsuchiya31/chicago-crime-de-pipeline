{{ config(schema='chicago_marts') }}

with source as (
    select * from {{ ref('stg_crime_reports') }}
),

aggregated as (
    select
        district,
        year,
        count(*) as total_crimes,
        sum(case when arrest = true then 1 else 0 end) as total_arrests,
        sum(case when domestic = true then 1 else 0 end) as total_domestic,
        round(
            sum(case when arrest = true then 1 else 0 end)::float 
            / nullif(count(*), 0) * 100, 2
        ) as arrest_rate_pct
    from source
    where district is not null
    group by district, year
)

select * from aggregated
order by year, total_crimes desc