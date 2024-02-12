public static final Logger LOG = LoggerFactory.getLogger(AbstractDmProcessor.class);
    protected static final Map<SnowflakeTable, Category> snowflakeTableCategoryMap = new HashMap<>();
    protected static final String PIPELINE_ENTITY_PREFIX = "polling ";
    protected static final String PIPELINE_DETAILS_QUERY_HISTORY = "poll for Query History";

    protected static final String PIPELINE_DETAILS_COMPUTE_CHARGE = "poll for Warehouse Charging History";

    protected static final String PIPELINE_DETAILS_COMPUTE_LOAD = "poll for Warehouse Loading History";

    protected static final String PIPELINE_DETAILS_COMPUTE_BASE = "poll for Warehouse Base Info";

    protected static final String PIPELINE_DETAILS_COMPUTE_EVENTS = "poll for Warehouse Events History";
    protected static final String PIPELINE_DETAILS_METERING_HISTORY = "poll for Warehouse Events History";
    protected static final String PIPELINE_DETAILS_METERING_DAILY_HISTORY = "poll for Warehouse Events History";
    public static final String WAREHOUSE = "WAREHOUSE";
    public static final String VALUE = "VALUE";
    public static final String KEY = "KEY";
    static final long ONE_DAY_IN_MILLIS = 24L * 60 * 60 * 1000;
    private static final long SECOND2MILLIS = 1000;
    private static final long DEFAULT_WAREHOUSE_TIMEOUT = 2L * ONE_DAY_IN_MILLIS;

    public static final String OFFSET = "Z";
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
    public static final long DEFAULT_FAILED_QUERY_ROW_COUNT = -1;
    public static final long KAFKA_LAG_IS_TOO_HIGH = -2;
    public static final long DATA_REPLICATION_NOT_DONE = -3;
    public static final String OFFSET_FORMAT = "/*{{_OFFSET}}*/";
    public static final String PROFILE_TASK = "profile_task";
    public static final String HISTORY_QUERY_TASK = "history_query_task";
    public static final String REALTIME_QUERY_TASK = "realtime_query_task";
    public static final int FIVE_MIN_SLOTS_MAX_SIZE = 2 * 24 * 12;
    public static final int MAX_QUERY_COUNT = 10000;
