% Prolog KB rules for the Bachelor of Science in Data Science and AI (DS-BS)

:- multifile user:required/1,
              user:prerequisite/2,
              user:corequisite/2,
              user:one_of_prereqs_fact/2,
              user:elective/1.
:- dynamic   user:required/1,
              user:prerequisite/2,
              user:corequisite/2,
              user:one_of_prereqs_fact/2,
              user:elective/1.

% — DS-BS Required Core Courses — 
user:required(cts1500).    % Emerging Topics in Digital Life
user:required(cgs3095).    % Technology in the Global Arena
user:required(cop2047).    % Python Programming I
user:required(cap2757).    % Introduction to Data Science
user:required(mac2312).    % Calculus II
user:required(mad2104).    % Discrete Math
user:required(cot3100).    % Discrete Structures
user:required(cop3045).    % Python Programming II
user:required(cop3465).    % Data Structures for IT
user:required(cap3764).    % Advanced Data Science
user:required(cap4612).    % Introduction to Machine Learning
user:required(cis3950).    % Capstone I
user:required(cis4951).    % Capstone II

% ==== Core Sequence ====
prerequisite(mac2312, mac2311).                     % Calc II ← Calc I
prerequisite(mac2311, mac1147).                     % Calc I ← Precalc
prerequisite(mad2104, mac1105).                     % Discrete Math ← College Algebra
prerequisite(cot3100, mac1105).                     % Discrete Structures ← any MAC
corequisite(cot3100, cop2047).                      % Coreq with Python I
prerequisite(cop3045, cop2047).                     % Python II ← Python I
prerequisite(cop3465, cop3045).                     % Data Structures ← Python II
prerequisite(cap3764, cap2757).                     % Adv Data Science ← Intro to DS
prerequisite(cap4612, cop3465).                     % ML ← Data Structures
prerequisite(cap4612, sta2023).                     % ML ← Stats
prerequisite(cis4951, cis3950).                     % Capstone II ← Capstone I

% ==== Elective Prerequisites ====
prerequisite(cap4630, cop3465).                     % AI ← Data Structures
prerequisite(cap4453, cop3465).                     % Robot Vision ← Data Structures
prerequisite(cap4453, mac2312).                     % and Calc II
prerequisite(cap4641, cop3465).                     % NLP ← Data Structures
prerequisite(cda4625, cop3465).                     % Mobile Robotics ← Data Structures
prerequisite(cda4625, sta2023).                     % and Stats
prerequisite(cap4506, mac2312).                     % Game Theory ← Calc II
prerequisite(cap4770, cop3465).                     % Data Mining ← Data Structures
corequisite(cap4770, cap3764).                      % co-req with Adv DS

prerequisite(cap4830, cop3465).                     % Modeling & Simulations
one_of_prereqs_fact(cap4830, [sta2023, sta3163]).
prerequisite(mad3401, cop3465).                     % Numerical Analysis
prerequisite(mad3401, mac2312).                     % and Calc II
prerequisite(sta4234, sta3163).                     % Regression ← Stat Methods I
prerequisite(mad3301, cop3410).                     % Graph Theory ← Comp Thinking
one_of_prereqs_fact(mad3301, [cot3100, mad2104]).
prerequisite(sta3164, sta3163).                     % Stat Methods II ← I

prerequisite(cen4083, cnt4713).                     % Cloud Computing ← Net-centric
prerequisite(cen4083, cot3100).
prerequisite(cop4534, cop3465).                     % Algorithm Techniques
prerequisite(cot4431, cop3465).                     % Applied Parallel Comp ← DS
prerequisite(cop4703, cop3465).                     % Info Storage ← DS

% ==== General Rules ====
prerequisite(enc3213, ucc_english).
prerequisite(enc3249, ucc_english).
