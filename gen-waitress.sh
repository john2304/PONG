#!/usr/bin/bash

cat > webtech.service << END
# /etc/systemd/system/helloapp.service
[Unit]
Description=Your App Name
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/home/$USER/PONG
ExecStart=/home/$USER/PONG/bin/waitress-serve --listen=127.0.0.1:5000 server:app
Restart=always

[Install]
WantedBy=multi-user.target
END
