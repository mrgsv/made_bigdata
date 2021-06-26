DROP TABLE IF EXISTS ip_regions;

CREATE EXTERNAL TABLE ip_regions (
    ip STRING,
    region STRING
)
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/data/user_logs/ip_data_M';


DROP TABLE IF EXISTS users;

CREATE EXTERNAL TABLE users (
    ip STRING,
    browser STRING,
    sex STRING,
    age INT
)
ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
STORED AS textfile
LOCATION '/data/user_logs/user_data_M';


ADD JAR /usr/local/hive/lib/hive-serde.jar;

DROP TABLE IF EXISTS logs_raw;

CREATE EXTERNAL TABLE logs_raw (
    ip STRING,
    `date` STRING,
    request STRING,
    page_size INT,
    http_status INT,
    user_agent STRING
)
ROW FORMAT
    serde 'org.apache.hadoop.hive.serde2.RegexSerDe'
    with serdeproperties (
        "input.regex" = "^(\\S*)\\t{3}(\\d*)\\t+(\\S+)\\t+(\\d+)\\t+(\\d+)\\t+(\\S+) .*"
)
STORED AS TEXTFILE
LOCATION '/data/user_logs/user_logs_M';


set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.max.dynamic.partitions.pernode=116;

DROP TABLE IF EXISTS logs;

CREATE TABLE logs (
    ip STRING,
    request STRING,
    page_size INT,
    http_status INT,
    user_agent STRING
) PARTITIONED BY (`date` STRING);

INSERT OVERWRITE TABLE logs PARTITION(`date`)
    SELECT ip, request, page_size, http_status, user_agent, SUBSTR(`date`, 1, 8) AS `date`
    FROM logs_raw;