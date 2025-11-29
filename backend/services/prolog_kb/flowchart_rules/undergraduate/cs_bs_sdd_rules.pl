% Prolog KB for the CS-BS Software Design & Development (SDD) Track

:- multifile
       user:required/1,
       user:prerequisite/2,
       user:corequisite/2,
       user:one_of_prereqs_fact/2,
       user:elective/1.
:- dynamic
       user:required/1,
       user:prerequisite/2,
       user:corequisite/2,
       user:one_of_prereqs_fact/2,
       user:elective/1.


% — Required Core Courses (CS-BS SDD) —
user:required(cgs1920).    % Intro to Computing
user:required(cop2210).    % Programming I
user:required(cop3337).    % Programming II
user:required(cop3530).    % Data Structures
user:required(cop4338).    % Systems Programming
user:required(cop4610).    % Operating Systems
user:required(cda3102).    % Computer Architecture
user:required(cen4010).    % Software Engineering I
user:required(cen4021).    % Software Engineering II
user:required(cen4072).    % Software Testing
user:required(cen4083).    % Cloud Computing
user:required(cop4520).    % Intro to Parallel Computing
user:required(cop4604).    % Advanced UNIX Programming
user:required(cop4710).    % Database Management
user:required(cis3950).    % Capstone I
user:required(cis4951).    % Capstone II


% Basic course sequence
user:prerequisite(cop3337, cop2210).                  % Programming II needs Programming I
user:prerequisite(cop3530, cop3337).                  % Data Structures needs Programming II
user:prerequisite(cop4338, cop3530).                  % Systems Programming needs Data Structures
user:prerequisite(cop4610, cop4338).                  % Operating Systems needs Systems Programming
user:prerequisite(cop4610, cda3102).                  % and Computer Architecture
user:prerequisite(cen4010, cop3530).                  % Software Engineering I
user:prerequisite(cen4021, cen4010).                  % Software Engineering II
user:prerequisite(cen4072, cop3530).                  % Software Testing

% Math and logic foundations
user:prerequisite(mac2312, mac2311).                  % Calculus II needs Calculus I
user:prerequisite(mac2311, mac1147).                  % Calculus I needs Pre-Calculus
user:prerequisite(mad2104, mac1105).                  % Discrete Math
user:prerequisite(cot3100, mac1105).                  % Discrete Structures needs a MAC course
user:prerequisite(cot3100, cop1000).                  % Discrete Structures needs a COP course
user:corequisite(cot3100, cop2210).                   % and co-requires Programming I

% Electives: Foundations
user:prerequisite(cop4534, cop3530).                  % Algorithm Techniques
user:prerequisite(cot3541, cot3100).                  % Logic for CS
user:prerequisite(cot3541, cop3337).                  % Logic for CS
user:prerequisite(cot4521, cop3530).                  % Computational Geometry
user:prerequisite(mad3301, cop2210).                  % Graph Theory
user:one_of_prereqs_fact(mad3301, [cot3100, mad2104]).
user:prerequisite(mad3401, cop2210).                  % Numerical Analysis
user:prerequisite(mad3401, mac2312).
user:prerequisite(mad3512, cop3530).                  % Theory of Algorithms
user:prerequisite(mhf4302, mad3512).                  % Math Logic
user:prerequisite(mad4203, mad2104).                  % Combinatorics
user:prerequisite(mad4203, mac2312).
user:corequisite(cot3510, cot3100).                   % Applied Linear Structures
user:corequisite(cot3510, mad2104).

% Electives: Systems
user:prerequisite(cap4453, cop3530).                  % Robot Vision
user:prerequisite(cap4453, mac2312).
user:prerequisite(cda4625, cop3530).                  % Mobile Robotics
user:prerequisite(cda4625, sta3033).
user:prerequisite(cen4083, cnt4713).                  % Cloud Computing
user:prerequisite(cen4083, cda3102).
user:prerequisite(cop4520, cop3530).                  % Parallel Computing
user:one_of_prereqs_fact(cop4520, [cda3102, cda4101, eel4709]).
user:prerequisite(cot4431, cop3530).                  % Applied Parallel Computing
user:one_of_prereqs_fact(cot4431, [cda3102, cda4101, eel4709]).
user:prerequisite(cop4604, cop4610).                  % Advanced UNIX Programming
user:prerequisite(cop4710, cop3337).                  % Database Management
user:corequisite(cop4710, cop3530).
user:prerequisite(cop4751, cop4710).                  % Advanced DBMS
user:prerequisite(cts4408, cop4710).                  % Database Administration

% AI / Data / Graphics
user:prerequisite(cap4630, cop3530).                  % Artificial Intelligence
user:prerequisite(cap4641, cop3530).                  % NLP
user:prerequisite(cap4710, cop3337).                  % Computer Graphics
user:prerequisite(cap4710, mac2312).
user:prerequisite(cap4770, cop3530).                  % Data Mining
user:corequisite(cap4770, cop4710).
user:prerequisite(cap4612, cop3530).                  % Machine Learning
user:prerequisite(cap4612, sta3033).
user:prerequisite(cap4052, cap4104).                  % Game Design
user:prerequisite(cap4052, cop3530).
user:one_of_prereqs_fact(cap4052, [sta2023, sta3033]).
user:prerequisite(cap4830, cop3530).                  % Modeling and Simulation
user:one_of_prereqs_fact(cap4830, [sta2023, sta3033]).
user:prerequisite(cap4506, mac2312).                  % Game Theory

% Software and apps
user:prerequisite(cop4226, cop3530).                  % Advanced Windows Programming
user:prerequisite(cop4655, cap4104).                  % Mobile App Dev
user:prerequisite(cop4655, cen4010).

% Advanced topics
user:prerequisite(cot4601, cot3100).                  % Quantum Computing
user:one_of_prereqs_fact(cot4601, [cop3337, cop3804]).
user:prerequisite(cis4203, cop2210).                  % Digital Forensics
user:prerequisite(cis4731, cop3530).                  % Blockchain

% Capstone
% (Junior and Senior standing assumed)
user:prerequisite(cis4951, cis3950).                  % Capstone II needs Capstone I
