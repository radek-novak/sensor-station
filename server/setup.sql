CREATE TABLE IF NOT EXISTS sensors (
  -- it increments by default without need for AUTOINCREMENT
  -- https://www.sqlite.org/autoinc.html
  id INTEGER PRIMARY KEY, 
  name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS sensordata (
  id TEXT UNIQUE,
  time TEXT,
  sensor_id INTEGER,
  value REAL,
  FOREIGN KEY(sensor_id) REFERENCES sensors(id)
);

CREATE TABLE IF NOT EXISTS experiments (
  time_start TEXT,
  time_end TEXT,
  description TEXT
);
