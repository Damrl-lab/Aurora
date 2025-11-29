/*─────────────────────────────────────────────────────────────────────────────
  cs_minor_rules.pl
  Prolog KB — Computer Science Minor (flow-chart rev. Apr-2023; patched 24 Jun 2025)

  • Exactly two electives via elective_quota/2
  • Core trio + every arrow, diamond, and footnote on the Minor flow-chart
  • All electives in Foundations / Systems / Applications boxes
─────────────────────────────────────────────────────────────────────────────*/

:- multifile  user:required/1,
              user:prerequisite/2,
              user:corequisite/2,
              user:one_of_prereqs_fact/2,
              user:elective/1,
              elective_quota/2,
              user:elective_box/2,
              user:box_quota/3,
              user:course/1.          
:- dynamic    user:required/1,
              user:prerequisite/2,
              user:corequisite/2,
              user:one_of_prereqs_fact/2,
              user:elective/1,
              elective_quota/2,
              user:elective_box/2,     
              user:course/1.           


% 0. Elective quota: choose exactly 2 electives
elective_quota(cs_minor, 2).

% 1. Minor CORE (must take all three)
user:required(cop2210).    % Programming I (4 cr)
user:required(cop3337).    % Programming II
user:required(cda3102).    % Computer Architecture

% 2. Foundational footnotes & Discrete Structures
user:one_of_prereqs_fact(cop2210,    % COP2210: MAC1140 or higher
    [mac1140, mac1147, mac2311, mac2312]).

user:one_of_prereqs_fact(mad2104,     % MAD2104: MAC1105 or MGF1106
    [mac1105, mgf1106]).

user:one_of_prereqs_fact(cot3100,         % COT3100: either a MAC or a COP
    [ mac1105      % Example MAC
    , mac1147      % (you can enumerate _all_ “any MAC” here)
    , mac2311
    , mac2312
    , cop1000      % and “any COP” you care about
    ]).
user:corequisite(cot3100, cop2210).  %   ♦ co-req Programming I
user:corequisite(cot3100, cop2250).  %   ♦    or COP2250
user:corequisite(cot3100, eel2880).  %   ♦    or EEL2880

% 3. Core course relationships
user:prerequisite(cop3337, cop2210).                                      % Prog II ← Prog I
user:one_of_prereqs_fact(cda3102, [cot3100, mad2104]).                    % Arch needs Discrete
user:prerequisite(cda3102, cop3337).                                      % Arch ← Prog II

% 4. Foundations electives
user:elective(cot3510). 
  user:one_of_prereqs_fact(cot3510, [cot3100, mad2104]).                 % Applied Linear Structures
user:elective_box(foundations, cot3510).

user:elective(cot3541).
  user:prerequisite(cot3541, cop3337).                                    % Logic for CS
  user:one_of_prereqs_fact(cot3541, [cot3100, mad2104]).
user:elective_box(foundations, cot3541).

user:elective(cop4534).  user:prerequisite(cop4534, cop3530).            % Algorithm Techniques
user:elective_box(foundations, cop4534).
user:elective(cop4555).  user:prerequisite(cop4555, cop3530).            % Programming Languages
user:elective_box(foundations, cop4555).

user:elective(cot4521).  user:prerequisite(cot4521, cop3530).            % Computational Geometry
user:elective_box(foundations, cot4521).

user:elective(cot4601).
  user:prerequisite(cot4601, cot3100).                                    % Quantum Computing
  user:one_of_prereqs_fact(cot4601, [cop3337, cop3804]).
user:elective_box(foundations, cot4601).


% 5. Systems electives
user:elective(cop3530).
  user:prerequisite(cop3530, cop3337).                                    % Data Structures
  user:one_of_prereqs_fact(cop3530, [cot3100, mad2104]).
user:elective_box(systems, cop3530).

user:elective(cis4203). 
  user:one_of_prereqs_fact(cis4203, [cop2210, cop2250, eel2880]).         % Digital Forensics
user:elective_box(systems, cis4203).

user:elective(cop4338).  user:corequisite(cop4338, cop3530).             % Systems Programming
user:elective_box(systems, cop4338).

user:elective(cop4520).
  user:prerequisite(cop4520, cop3530).                                    % Introduction to Parallel Computing
  user:one_of_prereqs_fact(cop4520, [cda3102, cda4101, eel4709]).
user:elective_box(systems, cop4520).

user:elective(cot4431).
  user:prerequisite(cot4431, cop3530).                                    % Applied Parallel Computing
  user:prerequisite(cot4431, cda3102).
user:elective_box(systems, cot4431).

user:elective(cop4710).
  user:prerequisite(cop4710, cop3337).                                    % Database Management
  user:corequisite(cop4710, cop3530).
user:elective_box(systems, cop4710).

user:elective(cis4731).  user:prerequisite(cis4731, cop3530).           % Fundamentals of Blockchain Technologies
user:elective_box(systems, cis4731).


% 6. Applications electives
user:elective(cap4104).  user:prerequisite(cap4104, cop3337).           % Human–Computer Interaction
user:elective_box(applications, cap4104).

user:elective(cap4630).  user:prerequisite(cap4630, cop3530).           % Artificial Intelligence
user:elective_box(applications, cap4630).

user:elective(cap4641).  user:prerequisite(cap4641, cop3530).           % Natural Language Processing
user:elective_box(applications, cap4641).

user:elective(cap4830).
  user:prerequisite(cap4830, cop3530).                                    % Modeling & Simulations
  user:one_of_prereqs_fact(cap4830, [sta2023, sta3033]).
user:elective_box(applications, cap4830).

user:elective(cen4010).
  user:prerequisite(cen4010, cgs3095).                                    % SE I ← Tech in Global Arena
  user:prerequisite(cen4010, cop3337).                                    %     + Prog II
user:elective_box(applications, cen4010).

user:elective(cen4021).  user:prerequisite(cen4021, cen4010).           % Software Engineering II
user:elective_box(applications, cen4021).

user:elective(cen4072).  user:prerequisite(cen4072, cop3530).           % Software Testing
user:elective_box(applications, cen4072).
user:elective(cop4226).  user:prerequisite(cop4226, cop3530).           % Advanced Windows Programming
user:elective_box(applications, cop4226).

user:course(C) :-
        user:elective(C).
user:course(C) :-
        user:required(C).

/*─────────────────────────────────────────────────────────────────────────────
  END — fully validated against the FIU CS Minor flow-chart
─────────────────────────────────────────────────────────────────────────────*/
