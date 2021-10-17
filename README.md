# Analysis of Short Duration Sprints to Evaluate Endurance of Athletes for Longer Runs

## Introduction
The movement of various muscles and joints in continuous synchronization across the body is extremely essential when it comes to successful sprint over long distances. Understanding of biomechanical factors in sprint running is useful because of their critical value to performance. At the beginning of the sprint run, it is important to produce great force/ power and generate high velocity in the block and acceleration phases. During the constant-speed phase, the events immediately before and during the braking phase are important in increasing explosive force/power and efficiency of movement in the propulsion phase. All of the aforementioned factors can be easily analysedusing the various joints and muscle movements across the body of the athelete.

## Background
There are various atheletic events across the country which offer participation to atheletes who have no prior experience to sports. Apart from recreation, such events are also organized as a part of long and elaborate physical examinations for recruitments under various security and defense personnel profiles. A majority of such athletes have no idea on how to appear for long sprints, and hence are unable to complete the tasks. The situation worsens when this is accompanied by physical ill-effects of the same. The issues range from mild-concussions to ligament tear, life-long handicap and sometimes even death. 

The following news articles confirms such happenings accross the country at a regular basis:
 * https://archive.siasat.com/news/youth-dies-punjab-police-recruitment-drive-1028554/
 * https://www.thehindu.com/news/cities/Madurai/youth-dies-while-taking-endurance-test-during-police-constable-recruitment/article35543878.ece
 * https://timesofindia.indiatimes.com/city/agra/constable-dies-15-others-faint-during-police-recruitment-physical-tests-in-aligarh/articleshow/64898160.cms


## Data Format
The target of the project is to design and create a solution that can evaluate the sprinting capacity of an individual in a short period of time and can be done without attaching any extra equipments (like ECG monitors) to the body. 

For achieving the same, video formats of small sprints from individuals could be really effective. Hence, short duration videos of atheletes from various angles and profiles could help in providing useful information regarding his/her endurance for long distance running 

## Methodology
The methodology for the project is explained as follows:
* Atheletes record short duration videos of them sprinting over a treadmill, recording 5-10 complete cycles of run
* The video is divided into various still frames for analysis
* Each still frame is taken into consideration, one-by-one and a pose detection algorithm is run on it
* The pose detection algorithm finds the various joints of the body as landmarks and returns their locations as X and Y Coordinates

<img src="https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/pose_tracking_full_body_landmarks.png" alt="Landmarks Across the Body" width="600px" />

<img src="https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/PoseDetection.jpg" alt="Detected Landmarks" width="300px" />

* Using three consecutive joints as points and cosine rule as a mathematical tool, the angle formed by the middle joint is represented (Right Shoulder, Right Elbow, Right Wrist gives the angle formed at the Right Elbow)

![Angle formed at a Joint](https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/JointAngle.jpg)


* These angles are continuously recorded with time and its values are recorded
* Smoothening functions are utilized to smoothen any noise found in the angles obtained

<img src="https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/GraphSmoothening.png" alt="Graph Smoothening" width="500px" />

* The resulting data is then superimposed with the data of trained atheletes to the the offset

<img src="https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/LiveRunning.png" alt="LiveRunning" width="500px" />

* If the offset is within the given threshold, the athelete is good for the run, otherwise he/she is disqualified for the long run

## Inferences
The data obtained after successful analysis for various joints and muscles across the body yields enough evidence to make a calculated estimate as to where the athelete is fit or not for a particular run. 

![Joint Analysis](https://github.com/adityakumar2809/SprintAnalysis/blob/master/info/Result.png)

It involves no physical connection to the body and there is no time required to set it up, hence can be easily configured, even at a remote location. All this can ease the process of screening extremely easy for the physically challenging events people are willing to participate in  
