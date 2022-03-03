# IOT structures
There are three main layers:
1. Sensing Layer: Can sense information from teh environment
2. Network Layer: Get the information from the sensors to the applications.
3. Application Layer: Take the information from the sensors to use in an application.

## Sensing Layer
This layer is aware of different factors of the environment.
It can also be aware of the environment in different ways.

## Web Service
By having the data meet at a web application, we can reduce the cost of the application machinery.
For example, a distributed calculation can reduce the hardware needs.

## Service Pattern
If we want some code to execute on the remote server, we need to send the name of the procedure and arguments 
through HTTP. 
How can we avoid tight coupling between the remote object and the methods on the web app?

There is a process as to request/acknowledge or perform an inquiry on the server.
The request and and response is given once the request is authenticated.

Some languages such as WSDL (Web Services Description Language) allow to communicate b/w languages
that the computer understands and low-level sensors.
Computers can communicate as to their abilities.

Universal Description, Discovery and Integration (UDDI) allows entities to list themselves and be discovered on the internet.
Through different XML files, one entity could tell others what services they offer and an API.

SOAP is a way of sending information where the important information uses XML.
Having XML in the actual message speeds up the data processing done on the server, for example when we need to turn the message
into XML to save in the database.

Since computers and humans can both understand XML, it's very convenient to use.
Also allows for the remote PC to execute code.

EPCCGlobal 

## Virtualization
Virtualization is a method of having multiple operating systems running on a single machine.
Usually there would have to be a host operating system before we install the guest os.
However, with VmWare ESXi, this hypervisor can run on bare metal.

Xen is an open-source para-virtualizaiton method that can allow the guest os directly to communicate with the bare metal.
Kernel-based Virtual Machines are similar.

The hardware layer is the one that contains the memory  and calculation possiblity.

# Application Layer
# Future Challenges
The main goal is to enable communication between people and objects.
We can do it by **RFID**.
This is a method that has a short-range radio wave that allows something to identify itself.
We can do it so that cards can accept payments using this ID, objects in a factory, etc...

Smart networks embedded in devices, I guess such as sensors can improve the communication ability 
of machines almost as people.

One of the main goals of IOT networks is to be low-power, eco-friendly, and high performing.
Then we can have some form of remote control management.
The main challenges involved in achieving this aim: 
1. Unified sensing standard.
2. The ability for different networks to coexist and pass messages to each other.
3. Information aggregation and analysis (sending the information to more powerful server?)

Because of the large difference in networking designs and standards, in order to increase the transparency 
and effectiveness of a network there has to be some agreement on the standards to use.
Also important since there is a large amount of data to store and process, and different network protocols have to coexist.

To achieve cooperation of different network types, we have to take into acount message transparency and their coexistence into account.
For example, different wireless communication protocols have to be supported (WiFi, Bluetooth, Zigbee, etc...).
If there are any problems with the broadband as well we will encounter issues.

Another concern is when people move about while wearing these devices or the devces themselves have to use multiple networks.
Given this possibility for disruption, we also have to send complete information across devices.
Apart from differences in netwokrks, there are concerns with the effectiveness:
1. Channel attitude: If the device can change the channel it uses to send info it can be more adaptable.
2. Information quality and support: Make sure that the information sent is complete and accuratte.
3. Infosec: Protect the data from possible attacks.

All the data have to be efficiently distributed to different clients, since bandwidth and other resources might be limited.
Automation  and personal privacy in automated applications need to have a plan in place to respect user data.
Data collection and organization is also quite important, since the data originally might be quite messy.
Also in the movie "Avatar" all the beings live in an interconnected network without being limited by time or space.

## Platform Technologies(?)
Since IOT platforms are widely used in various domains, then having 
a simple experience for developers to use is important.
M2M (mahcine-to-machine) platform lets developers focus on higher-level functionality rather than focus
on implementation details.

## OneM2M

Then the application can collect data from the sensors using a **common horizontal layer**.
The idea is that all applications and different types of servers/networks can still talk to the sensors through a 
common network interface and common service layer.

Between the devices/sensors and the common network layer there might have to be a gateway to perform necessary transformations.
Without such an interface, developers would need to implement their own 3-layer architecture: service layer, logic layer and device layer.
However, sith a horizontan platform devs only need logic layer.

