#! /bin/sh
#! /bin/bash

export OSQUERY_KEY=1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B
echo `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $OSQUERY_KEY`
echo `sudo add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main'`
echo `sudo apt-get update`
echo `sudo apt-get install -y osquery`
echo `sudo apt-get install -y rsyslog`
echo `sudo touch /etc/rsyslog.d/osquery.conf`
echo `sudo touch /etc/osquery/osquery.conf`
echo `sudo touch /usr/share/osquery/packs/fim.conf`
echo `sudo cp agent/conf/rsyslog_osquery.conf /etc/rsyslog.d/osquery.conf`
echo `sudo cp agent/conf/fim_osquery.conf /etc/osquery/osquery.conf`
