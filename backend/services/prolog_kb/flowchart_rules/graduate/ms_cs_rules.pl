% ms_cs_rules.pl
% Prolog KB for the M.S. in Computer Science (effective Fall 2019)

:- multifile
    user:required/1,
    user:elective/1,
    user:minimum_grade/2,
    user:minimum_gpa/1,
    user:non_thesis_track/1,
    user:thesis_track/2,
    user:max_independent_study/1,
    user:max_non_scis_electives/1.
:- dynamic
    user:required/1,
    user:elective/1,
    user:minimum_grade/2,
    user:minimum_gpa/1,
    user:non_thesis_track/1,
    user:thesis_track/2,
    user:max_independent_study/1,
    user:max_non_scis_electives/1.

% — Required Core Course —
user:required(cot5407).    % COT 5407: Introduction to Algorithms

% — Required Core‐Elective Options (choose any 2 of 3) —
user:elective(cen5011).    % CEN 5011: Advanced Software Engineering
user:elective(cop5614).    % COP 5614: Operating Systems
user:elective(cop5725).    % COP 5725: Principles of DBMS

% — Grade & GPA Constraints —
user:minimum_grade(cot5407, b).
user:minimum_grade(cen5011, b).
user:minimum_grade(cop5614, b).
user:minimum_grade(cop5725, b).
user:minimum_gpa(3.0).

% — Degree‐track options —
user:non_thesis_track(elective_credits(21)).                        
user:thesis_track(elective_credits(15), thesis_credits(6)).        

% — Credit limits —
user:max_independent_study(3).      % CIS 5900 or 5910
user:max_non_scis_electives(3).     % per handbook §7.2

% — Elective Courses (all SCIS offerings) —
user:elective(cap5011).  user:elective(cap5109).
user:elective(cap5507).  user:elective(cap5602).
user:elective(cap5610).  user:elective(cap5627).
user:elective(cap5640).  user:elective(cap5701).
user:elective(cap5738).  user:elective(cap5768).
user:elective(cap5771).  user:elective(cap6776).
user:elective(cap6778).  user:elective(cap6736).
user:elective(cap6619).  user:elective(cda5655).
user:elective(cda6939). user:elective(cen5064).
user:elective(cen5076). user:elective(cen5079).
user:elective(cen5082). user:elective(cen5120).
user:elective(cen6070). user:elective(cen6075).
user:elective(cot5310). user:elective(cot5428).
user:elective(cot5520). user:elective(cot6421).
user:elective(cot6446). user:elective(cot6930).
user:elective(cot6931). user:elective(cot6936).
user:elective(cop5621). user:elective(cop6556).
user:elective(cop6611). user:elective(cop6727).
user:elective(cop6795). user:elective(cis5207).
user:elective(cis5208). user:elective(cis5346).
user:elective(cis5370). user:elective(cis5372).
user:elective(cis5373). user:elective(cis5374).
user:elective(cis5432). user:elective(cis5931).
user:elective(cis6612). user:elective(cis6930).
user:elective(cis6931).

% — Approved Non-SCIS Electives (max 1) —
:- multifile user:non_scis_elective/1.
:- dynamic   user:non_scis_elective/1.

user:non_scis_elective(eel6167). user:non_scis_elective(eel5500).
user:non_scis_elective(eel5718). user:non_scis_elective(eel5813).
user:non_scis_elective(eel5820). user:non_scis_elective(eel6787).
user:non_scis_elective(eel6821). user:non_scis_elective(esi6546).
user:non_scis_elective(cnt6154). user:non_scis_elective(eee5348).
user:non_scis_elective(sta5236).