OpenM2M specifies different **Application Entities(AE)**, **Common Service Entity(CSE)**, **Network Service Entity**, and **Underlying network** structures.
These all are part of the application layer, common service layer, and network service layer, respectively.
Each layer is going to have their own entities.

The Application Entities just represents some application logic used for M2M solutions.
I guess this would be like the devices that actually make use of the Common Service Layer for some higher-level application?

The Common Service Entities are a common set of functions for M2M devices, they standardize the functionality of devices across networks and manufacturers.

The Network Service Entities allow the CSEs to access functionality from the underlying network.

The **Mca** allows the application entities to use the services from the common service entities,
The **Mcc** allows different common service entities to communicate with other CSEs, either in same or different domain.
The **Mcc'** allows a CSE to connect with an Infrastructure node 
The **Mcn** allows the common service entities to use the services provided by the network servce entities.

The **Mch** allows for "communication flows which transfer Charging Data Record (CDRs) generated by the Infrastructure
Node (IN) to an external charging server across the Mch reference point."
The Infrastructure nodes connect to other M2M service providers (I guess like  a "top level" node?)

In a single network there are some nodes that are capable of having CSEs and some that are not capable.
The non-CSE capable nodes will not be connected to the underlying network nodes.
There are abbrevs for Common Service Functions (CSF's):
1. ASM: Application and Service Layer Management
2. CMDH: Communication Management and Delivery Handling
3. DMR: Data Management and Repository CSF
4. DMG: Device Management
5. DIS: Discovery 
6. GMG: Group Management
7. LOC: Location
8. NSSE: Network Service Exposure, Service Execution and Triggering
9. REG: Registration
10. SEC: Security 
11. SCA: service Charging and Accounting
12. Subscription and Notification

- ASM: Manages the Applicaiton Entities and Common Service Entities
	- Application Dedicated Nodes
	- Application Service Nodes
	- Middle Nodes
	- Infrastructure Nodes
- CMDH: Determines which connection to use and when to buffer a request
	- A request may be buffered if there is no connection currently (?)
	- Uses role-based permissions to provide transparent data delivery.
	- Can store request
	- Accesses provisioned policies.
- DMR: Stores Data and mediates M2M communication
	- can store data from different entities
	- uses policies to grant access
	- converts data between formats for analysis and semantic processing
	- Can send the data to an intermediate node
	- Can send data to another CSE or an AE
	- Can perform analytics on large amounts of data
	- Can discover and interpret M2M data from different sources.
- DMG: Manages device capabilities on middle nodes, application service nodes, and application dedicated nodes.
	- Can also discover capability of other devices
- DIS: Gives information/resources residing on local or other CSEs.
	- Can filter devices based on certain criteria.
	- Returns the address of things found or information
- GMT: Group related requests
	- read, write, subscribe, notify, etc...
	- Relies on broadcasting and multicasting capabilities of the networks.

One M2M communicates using the **REST** architecture (Representational State Transfer).
REST architectures are a way of clients and servers to communicate with each other.
1. There is a uniform interface separating clients from servers. There is a clear separation
of function between the server's concerns and the clients so that the each side can be portable and scalable.
2. Stateless. No client information is stored in the server.
3. Cacheable. The clients can cache repsonses from the servers, and responses from the server must be labeled
as cacheable or not.
4. Layered system. The client cannot tell whether it's connected to the end server or a server along the way.

There are **resources** on the server which can be accessed with a URI.
There are then standardized ways for the server to communicate between the clients and these resources through the server.
We need to know the URI of the resource and the action we want to perform (GET, PUT, etc...).

The client receives a **representation** of the resource, which can be contained in an HTTP or JSON format.
There are four operations we can perform with REST: HTTP POST, HTTP PUT, HTTP DELETE, HTTP GET.
UPDATE and READ requests are **idempotent**, which means that multiple identical requests is the same as just making one request.
(Since they don't change anything on the server?)

REST is used in M2M because it allows easy visualization and management of various different sensor data.
Since it is stateless, scalability is easier as it avoids keeping client info, e.g. when we use some proxy server.
M2M applications can be developed using web technologies like HTML and JS.
A proxy server can make some request to the end server on behalf of the client.

A sensor could implement its own protocol to send its data. 
Therefore, the sensor could connect to a web server which recognizes its **native protocol** and implements REST to talk to
outside computers.
There might be a hierarchy of proxy servers which update in a certain time interval.
These proxies can cache the sensor data and serve it to a varying number of clients, all with constant caching and updating.

REST ties in to the oneM2M model because each entity can be modeled as resources when we want to interact with them: they have their
URI, and a **Resource Type**, which determines the semantics of the information in the resource.

### Properties of a Resource
Every resource in our server is going to have a unique URI which stems from the **base uri** or root.
Different resources can implement different HTTP request types.

Each Common Service Entity (connects Application and Network Entities) has a base CSE which serves as the root for all the resources
on that CSE.
Underneath the CSE there are several resources.
We can access the information from other CSEs and nodes on the network, as well as from other groups, manage subscriptions to resources, etc...
Some other common attributes include managing commands to execute on the CSE and other ways of communicating with other networks.

The Application Entity(AE) contains resources for subscriptions and buffering ''data'' between the AE and CSE.
Inside the container (common to the AE and CSE) is where the data for the entity is stored.

There are a couple of types of resources: **normal resources**, **virtual resources**, and **announced resources**.
Virtual resources are used to trigger resources and retrieve results, but don't have definite representation in the CSE.
Announces resources exist on some remote CSE
...

Subscriptions make resources notify other resources when some change happens. 
This avoids the need of constant polling the resource consantly to check for changes.

The Eclipse OM2M Platform is a platform that allows for management of all the oneM2M devices.
It is based on the JVM to implement all the different parts of the oneM2M hierarchy.
Teh platform has a FlexContainer resource where we can self-contain pieces of code, 
as well as other structures in its roadmap.

# Core technologies in IOT Networks
There are several domains in IOT applicaitons: the M2M domain where sensors talk to each other; a gatweway which connects the M2M network with the 
regular network; and the application network where developers can interact with the sensors through the network.
The network communication occurs between machines and each other or some server/gateway. 
However, a single machine's communications may occur not super frequently or require low bandwidth, etc...

However, different M2M communications have different characteristics, such as volume and QOS, time sensitivity and direction, etc...
Most applications use a mobile network since the cost of wiring could be too expensive, even if a sensor is not moving.
The core networks in IOT/M2M applications have to be low cost, have to be valueable in our network, and individually addressible.

## Low cost
There are a couple factors that drive the cost of the devices up: the number of group sybscriptions and simultaneously attached devices; a large number of
connections will be always on; there might be a large volume of data throughout the many data sessions.

For the network components, most of the factors in the cost involve the SIM cards, setup, and radio capacity/radius etc...

Methods for reducing the costs can include **group-based communications**, where devices have to have a subscription to operate on a network, polcing
for subscriptions, and triggering.
Idle devices that are connected to the network drag on the network by saving their context information, but removing them while idle could add to the 
reconnection cost when they start sending information again.

The second cost reduction method includes reducing the network signaling, which is how frequently we send data across the network.
For example, keep devices that constantly send data connected to the network and disconnect infrequent devices.
Another alternative is to avoid a spike during times of peak usage.
We can control how long a window  a device has to send data during times of peak usage.

The next cost reduction method involves separating the M2M communications into a separate network. 
We could separate both the **core networks** and the **access networks** for H2M and M2M comms into their own networks, or we could only separate 
core networks for M2M comms.

Requirements for value-added services: 
1. QoS and priority differentiation
	- There are different levels of QoS depending on the applicaiton, where more important applications require lower latency.
	- The "Allocation and Retention Priority", or **ARP**, determines how long the packet should be maintained by the network, and what level of priority the packet contains (1-15).
2. Charging and subscription management
	- Has to support flexible subscription time (e.g. EZ cards are activated only after they're bought and turned on).	
	- Flexible choice of mobile operators.
3. Device management
	- Activating M2M devices
	- Remote management of M2M devices
4. Connection monitoring
	- Ensure the connection is in good condition
	- Detect anomalies (sometimes using AI)
	- Reporting any issue to applications.
5. Fraud control
	- One device suddenly sends more data than usual
6. Secure connection
	- Encrypt connections


## IOT Core Technologies
M2M core networks consist  of the M2M area network(sensors), the M2M gateway which leads to the M2M core network (routers, satellites, antennas), and then
the data reaches the client applications.
The core network can use a wired or wireless approach to sending data.

There are different ways for the M2M components to communicate with each other:
- Machine to Machine
- Machine to Server
- Machine to Gateway to Server

Different machines communicate under different circumstances: some need to constantly update/send data, others do so rarely.
The type of data sent can also vary: video data from a camera takes more bandwidth than just temperature readings.
**Mobile networks are the best choice for IOT network connections**. Cabling to nested sensors, and the lack of mobility of wired
networks make mobile networks a better choice.
Mobile networks can also support global roaming for devices such as vehicles; however, we would need to ensure the network has good coverage.

For the core networks, there are a couple factors that drive up the cost for many M2M comms: group-based subscriptions, many simultaneous devices and connections,
the volume and type of data that passes through the network. 
As for the network components, having a SIM card in every device and having a large range to send data drives up the cost.
There are a couple ways we could reduce the cost: group based communications, reducing resource usage for idle devices, reducing the network signaling,
avoiding peaks in user data from the networks, and even having a separate network for M2M comms.

We can reduce the cost by charging for the communications of each group. 
However, each device belonging to more than one group can complicate things a bit.

When a device idles, it can save its session context until it comes online again. 
This prevents the load associated with disconnecting and reconnecting the device.

To reduce the network signaling of the devices, we can disconnect devices that don't often send data.
To prevent the network from peaks, network providers can offer better rates during times the network is not congested,
or other incentive to use the network at different times.
3GPP details how devices can be limited to use the network only at certain times.

The final cost reduction method is to have a separate network for M2M comms.
We could separate only the core network or both core and access networks for M2M and H2H comms.
If we don't use 5G, we could have another type of GSSN access network.
For 5G networks, we can use some form of time/frequency slicing.

Network providers need to handle groups and subscription management, as well as remote SIM management.
Fraud detection could also be considered important, this can be done by checking if one device transmits more than frequent, etc...

...

The LoRaWAN network is usually a **star-of-stars** topology in which all 
coms are bi-directional.
LoRaWAN cna support different types of bi-directional communication, such as 
only receiving communication, scheduled receive slots, and maximal recieve slots.

The first class of devices(class A)  requires the lowest power for devices that are on 
battery, occasional communication with low-powered devices.

The second types of devies use a **scheduled interval**, and this way we can
know how much energy to consume, at the expense of type A devices.

The final type of devices are ones that are constantly connected, can send
messages at any time. Class C devices have the lowest latency but consume the 
most power.

### Ingenu
This protocol was designed for low-power wide-area communications.
An Ingenu AP can provide a connection to all connected devices.
The AP in Ingenu acts as the gateway to the Network Server, cloud server and
eventually the customer/client devices.

### SIGFOX
This protocol was designed for low-throughput devices.
Devices can send up to 140 messages per day.
Because it is based on ultra narrow band, it can be **tolerant to resistance and jamming**.

The devices initiate the communication with the servers and has light HW requirements.

### 4G Core Network Architecture
The E-UTRAN Unity in 4G networks allows the different entities to connect to the 
larger network.

### 5G Network Architecture
The main difference between the 4G and 5G networks is that 5G is more oriented
to microservices.
The methods used to intereact with other resources include APIs, protocols like HTTP,
and managing core network functions such as virtualization and slicing. 

Some of the basic components of 5G architecture:
1. **AMF (Access and Mobility Management Function)**: AMF is the node
that manages all UE-related functions. All the access and mobility functionality has been moved to this node.
2. **SMF (Session Management Function)** : Establishes and takes care of sessions,
manages/allocates IP addresses.
3. **UPF (User Plane Function)**: Provides functions specific to user plane.
4. The **Unified Data Management** in the network stores and manages subscriber
information.
5. **AUSF Authentication Server Function** Authentication processing with an interface.
6. **PCF (Policy Charging Function)**: Sets policy that governs network behavior.
7. **NEF (Network Exposure Function))**: Allows devices to send data b/w networks w/o first establishing session.
8. **NSSF (Network Slice Selection Function)**: Selects the network slices that serve the User Entity(UE?)

### SDN/NFV in 5G
SDN separates the control and data plane, which allows programmability of network
functions rather than the "backend" logic being done in the same place as route selection.
Network Function Virtualization (NFV) enables the virtualization of hardware-based network appliances.
I guess this means you can have some virtualization directly on the devices that carry out the brunt of the work?

The routing table and other access control/load balancing issues are handled in the
control plane, and the information is set in the data plane.
Virtualization here allows for one physical device to operate as multiple virtual 
devices and appear as such to the control plane.

SDN aims to achieve :
1. Resource sharing -- allows multiple tenants on a certain network (e.g. telecoms sharing the same network?)
2. Network slicing: -- How to allocate the physical resources most efficiently?
3. Network programmability -- Easily allow new applications (thru changin routing table, etc...)

This makes the network appliances easier to deploy and manage.

For Network Function Virtualization, we can split a single physical hardware resource
into multiple software resources.
When we want to access a slice of the network, our device such as a phone
will contact the Access and Mobility Function to request 5G services.
The AMF will ask the Network Slice Selection Function to select a network slice.
The NSSF will query the NRF for the set of network functions required for the slice.
The request will then be forwarded to different Data Networks.

The main points of Network Slicing:
- A slice can consist of multiple slice subnets (parts of multiple subnets?)
- Network slice subset is supported by a set of 5G VNFs.
- Virtual Network Functions are managed by NFV MANO
- BSS/OSS tells NFV MANO when to create/terminate VNFs.

# Security
## Smart-card based solutions
Devices such as credit cards will have the necessary key information 
so that during use they can send their info to the M2M service layer.
This key is hard-wired by the manufacturer, so there is no sending
of the private key but the manufacturer has to be trusted.

However, this approach is not really scalable in cellular networks,
which can be run on billions of devices.
## Pre-provisioned symemtric keys
Here the keys are given to the m2m service provider and the device
at the factory.
This can be useful for ensuring authenticity during the initial setup.
Devices and the m2m service provider can use the pre-provisioned
symmetric key during initial authentication while they generate another key.

## Identity-Based encryption solutions
Here we use the **identity** to generate the public key as a math function
of the identity. 
Once we have the public key, we can use a **private key generator** to 
produce the corresponding private key.
The shared key is based on **elliptic curves**, widely used in cryptography.

Because it's the identity that's used to generate the keys, there is 
no need to have an entire infrastructure to issue the keys.

## Identity Based Authenticated Key Exchange (IBAKE)
This protocol is used when there is little trust b/w the parties.
1. The device uses a random number $x$ and a point on an elliptic curve $P$.
The device then calculates $xP$ and encrypts it with the identity based public key of the 
operator.

2. The operator receives the encrypted message and decrypts it with their own public key,
and gets $xP$. The operator then likewise chooses a random number $y$ and 
calcualtes $yP$. It sends a message back to the receiver with $xP$, $yP$ both 
encrypted with its IBE public key.

3. The device recieves the messgae and decrypts it with its IBE public key,
obtaining $xP, yP$. If $xP$ mathces the value sent at the beginning, 
we have now authenticated the operator. The device then encrypts $yP$
and sends it to the operator. If decrypted value matches $yP$ at the 
operator, the device is authenticated there as well.

OneM2M also has its own methods of authenticating AEs and CSEs.
The authentication here checks for the identity provided by the entity and
also checks if the entity has registered.

As part of the authorization process, the entity has some access control
policies. 
These policies are just the conditions that would allow an entity 
to access another resource.

There are six security functions defined in the oM2M spec:
1. Authentication and Identification: mutual authentication b/w AE, CSE.
1. Authorization: Use the access control policy to check if an entity
is auhtorized to access the specific resource. For a specific resource 
there might be multiple policies.
2. Identity Management: provides identifiers to the requesting entity.
Would these be the names that appear when creating an AE or CSE, etc...?
3. Security Association: Establish a secure association b/w two nodes.
4. Sensitive Data Handling: Have the security algorithms computed in a secure environment,
handle secrets and keys appropriately.
5. Security Administration: provide functions to manage the security functions,
attributes and resources on the entity.

Each stage has its own objective. 
The **Remote security Provisioning Frameworks** (RSPF) is a post-provisioning
**Security Association Establishments Framework**.
entity and the autentication function of an M2M service provider.
This authentication can be done during manufacturing or development phase,
or by a boostrapping procedure as soon as the object is activated and before it
starts its oepration.
The RSPF framework could be used in a couple of different scenarios.
It could use a pre-shared key on both devices, or a certificate-based 
approach where they have their keys issued.
Or, it could use a GBA bootstrap server to authenticate using it's keys.


