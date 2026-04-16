Update 1: 
  timings 8:00AM to 9:00AM
 
  Discussed and Analysed all the extra requirements by reviewing the responces and survey by the StackHolders.
  Searched for the ways to design the schemetic of the circuit considering the limittion of the components on few IDEs/Platforms.

Member : Mihir and Gouri
Role : Discussion and Analysis of extra requirements

Member : Gouri 
Role : Documentation of the discussion looked for the schemetics IDEs.

Member : Mihir
Role : Creating the git repository and looked for the schemetics IDEs.

Update 2: 
Timing 9:00AM TO 10:00AM

Discussed the components according to the requirements. Downloaded the datasheets and reviewed it parrallely making the documentation noting the key parameters from the sheet.
 
 Member : Mihir 
 Reviewed Arduino Uno R4 Wifi datasheet. Link : https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf

 Member : Gouri 
 Reviewed MQ6 sensor datasheet. Link : http://www.handsontec.com/dataspecs/sensor/MQ6-LPG%20Sensor%20Module.pdf

 Member : Mihir And Gouri
 Documentation of the review on shared Google Doc. Link : https://docs.google.com/document/d/1aDvrpwIOXgHMgOs-GuqKawZm_Hea75zWhsju9SYhX9U/edit?tab=t.kmdql8rlme5y
 Discussed and shared the key points from each other's review.

Update 3: 
Timing 10:AM TO 11:00AM

Reviewed the rest of the datasheet of the remaining component

Member : Mihir 
Reviewed 2/2 & 3/2 WAY DIRECT ACTING
SOLENOID VALVE (NC / NO). Link : https://www.uflowvalve.com/Assets/Product/Catalogue/solenoid-valve/series/uflow_dac_series_catalogue.pdf

Member : Gouri 
Reviewed AS608 Finger print Sensor. Link : https://handsontec.com/dataspecs/sensor/AS608%20Finger%20print%20Sensor.pdf

Member : Mihir And Gouri
 Documentation of the review on shared Google Doc. Link : https://docs.google.com/document/d/1aDvrpwIOXgHMgOs-GuqKawZm_Hea75zWhsju9SYhX9U/edit?tab=t.kmdql8rlme5y
 Discussed and shared the key points from each other's review.

Update 4: 
Timing 11:00AM to 12:00PM
Mihir and Gouri

Designing of Circuit on paper and Schematic Diagram on EasyEDA Platform on a shared Workspace connecting all the components and Downloaded BOM(Bill of Materials).

Update 5:
Timing 12:00PM to 1:00PM
Mihir and Gouri

We have completed the simulation of our system design, integrating all required components and verifying the circuit connections. Further testing and refinements are currently in progress.

Update 6:
Timing 1:00PM to 2:00PM
Mihir and Gouri

We updated the simulator setup and made some changes to the circuit connections and code to improve the system’s functionality.

Update 7:
Timing 2:00PM to 4:00PM
Mihir and Gouri

We have Designed pcb of arduino shied according to our needs.

Update 8:
Timing 4:00PM to 6:00PM
Mihir and Gouri

- We have completed the hardware setup using an Arduino-based controller with an MQ6 gas sensor for gas concentration monitoring.

- We successfully connected the device to WiFi, enabling it to send sensor readings to a cloud database.

- We integrated the system with Firebase, which now stores real-time data from multiple devices.

- We developed a web dashboard using Python that retrieves and displays sensor readings from the cloud database.

- The platform now supports multiple users and multiple devices.

- An admin interface allows us to create new users and assign devices to them.

- Users can log in and view live sensor readings from their assigned devices.

- The dashboard also includes real-time graph visualization for monitoring gas level trends.




**DAY 2**


Update (7:15 - 9:20)
Member Mihir : Updated the dashboard ui and added featues such as monitoring all the devices for admin.
Made the changes in Firebase database for more security.

Update (7:15 - 9:20)
Member Mihir : Updated the dashboard ui and added featues such as monitoring all the devices for admin.
Made the changes in Firebase database for more security.

Member Gouri : Tested the changed UI for user level dashboard. Integrating the fingerprint sensor and reviewing its connection and datastorage videos from YT.


Update (9:15 – 11:15)
Team Members: Mihir, Gouri

Successfully integrated the fingerprint sensor, MQ-6 gas sensor, buzzer, and LED. The system is designed such that when an unauthorized user attempts access, an immediate alert is triggered through the buzzer and LED indication, ensuring quick detection of intrusion attempts. Additionally, fingerprint authentication data along with user credentials was securely stored and managed using Firebase, enabling reliable user identification and centralized data handling.


Update (11:15 – 1:15)
Members: Mihir, Gouri

Refined and optimized the Arduino code to improve system performance and reliability. Implemented unique pairing between device ID and fingerprint ID, ensuring accurate identification and preventing conflicts between multiple users or devices.
Enhanced the buzzer alert logic to provide clearer and more consistent responses during unauthorized access attempts. Additionally, restructured Firebase attributes to improve data organization, strengthen security, and enable more efficient credential management.
The UI was also updated to provide a cleaner and more intuitive interaction experience.

Marathon Day-2
Update (1:15 - 3:15)
Members: Mihir and Gouri

Initially, the schematic included only the MQ-6 gas sensor interfaced with the microcontroller. In this work session, the design was expanded by incorporating the fingerprint sensor, LED, and buzzer to improve system functionality. Circuit errors were identified and corrected, and pin mappings were refined to ensure proper communication between all components. The updated schematic now reflects a more complete and reliable system architecture.

<img width="1071" height="701" alt="image" src="https://github.com/user-attachments/assets/fa6f4a76-1722-4229-a946-d332ee8f80b0" />


Marathon Day - 2
Update (3:15 - 5:15)
Members: Gouri and Mihir

Designed and finalized the PCB layout by integrating the microcontroller with MQ-6 gas sensor interface, fingerprint module header, relay control header, buzzer, and LED indicators. Resolved multiple schematic-to-PCB conversion issues such as footprint mismatches, floating pins, and incorrect net mappings, ensuring proper connectivity and power distribution across all components. Optimized component placement and routing to achieve a clean, compact, and manufacturable layout. Verified the design using both 2D and 3D PCB views, confirming correct alignment and practical feasibility for hardware implementation.

**PCB DESIGN**
<img width="1450" height="742" alt="image" src="https://github.com/user-attachments/assets/b793626a-2698-4e47-838a-da62ae54c481" />

<img width="931" height="603" alt="image" src="https://github.com/user-attachments/assets/4f7789aa-f111-4569-9ae0-674eb34c1852" />

Marathon Day - 2 (7:15 am - 7:15 pm done)
Update (5:15 - 7:15)
Members: Mihir and Gouri

Updated the Arduino Uno code to support dynamic fingerprint registration, enabling each fingerprint ID to be securely mapped and stored in Firebase according to its respective device ID. Implemented corresponding modifications in the user dashboard to reflect real-time authentication status, valve control state, and gas sensor readings. Added new features for live monitoring, including continuous data updates, improved visualization of gas concentration trends, and synchronized device-level access control, enhancing overall system responsiveness and usability.


**ADMIN DASHBOARD**

<img width="1499" height="913" alt="image" src="https://github.com/user-attachments/assets/8ce1fc85-6b70-4d6d-b504-68d292ccedde" />

<img width="1505" height="885" alt="image" src="https://github.com/user-attachments/assets/82ae507d-9c83-40da-ade5-90cd424dfbc5" />


