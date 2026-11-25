import duckdb

output = duckdb.sql("""
    SELECT *
    FROM 'output.parquet'
    """
)

silver = duckdb.sql("""
        SELECT DISTINCT
            TRIM(session_id) AS session_id,
            session_date,
            customer_id
            store_id,
            TRIM(device_type) AS device_type,
            SPLIT_PART(TRIM(browser_os), '|', 1) AS browser,
            SPLIT_PART(TRIM(browser_os), '|', 2) AS os,
            session_purchase_made,
            session_duration_minutes,
            session_pages_visited,
            COALESCE(session_quality_score, avg(session_quality_score) OVER ()) AS session_quality_score
        FROM 'output.parquet'
        """
)

duckdb.sql("""
    COPY (
        SELECT DISTINCT 
            TRIM(session_id) AS session_id,
            session_date,
            customer_id
            store_id,
            TRIM(device_type) AS device_type,
            SPLIT_PART(TRIM(browser_os), '|', 1) AS browser,
            SPLIT_PART(TRIM(browser_os), '|', 2) AS os,
            session_purchase_made,
            session_duration_minutes,
            session_pages_visited,
            COALESCE(session_quality_score, avg(session_quality_score) OVER ()) AS session_quality_score
            FROM 'output.parquet'
    )
    TO 'silver_output.parquet'
    (FORMAT PARQUET);
""")
