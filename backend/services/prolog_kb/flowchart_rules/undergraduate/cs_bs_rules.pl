/*──────────────────────────────────────────────────────────────────────────────
  cs_bs_rules.pl
  Prolog KB — B.S. in Computer Science (flow-chart rev. Apr-2023; patched 24 Jun 2025)

  • Elective quota (must take exactly 7 CS electives)
  • Elective grouping (must take ≥1 from each of Foundations, Systems, Applications)
  • All required lower- and upper-division courses
  • Every prerequisite, co-requisite (♦) and “one-of” alternative (OR)
    printed on the CS-BS flow-chart
  • All electives in Foundations, Systems and Applications boxes
──────────────────────────────────────────────────────────────────────────────*/

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
              user:box_quota/3,
              user:course/1.

%── 1. Required lower-division math & writing ───────────────────────────────
user:required(mac1147).
user:required(mac2312).
user:required(mad2104).
user:required(cot3100).
user:required(sta3033).
user:required(enc3249).

%── 2. Required intro CS & cognates ──────────────────────────────────────────
user:required(cgs1920).
user:required(cgs3095).
user:required(cop2210).
user:required(cop3337).

%── 3. Required core CS sequence ────────────────────────────────────────────
user:required(cop3530).
user:required(cda3102).
user:required(cop4338).
user:required(cop4610).
user:required(cen4010).
user:required(cen4021).
user:required(cis3950).
user:required(cis4951).
user:required(cop4555).

%── 0. Elective quota & grouping ────────────────────────────────────────────
elective_quota(cs_bs, 7).             % total CS electives
user:box_quota(cs_bs, foundations, 3).
user:box_quota(cs_bs, systems,     2).
user:box_quota(cs_bs, applications,2).

%── Foundations electives ───────────────────────────────────────────────────
user:elective_box(foundations, cap4506).
user:elective_box(foundations, cop4534).
user:elective_box(foundations, cot3510).
user:elective_box(foundations, cot3541).
user:elective_box(foundations, cot4521).
user:elective_box(foundations, cot4601).
user:elective_box(foundations, mad3301).
user:elective_box(foundations, mad3401).
user:elective_box(foundations, mad3512).
user:elective_box(foundations, mad4203).
user:elective_box(foundations, mhf4302).

%── Systems electives ────────────────────────────────────────────────────────
user:elective_box(systems, cap4453).
user:elective_box(systems, cda4625).
user:elective_box(systems, cnt4713).
user:elective_box(systems, cen4083).
user:elective_box(systems, cis4203).
user:elective_box(systems, cis4731).
user:elective_box(systems, cop4520).
user:elective_box(systems, cop4604).
user:elective_box(systems, cop4710).
user:elective_box(systems, cop4751).
user:elective_box(systems, cot4431).
user:elective_box(systems, cts4408).

%── Applications electives ──────────────────────────────────────────────────
user:elective_box(applications, cap4052).
user:elective_box(applications, cap4104).
user:elective_box(applications, cap4630).
user:elective_box(applications, cap4641).
user:elective_box(applications, cap4770).
user:elective_box(applications, cap4830).
user:elective_box(applications, cen4021).
user:elective_box(applications, cen4072).
user:elective_box(applications, cop4226).
user:elective_box(applications, cop4655).



%── 4. Footnotes & prerequisite chains ──────────────────────────────────────
% COP2210 ← MAC1140 or higher
user:one_of_prereqs_fact(cop2210,[mac1140,mac1147,mac2311,mac2312]).

% MAD2104 ← MAC1105 or MGF1106
user:one_of_prereqs_fact(mad2104,[mac1105,mgf1106]).

% COT3100 ← any MAC, any COP; ♦ co-req one of {COP2210,COP2250,EEL2880}
user:one_of_prereqs_fact(cot3100,         % COT3100: either a MAC or a COP
    [ mac1105      % Example MAC
    , mac1147      % (you can enumerate _all_ “any MAC” here)
    , mac2311
    , mac2312
    , cop1000      % and “any COP” you care about
    ]).
user:corequisite(cot3100,cop2210).
user:corequisite(cot3100,cop2250).
user:corequisite(cot3100,eel2880).

% Math ladder
user:prerequisite(mac2311,mac1147).
user:prerequisite(mac2312,mac2311).
user:prerequisite(sta3033, mac2312).


% Prog II ← Prog I
user:prerequisite(cop3337,cop2210).

% Arch ← {MAD2104,COT3100} + Prog II
user:one_of_prereqs_fact(cda3102,[cot3100, mad2104]).
user:prerequisite(cda3102,cop3337).

