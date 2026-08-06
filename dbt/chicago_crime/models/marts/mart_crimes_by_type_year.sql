{{ config(schema='chicago_marts') }}

with source as (
    select * from {{ ref('stg_crime_reports') }}
),

aggregated as (
    select
        primary_type,
        year,
        count(*) as total_crimes,
        sum(case when arrest = true then 1 else 0 end) as total_arrests,
        round(
            sum(case when arrest = true then 1 else 0 end)::float 
            / nullif(count(*), 0) * 100, 2
        ) as arrest_rate_pct
    from source
    where primary_type is not null
    group by primary_type, year
)

select * from aggregated
order by year, total_crimes desc