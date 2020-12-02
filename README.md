# Mini_CPS Project
## Little DIY Project that includes some Cyber-Physical-System's design features.

This project represents an order and production system. It has been built with an Arduino, some led and sensors, and a Raspberry Pi, representing 3 systems interacting with each other.

The first component of this system is the Raspberry PI; it simulates some application, either web or implemented in a local company, that collects orders from clients. When it receives a new order, it checks if the Arduino is busy and then notifies it to start the development process of the ordered product.

The Arduino communicates with a simple circuit on a breadboard, on which there are 3 groups of led + sensor. Each one represents a stage of a production line, in which there could be ideally some robot that produces some component. Each component is represented by the data that is collected by the sensors. The Arduino proceeds in steps, notifying the start and stop to each stage and collecting data from it sequentially. We can see the actual stage by looking at the led blinking. When the process is finished the Arduino feeds the Raspberry PI with the collected data which then closes the order.

### Robustness and recoverability as CPS design feature

**What does it happen if some component fails**, for example one of the three production stages? In that case the Raspberry uses old history data, written for example in one file on the device’s disk. This solution can be suitable also when the Arduino fails, in that case the Raspberry could just close the order with old data.

This solution is robust in the production system because if one sensor fails, the Arduino just ignores that stage and goes to the next. 

An other issue of this system is that the single point of failure is the Raspberry. In this case a possible solution could be to integrate another component that represents a webserver or just a backup system with a database, to solve the orders in case of raspberry’s failure.

### Hardware components used

*Arduino*

- 3 Lights, representing each production step and the idle state 
- 1 Temperature sensor
- 1 LDR Sensor
- 1 Button

*Raspberry*

- Gets the orders
- Checks if the Arduino is busy, keeping a queue for orders
- When triggered by the Arduino, it collects the data from it, stores it on the disk and closes the order with the data.

To set up the Raspberry an USB-TTL adapter was used to communicate with its UART port. 

### Sketch of the breadboard

<img src="\Arduino\fritzing_sketch.png" alt="fritzing_sketch"  />