-- models/migrate_to_snowflake.sql

with postgres_data as (
    select * from {{ source('postgres_source', 'employee') }}
)

select * from employee_data
