SELECT date(time), sensors.name, avg(value), min(value), max(value) 
FROM sensordata 
JOIN sensors ON sensordata.sensor_id = sensors.id 
WHERE date('now', '-1 day') = date(time)
GROUP BY sensor_id;
