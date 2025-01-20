# DBT Snowflake Migration

This guide provides instructions on how to use dbt to migrate a PostgreSQL database to Snowflake.

## Prerequisites

- PostgreSQL database
- Snowflake account
- dbt installed (`pip install dbt`)

## Steps

### 1. Set Up Your dbt Project

1. Create a new dbt project:
    ```sh
    dbt init dbt-snowflake-migration
    cd dbt-snowflake-migration
    ```

2. Update the `profiles.yml` file with your Snowflake and PostgreSQL connection details.

### 2. Configure Your Profiles

Edit the `profiles.yml` file to include both PostgreSQL and Snowflake configurations:

```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_snowflake_account>
      user: <your_snowflake_user>
      password: <your_snowflake_password>
      role: <your_snowflake_role>
      database: <your_snowflake_database>
      warehouse: <your_snowflake_warehouse>
      schema: <your_snowflake_schema>
      threads: 1

    postgres:
      type: postgres
      host: <your_postgres_host>
      user: <your_postgres_user>
      password: <your_postgres_password>
      dbname: <your_postgres_dbname>
      schema: <your_postgres_schema>
      port: 5432
```

### 3. Create Models

1. Create models in the `models/` directory to define the transformations needed for your data.

2. Example model (`models/model.sql`):
    ```sql
    select * from {{ source('postgres', 'your_table') }}
    ```

### 4. Run dbt

1. Run the dbt models to transform and load data into Snowflake:
    ```sh
    dbt run --target dev
    ```

### 5. Verify Data

1. Verify that the data has been successfully migrated to Snowflake by querying the Snowflake tables.

## Additional Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
