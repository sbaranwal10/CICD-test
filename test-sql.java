public static final String SHOW_PARAMETERS_FOR_WAREHOUSE = "show parameters for warehouse ";
public static final String SHOW_WAREHOUSES = "show warehouses";
public static final String SELECT_WAREHOUSE_ID_NAME = "SELECT DISTINCT WAREHOUSE_ID, WAREHOUSE_NAME FROM (" +
            "SELECT DISTINCT warehouse_id AS WAREHOUSE_ID, warehouse_name AS WAREHOUSE_NAME " +
            "FROM ${db}.${schema}.warehouse_events_history UNION ALL " +
            "SELECT DISTINCT warehouse_id AS WAREHOUSE_ID, warehouse_name AS WAREHOUSE_NAME " +
            "FROM ${db}.${schema}.warehouse_metering_history UNION ALL " +
            "SELECT DISTINCT warehouse_id AS WAREHOUSE_ID, warehouse_name AS WAREHOUSE_NAME " +
            "FROM ${db}.${schema}.warehouse_load_history UNION ALL " +
            "SELECT DISTINCT warehouse_id AS WAREHOUSE_ID, warehouse_name AS WAREHOUSE_NAME "
            + "FROM ${db}.${schema}.query_history) ORDER BY WAREHOUSE_ID;";
public static final String SELECT_WAREHOUSE_SUSPEND_TIME = "select warehouse_id, warehouse_name, max(timestamp) as "
            + "suspended_on from ${db}.${schema}.warehouse_events_history where event_name='SUSPEND_WAREHOUSE' and "
            + "event_state='COMPLETED' group by warehouse_id, warehouse_name order by warehouse_id;";
public static final String RT_QUERY_COUNT_IS = "SELECT count(1) as count from TABLE "
            + "(snowflake.information_schema.query_history(dateadd('DAYS', -2, CURRENT_TIMESTAMP), null, 10000));";
public static final String RT_QUERY_COUNT_REPLICATION = "SELECT count(1) as count from "
            + "${db}.${schema}.is_query_history WHERE start_time > dateadd('DAYS', -2, CURRENT_TIMESTAMP);";
