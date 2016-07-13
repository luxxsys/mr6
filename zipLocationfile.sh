#!/bin/bash

day=`date +%Y%m%d`
size=`stat --format=%s mr6_locationfile`
if [ $size -gt 1000 ]; then
	tar czf mr6_location.${day}.tar.gz mr6_locationfile
	rm mr6_locationfile
	touch mr6_locationfile
fi
