#!/bin/bash
echo "Copy supervisor configuration for facebook workers"
sudo cp -f ./facebook_workers.conf /etc/supervisor/conf.d/facebook_workers.conf
sudo supervisorctl reread
sudo supervisorctl update
