#!/bin/bash
echo "Copy supervisor configuration for api service"
sudo cp -f ./api.conf /etc/supervisor/conf.d/api.conf
sudo supervisorctl reread
sudo supervisorctl reload
