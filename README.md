# CS433-assignment2


**First Part**
1. Run the file of the first question ```first.py``` by following the command
   ```sudo python first.py```
2. For the b part, we chose the router A.

   First open the xterm for A by running command ```xterm A```

   Then in that terminal use command ```tcpdump -n -i ra-eth2 -w output.pcap```

   Also ping ```ra ping rb``` or ```h1 ping h6``` to generate flow of packets through router A. After sometime end the process using ```ctrl + c```.
   It will create a ```.pcap``` file which can be analyzed by wireshark.
  
3. For the d part dump the routing tables by routers using ```ra route -n``` for router A and similarly for other routers.


**Second Part**
1. Run the file for second part by using command ```sudo python second.py```.
2. For the second part run the file and open the xterm for H1 & H4 by using command ```xterm H1 H4```.
   Now in the server i.e in H4 run following command
   ```wireshark -i eth0 & python3 client_server.py --r server --p 5001 --config b --c vegas```
   Change the congestion control by using the respective name in for congestion ```--c``` field.

   Now for the client H1
   ```wireshark -i eth0 & python3 client_server.py --r client --p 5001 --config b --c vegas```

   It will also open wireshark in background process. 
3. For third part open the xterm for all the parts and run the client part in H1, H2 and H3 and server in H4.
4. For the d part just vary the link loss parameter in ```second.py```.

   ```self.addLink(S1,S2,loss=3)```

