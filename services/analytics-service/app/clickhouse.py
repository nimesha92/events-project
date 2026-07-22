import os

import clickhouse_connect


def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=os.getenv(
            "CLICKHOUSE_HOST",
            "clickhouse.clickhouse.svc.cluster.local",
        ),
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "ClickHouse123!"),
        database=os.getenv("CLICKHOUSE_DATABASE", "analytics"),
    )