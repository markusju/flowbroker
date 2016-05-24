
<Request> = <method> | <method> \n <parameters>

<method> = <methodName> <args> | <methodName>
<methodName> = DISCARD | RATE-LIMIT <LimitSpecifier>

<parameterS> = <parameter> | <parameter> \n <parameterS>
<parameter> = <key>: <value>

<args> = <ipcidr>
<ipcidr> = ##REGEX IP CIDR##










DISCARD 10.10.100.12/32
Destination: 192.168.42.40
Port: 80
Source-Port: 90
Destination-Port: 80
Protocol: tcp


RATE-LIMIT 9600 10.10.100.12/32
Destination: 192.168.42.40
Port:
Source-Port:
Destination-Port:
Protocol:



200 DISCARDED

201 RATE-LIMITED
