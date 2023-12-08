CREATE TABLE wallet_scorings (
    activity_id INT,
    wallet TEXT,
    protocol_activity FLOAT,
    competitors_activity FLOAT,
    program_engagement FLOAT,
    sybil_likelihood FLOAT,
    dt TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
);

