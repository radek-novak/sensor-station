install:
	cp sensor_station.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable sensor-station.service
	systemctl start sensor-station.service 

restart:
	systemctl reload-or-restart sensor-station.service 

deploy-from-host:
	scp ./* pi@raspberrypi:/home/pi/bin/station
	ssh pi@raspberrypi "cd bin/station; sudo make restart"