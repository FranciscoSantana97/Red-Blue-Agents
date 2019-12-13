#! /bin/sh
#! /bin/bash

echo `sudo apt-get install -y ethtool build-essential libpcap-dev libpcre3-dev libdumbnet-dev zlib1g-dev bison flex`
echo `mkdir -p ~/snort`
echo `wget -P ~/snort/ https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz`
echo `wget -P ~/snort/ https://www.snort.org/downloads/snort/snort-2.9.15.tar.gz`
echo `wget -P ~/snort/ http://luajit.org/download/LuaJIT-2.0.5.tar.gz`
echo `tar -xvzf ~/snort/daq-2.0.6.tar.gz -C ~/snort`
echo `tar -xvzf ~/snort/snort-2.9.15.tar.gz -C ~/snort`
echo `tar -xvzf ~/snort/LuaJIT-2.0.5.tar.gz -C ~/snort`
echo `cd ~/snort/LuaJIT-2.0.5 && sudo make && sudo make install`
echo `cd ~/snort/daq-2.0.6 && sudo ./configure && sudo make && sudo make install`
echo `cd ~/snort/snort-2.9.15 && sudo ./configure --disable-open-appid && sudo make && sudo make install && sudo ldconfig`
echo `sudo ln -s /usr/local/bin/snort /usr/sbin/snort`
echo `sudo mkdir -p /etc/snort`
echo `sudo mkdir -p /etc/snort/rules`
echo `sudo mkdir -p /etc/snort/preproc_rules`
echo `sudo touch /etc/snort/rules/white_list.rules`
echo `sudo touch /etc/snort/rules/black_list.rules`
echo `sudo touch /etc/snort/rules/local.rules`
echo `sudo mkdir -p /var/log/snort`
echo `sudo mkdir -p /usr/local/lib/snort_dynamicrules`
echo `sudo chmod -R 5775 /etc/snort`
echo `sudo chmod -R 5775 /var/log/snort/`
echo `sudo chmod -R 5775 /usr/local/lib/snort_dynamicrules/`
echo `sudo cp ~/snort/snort-2.9.15/etc/*.conf* /etc/snort`
echo `sudo cp ~/snort/snort-2.9.15/etc/*.map* /etc/snort`
echo `sudo cp /etc/snort/snort.conf /etc/snort/snort.conf_orig`
echo `sudo sed -i 's/include \$RULE\_PATH/\#include \$RULE\_PATH/' /etc/snort/snort.conf`
echo `sudo sed -i 's/whitelist \$WHITE/\# whitelist \$WHITE/' /etc/snort/snort.conf`
echo `sudo sed -i 's/blacklist \$BLACK/\# blacklist \$BLACK/' /etc/snort/snort.conf`
echo `sudo sed -i 's/var WHITE\_LIST\_PATH \.\.\/rules/var WHITE\_LIST\_PATH \/etc\/snort\/rules/' /etc/snort/snort.conf`
echo `sudo sed -i 's/var BLACK\_LIST\_PATH \.\.\/rules/var BLACK\_LIST\_PATH \/etc\/snort\/rules/' /etc/snort/snort.conf`
echo `sudo sed -i 's/var RULE\_PATH \.\.\/rules/var RULE\_PATH \/etc\/snort\/rules/' /etc/snort/snort.conf`
echo `sudo sed -i 's/var SO\_RULE\_PATH \.\.\/so\_rules/var SO\_RULE\_PATH \/etc\/snort\/so\_rules/' /etc/snort/snort.conf`
echo `sudo sed -i 's/var PREPROC\_RULE\_PATH \.\.\/preproc\_rules/var PREPROC\_RULE\_PATH \/etc\/snort\/preproc\_rules/' /etc/snort/snort.conf`
echo `sudo sed -i 's/\#include \$RULE\_PATH\/local\.rules/include \$RULE\_PATH\/local\.rules/' /etc/snort/snort.conf`