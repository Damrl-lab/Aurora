% Prolog KB for CS-BA (Bachelor of Arts in Computer Science)

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

% — Required Core Courses —
user:required(mac1147).    % Pre-Calculus :contentReference[oaicite:58]{index=58}  
user:required(mac1105).    % College Algebra :contentReference[oaicite:59]{index=59}  
user:required(mgf1106).    % College Algebra alternative :contentReference[oaicite:60]{index=60}  
user:required(cot3100).    % Discrete Structures :contentReference[oaicite:61]{index=61}  
user:required(mad2104).    % Discrete Math :contentReference[oaicite:62]{index=62}  
user:required(cgs1920).    % Intro to Computing :contentReference[oaicite:63]{index=63}  
user:required(cop1000).    % Intro to Programming :contentReference[oaicite:64]{index=64}  
user:required(idc1000).    % CS for Everyone :contentReference[oaicite:65]{index=65}  
user:required(enc3249).    % Technical Writing :contentReference[oaicite:66]{index=66}  
user:required(enc3213).    % Technical Writing alternative :contentReference[oaicite:67]{index=67}  
user:required(cda3102).    % Computer Architecture :contentReference[oaicite:68]{index=68}  
user:required(cop2210).    % Programming I :contentReference[oaicite:69]{index=69}  
user:required(cop3337).    % Programming II :contentReference[oaicite:70]{index=70}  
user:required(cop3530).    % Data Structures :contentReference[oaicite:71]{index=71}  
user:required(cop4338).    % Systems Programming :contentReference[oaicite:72]{index=72}  
user:required(cen4010).    % Software Engineering I :contentReference[oaicite:73]{index=73}  
user:required(cen4021).    % Software Engineering II :contentReference[oaicite:74]{index=74}  
user:required(cgs3095).    % Technology in the Global Arena :contentReference[oaicite:75]{index=75}  
user:required(cop4610).    % Operating Systems :contentReference[oaicite:76]{index=76}  


% Basic course sequence
user:prerequisite(cop3337, cop2210).         % Programming II needs Programming I
user:prerequisite(cop3530, cop3337).         % Data Structures needs Programming II
user:prerequisite(cop4338, cop3530).         % Systems Programming needs Data Structures
user:prerequisite(cop4610, cop4338).
user:prerequisite(cop4610, cda3102).         % Operating Systems needs Systems Programming and Comp Arch
user:prerequisite(cen4010, cop3530).         % Software Engineering I
user:prerequisite(cap4104, cop3337).         % Human-Computer Interaction
user:prerequisite(cen4021, cen4010).         % Software Eng II needs SE I
user:prerequisite(cop4710, cop3337).
user:corequisite(cop4710, cop3530).          % DBMS needs Programming II, co-req with Data Structures
user:prerequisite(cop4751, cop4710).         % Adv DBMS
user:prerequisite(cts4408, cop4710).         % DB Admin
user:prerequisite(cop4555, cop3530).         % Programming Languages
user:prerequisite(cop4534, cop3530).         % Algorithm Techniques
user:prerequisite(cot3541, cot3100).
user:prerequisite(cot3541, cop3337).         % Logic for CS
user:prerequisite(cot4521, cop3530).         % Comp Geometry
user:prerequisite(mad3512, cop3530).         % Theory of Algorithms
user:prerequisite(mhf4302, mad3512).         % Math Logic
user:prerequisite(cnt4713, cop4338).         % Net Centric Computing
user:prerequisite(cen4083, cnt4713).
user:prerequisite(cen4083, cda3102).         % Cloud Computing
user:prerequisite(cop4520, cop3530).
user:one_of_prereqs_fact(cop4520, [cda3102, cda4101, eel4709]).
user:prerequisite(cot4431, cop3530).
user:one_of_prereqs_fact(cot4431, [cda3102, cda4101, eel4709]). % Applied Parallel Comp

user:prerequisite(cis4731, cop3530).         % Blockchain
user:prerequisite(cap4630, cop3530).         % AI
user:prerequisite(cap4641, cop3530).         % NLP
user:prerequisite(cap4770, cop3530).
user:corequisite(cap4770, cop4710).          % Data Mining
user:prerequisite(cap4052, cap4104).
user:prerequisite(cap4052, cop3530).
user:one_of_prereqs_fact(cap4052, [sta2023, sta3033]). % Game Design

% Math and discrete foundations
user:one_of_prereqs_fact(mad2104, [mac1105, mgf1106]).
user:prerequisite(cot3100, mac1105).         % Any MAC course (approximation)
user:prerequisite(cot3100, cop1000).         % Any COP course (approximation)
user:corequisite(cot3100, cop2210).

% Additional
user:prerequisite(cot4601, cot3100).
user:one_of_prereqs_fact(cot4601, [cop3337, cop3804]).
user:prerequisite(cis4203, cop2210).         % Digital Forensics

