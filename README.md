# Flowbroker

The Flowbroker is a proof-of-concept for a system architecture allowing to make RFC 5575 compliant Flow Specification Rules accessible to end users securely.
It was developed as part of my Bachelor's thesis at Saarland University of Applied Sciences (htw saar, Saarbrücken, Germany) in 2016.

## Quick Start

Our Broker Server implementation relies on EXABGP. 
In order to use our server, please install EXABGP first. This can easily be done using **pip**:

> **$** pip install exabgp

To install the server module, which can be used in conjunction with the tool by exanetworks, please execute our setup script:

> **$** python ./src/client/setup.py install

In order to use the server, you then need to create a configuration file for EXABGP which uses our server. The Listing below shows a sample configuration file:

```ini
group test {
	 neighbor 10.10.100.1 {
         router-id 1.2.3.4;
         local-address 10.10.100.68; 
         local-as 100;
         peer-as 100;
         graceful-restart;
         process broker-server {
             run /usr/local/bin/exabgp-broker-server;
         }
     }
 }    
```
Save the file to a directory (e.g. `/etc/exabgp/exabgp.conf`)
We then need to create a configuration file for our server implementation. You can find a sample configuration in `./src/client/config.yml`. When starting the server, it will search for a configuration file in three different paths. It will use the first file in the list which is accessible:

1. `/etc/broker-server/config.yml`
2. `/etc/exabgp/broker-server/config.yml`
3. `./config.yml`

After placing a configuration in one of the paths shown above, we can start EXABGP and our server implementation by starting the EXABGP script:

> **$** exabgp /etc/exabgp/exabgp.conf
