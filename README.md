# Robot-Motion-Planning
In this project, Bug2 algorithm is implemented on an omnidirectional robot using Python and in "Webots" simulation environment. the robot uses sonar and infrared sensors, GPS, camera, and deep learning algorithms to detect obstacles and its predefined destination.

## Preview
In these videos you can see how the robot will move toward the destination point in each algorithm:

<img src="https://github.com/MRSadeghi78/Robotics-Final-Project/blob/main/demo%20%231.gif" width="820">
<br>
<br>
<img src="https://github.com/MRSadeghi78/Robotics-Final-Project/blob/main/demo%20%232.gif" width="820">

## Algorithms
You can see the main idea of Bug2 algorithm and the state machine we designed for it in the following diagrams:

<img src="Bug2 algorithm.png" alt="drawing" width="600">
<br>
<br>
<img src="state-machine.jpg" alt="drawing" width="600">

## Image Recognition
For image recognition, a deep learning model was used. The implementation of this model can be found [here](https://colab.research.google.com/drive/1e-FfjJRSnnYn3Q8n4U6HS3wuCNbMYNPr?usp=sharing)

## How to run the simulation
Open the world file (worlds/current.wbt) in [Webots](https://cyberbotics.com/).

