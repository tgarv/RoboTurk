SHELL := /bin/bash

run:
	source venv/bin/activate
	sudo sh run.sh

clear:
	sudo python3 scripts/clear_pixels.py

configure:
	sudo python3 game/board_space_configurator.py $(spaces)

test:
	sudo python3 game/board_space_tester.py
	
test2:
	sudo python3 game/board_space_tester_i2c.py

disable-ap:
	sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.copy
	sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.copy
	sudo mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.copy
	echo "Files moved - run sudo systemctl reboot for changes to take effect"

enable-ap:
	sudo cp /etc/dhcpcd.conf.copy /etc/dhcpcd.conf
	sudo cp /etc/dnsmasq.conf.copy /etc/dnsmasq.conf
	sudo cp /etc/hostapd/hostapd.conf.copy /etc/hostapd/hostapd.conf
	echo "Files moved - run sudo systemctl reboot for changes to take effect"

reboot:
	sudo systemctl reboot
