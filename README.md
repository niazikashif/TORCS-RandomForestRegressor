# TORCS-RandomForestRegressor
The project centers around the concept of simulating the car. The goal was to train a model so that the car drives autonomously in the game and ideally wins the race. Semester Project.


## Dataset Collection:
The dataset contains information about the surroundings from different sensors 
such as the acceleration of the car, the gear, the angle, the distance from the 
boundaries, fuel amount, the distance from opponents and opponent cars. The 
dataset is stored in a csv and is collected by playing the game multiple times with 
multiple laps on each map. I used 3 laps each map to collect more than 400k 
dataset stored in a csv file.

Link to the Dataset: https://drive.google.com/drive/folders/1cSbJOPggyu9oo5uviiAFfYPB-4OND4x5?usp=sharing

## AI Model:
The Model is built using Random Forest Regressor. It collects the dataset from the csv file 
and on the basis of different parameters it applies random forest distribution. It 
takes into account the acceleration, the gear, the brake and the steer values from 
the dataset to make decision tree and apply Random Forest Distribution.

## PSKL Files
Running the Python Notebooks will generate pskl files. The client will use these files to drive and race the car. These files are the trained model in action.

## Conclusion:
At the end, got the model to work, trained it using the extensive and clean 
dataset. The car is able to perform well on the maps, takes the turns and avoids 
going into the boundaries, centers the car and accelerates at a good rate with clean 
gear shifts



