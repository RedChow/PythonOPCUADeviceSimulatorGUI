# How To Run
After all the required packages have been installed, type 
```python
python mainwindow.py
```
or
```python
python3 mainwindow.py
```
in your favorite terminal. 
# Quick Introduction
The default starting address is opc.tcp://0.0.0.0:4840. This can be easily changed by
typing a new address in the Server Address line. The program will not let you add
any devices until the server has been started.
![Main Window](images/mainwindow.png)

Click "Start Server" to start the OPC UA server.
The "Server Status" will change from "Not Running" to "Running" if the server has been
stared successfully.
![Main Window Server Started](images/mainwindow_server_started.png)

You can add devices by using the "File" menu item at the top and then selecting "Add
Directory" or "Add File." See the "Device XML Structure" if you'd like
to try to make your own from scratch. There is also "test_file_2.xml" in the
devices_and_timers folder as an example.

If you have successfully imported files, you should see the devices listed in the
tree on the left hand side.
![Device have been added](images/device_tree_expanded.png)


If you have added the server to your Ignition Gateway, you can see it listed in 
the OPC browser.
![OPC Browser](images/home_automation.png)

You can drag and drop the items into your tags folder
![Tag Browser](images/home_automation_3.png)

# Functions
The following functions can be used to simulate values.

## ValueList
This function takes a list of values and then iterates through the list in order.
The function can iterate through a set number of times or indefinitely.
### Example
[1, 3, 2, 4, 6], Period = 3, Repeat = False: This would cause the variable to take 
on the values 1, 3, 2, 4, 6, 1, 3, 2, 4, 6, 1, 3, 2, 4, 6 and then stop on 6. 
Having Repeat=True discards any value period

## WeightedList

## RampStep

## RampPeriodic

## Square

## RandomSquare

## Triangle

## Sin

## Cos
# Device XML Structure



## Disclaimer
This still needs a lot of work. The GUI is operational and allows for adding/deleting 
devices. Being able to edit devices and such still needs some work.