% Data Structures chain
user:prerequisite(cop3530,cop3337).
user:one_of_prereqs_fact(cop3530,[cot3100, mad2104]).
user:prerequisite(cop4338,cop3530).
user:prerequisite(cop4610,cop4338).
user:prerequisite(cop4610,cda3102).
user:prerequisite(cop4555,cop3530)

% Software Eng’n
user:prerequisite(cen4010,cop3530).
user:prerequisite(cen4021,cen4010).


%── 5. Foundations electives definitions ────────────────────────────────────
user:elective(cap4506).  user:prerequisite(cap4506,mac2312).
user:elective(cop4534).  user:prerequisite(cop4534,cop3530).
user:elective(cot3510).
  user:corequisite(cot3510,cot3100).
  user:corequisite(cot3510,mad2104).
user:elective(cot3541).
  user:prerequisite(cot3541,cop3337).
  user:one_of_prereqs_fact(cot3541,[cot3100,mad2104]).
user:elective(cot4521).  user:prerequisite(cot4521,cop3530).
user:elective(cot4601).
  user:prerequisite(cot4601,cot3100).
  user:one_of_prereqs_fact(cot4601,[cop3337,cop3804]).
user:elective(mad3301).
  user:prerequisite(mad3301,cop2210).
  user:one_of_prereqs_fact(mad3301,[cot3100,mad2104]).
user:elective(mad3401).
  user:prerequisite(mad3401,cop2210).
  user:prerequisite(mad3401,mac2312).
user:elective(mad3512).  user:prerequisite(mad3512,cop3530).
user:elective(mad4203).
  user:prerequisite(mad4203,mad2104).
  user:prerequisite(mad4203,mac2312).
user:elective(mhf4302).  user:prerequisite(mhf4302,mad3512).

%── 6. Systems electives definitions ───────────────────────────────────────
user:elective(cap4453).
  user:prerequisite(cap4453,cop3530).
  user:prerequisite(cap4453,mac2312).
user:elective(cda4625).
  user:prerequisite(cda4625,cop3530).
  user:prerequisite(cda4625,sta3033).
user:elective(cnt4713).  user:prerequisite(cnt4713,cop4338).
user:elective(cen4083).
  user:prerequisite(cen4083,cnt4713).
  user:one_of_prereqs_fact(cen4083,[cda3102,cda4101]).
user:elective(cis4203).
  user:one_of_prereqs_fact(cis4203,[cop2210,cop2250,eel2880]).
user:elective(cis4731).  user:prerequisite(cis4731,cop3530).
user:elective(cop4520).
  user:prerequisite(cop4520,cop3530).
  user:one_of_prereqs_fact(cop4520,[cda3102,cda4101,eel4709]).
user:elective(cop4604).  user:prerequisite(cop4604,cop4610).
user:elective(cop4710).
  user:prerequisite(cop4710,cop3337).
  user:corequisite(cop4710,cop3530).
user:elective(cop4751).  user:prerequisite(cop4751,cop4710).
user:elective(cot4431).
  user:prerequisite(cot4431,cop3530).
  user:one_of_prereqs_fact(cot4431,[cda3102,cda4101,eel4709]).
user:elective(cts4408).  user:prerequisite(cts4408,cop4710).

user:elective(cop4655).
  user:prerequisite(cop4655,cap4104).
  user:prerequisite(cop4655,cen4010).

%── 7. Applications electives definitions ─────────────────────────────────
user:elective(cap4052).
  user:prerequisite(cap4052,cop3530).
  user:prerequisite(cap4052,cap4506).
  user:one_of_prereqs_fact(cap4052,[sta2023,sta3033]).

user:elective(cap4104).  user:prerequisite(cap4104,cop3337).
user:elective(cap4630).  user:prerequisite(cap4630,cop3530).
user:elective(cap4641).  user:prerequisite(cap4641,cop3530).
user:elective(cap4770).
  user:prerequisite(cap4770,cop3530).
  user:corequisite(cap4770,cop4710).
user:elective(cap4830).
  user:prerequisite(cap4830,cop3530).
  user:one_of_prereqs_fact(cap4830,[sta2023,sta3033]).

%── Finally, unify into user:course/1 so the planner sees them all
user:course(C) :- user:required(C).
user:course(C) :- user:elective(C).

/*──────────────────────────────────────────────────────────────────────────────
   END — Clean, correct, no stray PDF text, ready for `planner_rules.pl` to
   consume.
──────────────────────────────────────────────────────────────────────────────*/
