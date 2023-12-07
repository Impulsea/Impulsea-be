CREATE TABLE metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name TEXT
);

CREATE TABLE activities_stats (
    activity_id INT REFERENCES activities(activity_id),
    metric_id INT REFERENCES metrics(metric_id),
    dt TIMESTAMP,
    value FLOAT
);
