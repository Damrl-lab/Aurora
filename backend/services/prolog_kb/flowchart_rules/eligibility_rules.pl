% -------------------------------------------------------------------
% flowchart_rules/eligibility_rules.pl
% -------------------------------------------------------------------

% allow predicates to be spread across files
:- discontiguous recommended/3, recommended_sdd/3.
:- discontiguous prerequisite/2, corequisite/2, one_of_prereqs/2.
:- discontiguous can_take/2.

% -------------------------------------------------------------------
% 1) Year-by-year recommended courses for CS-BS
%    plan_of_study(cs_bs, Year, Plan).
% -------------------------------------------------------------------
recommended(cs_bs, freshman,  [cgs1920, mac2311, mac2312, cs_science1, ucc1, ucc2, ucc3, ucc4, ucc5]).
recommended(cs_bs, sophomore, [cop2210, cot3100_or_mad2104, phy2048, phy2049, ucc6, ucc7, cs_science2, gen_elective1]).
recommended(cs_bs, junior,    [cda3103, cop3337, enc3249, sta3033, cgs3095, cop3530, cot3541, cop4338, cda4101, cs_elective1]).
recommended(cs_bs, senior,    [cnt4713, mad3512, cen4010, cop4555, cop4710, cop4610, cis3950, cis4951, cs_elective2, gen_elective2]).

% -------------------------------------------------------------------
% 2) Year-by-year recommended courses for CS-BS-SDD
%    plan_of_study(cs_bs_sdd, Year, Plan).
% -------------------------------------------------------------------
recommended(cs_bs_sdd, freshman,  [cgs1920, mac2311, mac2312, cs_science1, ucc1, ucc2, ucc3, ucc4, ucc5]).
recommended(cs_bs_sdd, sophomore, [cop2210, cot3100_or_mad2104, phy2048, phy2049, ucc6, ucc7, cs_science2, gen_elective1]).
recommended(cs_bs_sdd, junior,    [cda3103, cop3337, enc3249, sta3033, cop3530, cop4338, cot3541, cda4101, cgs3095, gen_elective2]).
recommended(cs_bs_sdd, senior,    [cnt4713, mad3512, cen4010, cop4555, cop4710, cop4610, cen4021, cen4072, cis3950, cis4951, cs_elective]).

% -------------------------------------------------------------------
% 3) plan_of_study/3 dispatches to the right recommended/3 fact
% -------------------------------------------------------------------
plan_of_study(cs_bs,      Year, Plan) :- recommended(cs_bs,      Year, Plan).
plan_of_study(cs_bs_sdd,  Year, Plan) :- recommended(cs_bs_sdd,  Year, Plan).

% -------------------------------------------------------------------
% 4) Eligibility checker (exactly as before):
%    can_take(Course, TakenCoursesList).
% -------------------------------------------------------------------
% no prereqs → can take
can_take(Course, Taken) :-
  \+ prerequisite(Course, _),
  \+ one_of_prereqs(Course, _),
  \+ corequisite(Course, _).

% all hard prereqs must be in Taken
can_take(Course, Taken) :-
  findall(P, prerequisite(Course, P), Prs),
  subset(Prs, Taken).

% satisfy any‐of prereqs
can_take(Course, Taken) :-
  one_of_prereqs(Course, Options),
  member(Opt, Options),
  member(Opt, Taken).

% satisfy coreq by already having it
can_take(Course, Taken) :-
  corequisite(Course, Coreq),
  member(Coreq, Taken).

% -------------------------------------------------------------------
% 5) subset helper
% -------------------------------------------------------------------
subset([], _).
subset([H|T], List) :-
  member(H, List),
  subset(T, List).
