CREATE KEYSPACE Message WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

CREATE TABLE message.message_by_sender (
   sender_id TEXT,
   time timestamp,

   receiver_id TEXT,
   message TEXT,
   audience TEXT,

   asset_name TEXT,

   PRIMARY KEY ((sender_id), time)
) WITH CLUSTERING ORDER BY (time DESC);

CREATE TABLE message.message_by_receiver (
   receiver_id TEXT,
   time timestamp,

   sender_id TEXT,
   message TEXT,
   audience TEXT,

   asset_name TEXT,

   PRIMARY KEY ((receiver_id), time)
) WITH CLUSTERING ORDER BY (time DESC);