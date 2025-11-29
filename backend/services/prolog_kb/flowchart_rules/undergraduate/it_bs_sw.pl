% Prolog KB for the IT-BS Software Track


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
              
user:required(mac1147).      % Pre-Calculus 
user:required(mac1105).      % College Algebra 
user:required(mad1100).      % Math Concepts for IT 
user:required(cop2250).      % Programming in Java 
user:required(cop3804).      % Intermediate Java 
user:required(cot3100).      % Discrete Structures 
user:required(cen3721).      % HCI
user:required(cop4703).      % Info Storage & Retrieval 
user:required(cgs2060).      % Intro to Microcomputers 
user:required(cgs2100).      % Microcomputers for Business 
user:required(cgs3767).      % Operating Systems 
user:required(cgs4285).      % Applied Networking 
user:required(cgs4854).      % Website Management 
user:required(cnt4403).      % Network Security 

% === Math and Foundations ===
prerequisite(mac1147, mac1105).                       % Pre-Calc ← College Algebra
prerequisite(mad2104, mac1105).                       % Discrete Math ← College Algebra
prerequisite(cot3100, mac1147).                       % Discrete Structures ← Pre-Calc (via MAC)
corequisite(cot3100, cop2210).                        % Discrete Structures ← co-req with Programming I

% === Programming Sequence ===
prerequisite(cop3337, cop2210).                       % Programming II ← Programming I
prerequisite(cop3530, cop3337).                       % Data Structures ← Programming II
prerequisite(cop4338, cop3530).                       % Systems Programming ← Data Structures

% === HCI & Systems ===
prerequisite(cen3721, cop3337).                       % HCI ← Programming II
prerequisite(cgs2100, cgs2060).                       % Micro for Business ← Intro Microcomputers
prerequisite(cgs4854, cgs2100).                       % Website Mgmt ← Micro for Business
prerequisite(cop4703, cop3337).                       % Info Storage ← Programming II

% === Capstone ===
prerequisite(cis4951, cis3950).                       % Capstone II ← Capstone I

% === Application Dev Electives ===
prerequisite(cop4751, cop4703).                       % Adv DBMS ← Info Storage
prerequisite(cts4408, cop4703).                       % DB Admin ← Info Storage
prerequisite(cop4814, cop4703).                       % Component-Based Dev
prerequisite(cop4814, cgs4854).                       % and Website Management
prerequisite(cop4813, cgs4854).                       % Web App Programming ← Website Management

prerequisite(cop4005, cen3721).                       % Windows Programming ← HCI
one_of_prereqs_fact(cop4005, [cop3804, cop3337]).          % ← Intermediate Java or Programming II
corequisite(cop4005, cop4703).                        % co-req: Info Storage

prerequisite(cop4655, cen3721).                       % Mobile App Dev ← HCI
prerequisite(cop4655, cop4814).                       % and Component-Based Dev
% OR
prerequisite(cop4655, cap4104).                       % Mobile App Dev ← HCI alt
prerequisite(cop4655, cen4010).                       % and Software Eng I

% === Security & Advanced Topics ===
prerequisite(cnt4403, cop3337).                       % Network Security ← Programming II
prerequisite(cnt4182, cnt4403).                       % Mobile & IoT Security ← Network Security
prerequisite(cot4601, cot3100).                       % Quantum Computing ← Discrete Structures
one_of_prereqs_fact(cot4601, [cop3337, cop3804]).
