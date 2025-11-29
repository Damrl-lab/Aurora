% Prolog KB for IT-BS (Bachelor of Science in Information Technology)

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

% — Required Core Courses for IT-BS (Fall 2023 flowchart) —
user:required(mac1105).  % College Algebra
user:required(mac1147).  % Pre-Calculus
user:required(mad1100).  % Math Concepts for IT
user:required(cop2250).  % Programming in Java
user:required(cgs1920).  % Intro to Computing
user:required(cot3100).  % Discrete Structures
user:required(cop3804).  % Intermediate Java
user:required(cen3721).  % Human-Computer Interaction
user:required(cgs2060).  % Intro to Microcomputers
user:required(cgs2100).  % Microcomputers for Business
user:required(cgs4854).  % Website Management
user:required(cgs3767).  % Operating Systems
user:required(cgs4285).  % Applied Networking
user:required(cnt4403).  % Computing & Network Security
user:required(cnt4513).  % Data Communication
user:required(cnt4504).  % Advanced Network Management
user:required(cis4950).  % Capstone I
user:required(cis4951).  % Capstone II
user:required(cop4703).  % Information Storage & Retrieval
user:required(cts4408).  % Database Administration
user:required(cop4005).  % Windows Programming for IT
user:required(cop4655).  % Mobile App Development
user:required(cop4813).  % Web App Programming
user:required(cop4814).  % Component-Based Software Dev
user:required(cts4348).  % Unix System Administration
user:required(cnt4603).  % Windows System Administration
user:required(cis4365).  % Enterprise Cybersecurity

% === Math and Foundations ===
prerequisite(mac1147, mac1105).                       % Pre-Calc ← College Algebra
prerequisite(mad1100, mac1105).                       % Math Concepts for IT ← College Algebra
prerequisite(cot3100, mac1147).                       % Discrete Structures ← Pre-Calc (assumed via any MAC)
corequisite(cot3100, cop2250).                        % Discrete Structures coreq with Java

% === Programming and Systems Core ===
prerequisite(cop3804, cop2250).                       % Intermediate Java ← Intro Java
prerequisite(cen3721, cop3804).                       % HCI ← Intermediate Java
prerequisite(cop4703, cop3804).                       % Info Storage ← Intermediate Java
prerequisite(cgs2100, cgs2060).                       % Microcomputers for Business ← Intro Microcomputers
prerequisite(cgs4854, cgs2100).                       % Website Management ← Microcomputers for Business

% === Capstone Series ===
prerequisite(cis4951, cis3950).                       % Capstone II ← Capstone I

% === Application Development Electives ===
prerequisite(cop4751, cop4703).                       % Adv DBMS ← Info Storage
prerequisite(cts4408, cop4703).                       % DB Admin ← Info Storage
prerequisite(cop4814, cop4703).                       % Component-Based Dev
prerequisite(cop4814, cgs4854).                       % and Website Management
prerequisite(cop4813, cgs4854).                       % Web App Programming ← Website Management

prerequisite(cop4005, cen3721).                       % Windows Programming ← HCI
one_of_prereqs_fact(cop4005, [cop3804, cop3337]).
corequisite(cop4005, cop4703).                        % co-req: Info Storage

prerequisite(cop4655, cen3721).                       % Mobile App Dev ← HCI
prerequisite(cop4655, cop4814).                       % and Component-Based Dev
% OR
prerequisite(cop4655, cap4104).                       % Mobile App Dev ← HCI alt path
prerequisite(cop4655, cen4010).                       % and Software Eng I

% === Systems & Networking Electives ===
prerequisite(cgs4285, cgs3767).                       % Networking ← Operating Systems
prerequisite(cnt4403, cop3804).                       % Network Security ← Intermediate Java
corequisite(cnt4403, cgs4285).                        % co-req: Networking
prerequisite(cnt4513, cop3804).                       % Data Comm ← Intermediate Java
prerequisite(cnt4513, cgs4285).                       % and Networking
prerequisite(cnt4504, cnt4513).                       % Advanced Network Mgmt ← Data Comm
prerequisite(cnt4182, cnt4403).                       % Mobile & IoT Security ← Network Security
prerequisite(cis4365, cnt4403).                       % Enterprise Cybersecurity ← Network Security
prerequisite(cis4431, cgs4285).                       % IT Automation ← Networking (co-req)
prerequisite(cnt4603, cgs3767).                       % Windows Admin ← Operating Systems
prerequisite(cts4348, cgs3767).                       % Unix Admin ← Operating Systems
prerequisite(cts4743, cop4703).                       % IT Troubleshooting ← Info Storage
one_of_prereqs_fact(cts4743, [cnt4403, eel4806]).

% === Advanced Computing & Security ===
prerequisite(cot4601, cot3100).                       % Quantum Computing ← Discrete Structures
one_of_prereqs_fact(cot4601, [cop3804, cop3337]).
prerequisite(cis4203, cop2210).                       % Digital Forensics
