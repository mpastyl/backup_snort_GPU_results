#!/bin/bash

versions=(0 1 2 3)
#speeds=(200 300 400 500 600 700 800)
speeds=(10 20 30 40 50 60 70 75 80 90 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 300 350 400 450 500 550 600 650 700 750 800)
#speeds=(50 100 150)
#speeds=(10 20 40 70)

for ver in "${versions[@]}"
do

ssh odroid@10.168.1.126 /bin/bash <<EOF
cd /home/odroid/snort_GPU_system/Master/src/search_engines
sed -i -e "s/USE_GPU [0-9]/USE_GPU $ver/g" acsmx2.h
cd /home/odroid/snort_GPU_system/Master/build
make -j 8 install
EOF
	for s in "${speeds[@]}"
	do
	for i in `seq 1 5`
	do
		ssh odroid@10.168.1.126 /bin/bash <<"EOF"
		export LUA_PATH="/home/odroid/snort_GPU_system_build/include/snort/lua/?.lua;;"
		export SNORT_LUA_PATH=/home/odroid/snort_GPU_system_build/etc/snort
		cd /home/odroid/snort_GPU_system_build
		sudo LUA_PATH=$LUA_PATH SNORT_LUA_PATH=$SNORT_LUA_PATH ./bin/snort -i eth0 -R ~/Downloads/snort3-community-rules/snort3-community.rules  -c ~/Downloads/clort.lua  > log.txt &
EOF
			
		sleep 10
		#sudo tcpreplay -i en3 --loop=1 --mbps=$s /Users/mpastyl/snort_GPU_plots/testbed-13jun_1.pcap
		sudo tcpreplay -i en3 --loop=1000 --mbps=$s --unique-ip /Users/mpastyl/Desktop/web-stream.pcap
		#sudo tcpreplay -i en3 --loop=1 --mbps=$s --duration=5 /Users/mpastyl/snort_GPU_plots/testbed-13jun_1.pcap
		sleep 2
		ssh odroid@10.168.1.126 /bin/bash <<EOF
		sudo pkill -SIGTERM snort
EOF
		sleep 2
		scp odroid@10.168.1.126:/home/odroid/snort_GPU_system_build/log.txt /Users/mpastyl/snort_GPU_plots/logs_from_snort/result_proper_big_dataset_proper_config_web_stream_$ver"_"$s"_"$i".txt"
	done
	done
done
