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

# Cybersecurity
