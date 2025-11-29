% Prolog rule set for the Bachelor of Arts in Information Technology (IT-BA)

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

user:required(cop2250).   % Programming in Java
user:required(cot3100).   % Discrete Structures
user:required(cen3721).   % Human-Computer Interaction

% === Core Sequence ===
user:prerequisite(mad1100, mac1105).                         % Math Concepts for IT ← College Algebra
user:prerequisite(cot3100, mac1105).                         % Discrete Structures ← any MAC
user:prerequisite(cot3100, cop2250).                         % Discrete Structures ← any COP
user:corequisite(cot3100, cop2250).                          % Corequisite allowed: Programming in Java
user:prerequisite(cop3804, cop2250).                         % Intermediate Java ← Programming in Java
user:prerequisite(cen3721, cop3804).                         % Human-Computer Interaction ← Intermediate Java
user:prerequisite(cgs4285, cgs3767).                         % Networking ← Operating Systems

% === Intermediate Core Courses ===
user:prerequisite(cop4703, cop3804).                         % Information Storage ← Intermediate Java
user:prerequisite(cgs4854, cgs2100).                         % Website Management ← Microcomputers for Business
user:prerequisite(cgs2100, cgs2060).                         % Microcomputers for Business ← Intro to Microcomputers

% === IT Cognate Electives ===
user:prerequisite(cnt4403, cop3804).                         % Network Security ← Intermediate Java
user:corequisite(cnt4403, cgs4285).                          % Network Security co-req: Networking

user:prerequisite(cnt4513, cop3804).                         % Data Communication ← Intermediate Java
user:prerequisite(cnt4513, cgs4285).                         % Data Communication ← Networking
user:prerequisite(cnt4504, cnt4513).                         % Advanced Network Mgmt ← Data Communication

user:prerequisite(cnt4182, cnt4403).                         % Mobile & IoT Security ← Network Security
user:prerequisite(cnt4603, cgs3767).                         % Windows Admin ← Operating Systems

user:prerequisite(cis4365, cnt4403).                         % Enterprise Cybersecurity ← Network Security

user:prerequisite(cis4431, cgs4285).                         % IT Automation ← Networking (co-req)

user:prerequisite(cop4005, cen3721).                         % Windows Programming ← HCI
user:one_of_prereqs_fact(cop4005, [cop3804, cop3337]).
user:corequisite(cop4005, cop4703).                          % co-req: Info Storage

user:prerequisite(cop4751, cop4703).                         % Advanced DBMS ← Info Storage
user:prerequisite(ctr4348, cgs3767).                         % Unix Admin ← Operating Systems
user:prerequisite(cts4408, cop4703).                         % DB Admin ← Info Storage
user:prerequisite(cop4813, cgs4854).                         % Web App Programming ← Website Mgmt
user:prerequisite(cop4814, cop4703).                         % Component Based SW ← Info Storage
user:prerequisite(cop4814, cgs4854).                         % and Website Mgmt
user:prerequisite(cts4743, cop4703).                         % IT Troubleshooting ← Info Storage
user:one_of_prereqs_fact(cts4743, [cnt4403, eel4806]).            % and (Network Security or EEL4806)

% === App Dev Path ===
user:prerequisite(cop4655, cen3721).                         % Mobile App Dev ← HCI
user:prerequisite(cop4655, cop4814).                         % and Component-Based Dev
% OR
user:prerequisite(cop4655, cap4104).                         % Mobile App Dev ← HCI
user:prerequisite(cop4655, cen4010).                         % and Software Eng I

% === Quantum &
