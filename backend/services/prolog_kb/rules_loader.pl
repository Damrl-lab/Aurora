%  rules_loader.pl  – master loader for the Prolog KB
%  --------------------------------------------------

% ── predicate declarations ───────────────────────────────────────────
:- multifile
       program_rules/2,
       user:required/1,
       user:prerequisite/2,
       user:corequisite/2,
       user:one_of_prereqs_fact/2.

:- dynamic
       program_rules/2,
       current_program/1,
       user:required/1,
       user:prerequisite/2,
       user:corequisite/2,
       user:one_of_prereqs_fact/2.

% allow discontiguous predicates spread across files
:- discontiguous
       course/1, credit/2, offered/2,
       prerequisite/2, corequisite/2, one_of_prereqs_fact/2,
       recommended/3, recommended_sdd/3,
       can_take/2.

% ── 1. catalogue facts ──────────────────────────────────────────────
% :- consult('courses_facts.pl').  <- dont need this anymore... For rules we will only rely on the program_facts!

% ── 2. helper: consult but ignore syntax-error files ────────────────
safe_consult(File) :-
    catch(consult(File),
          error(syntax_error(_), _),
          ( print_message(warning,
                          format('Skipping ~w – syntax error', [File])),
            fail )).

% ── 3. registry of programme → rule-file pairs (facts) ──────────────
% 3a) undergraduate
program_rules(cs_ba     ,'flowchart_rules/undergraduate/cs_ba_rules.pl').
program_rules(cs_bs     ,'flowchart_rules/undergraduate/cs_bs_rules.pl').
program_rules(cs_bs_ssd ,'flowchart_rules/undergraduate/cs_bs_sdd_rules.pl').
program_rules(cs_minor  ,'flowchart_rules/undergraduate/cs_minor_rules.pl').
program_rules(ds_bs     ,'flowchart_rules/undergraduate/ds_bs_rules.pl').
program_rules(it_ba     ,'flowchart_rules/undergraduate/it_ba_rules.pl').
program_rules(it_bs     ,'flowchart_rules/undergraduate/it_bs_rules.pl').
program_rules(it_sw     ,'flowchart_rules/undergraduate/it_bs_sw.pl').

% 3b) graduate
program_rules(ms_cs     ,'flowchart_rules/graduate/ms_cs_rules.pl').
program_rules(ms_ds     ,'flowchart_rules/graduate/ms_ds_rules.pl').
program_rules(ms_it     ,'flowchart_rules/graduate/ms_it_rules.pl').
program_rules(phd_cs    ,'flowchart_rules/graduate/phd_cs_rules.pl').

% ── 4. public helper – load exactly one flow-chart into memory ──────
load_program(Prog) :-
    % clear out any previous state
    retractall(current_program(_)),
    retractall(user:required(_)),
    retractall(user:prerequisite(_,_)),
    retractall(user:corequisite(_,_)),
    retractall(user:one_of_prereqs_fact(_,_)),

    % always load eligibility rules first, so validate_id/4 is available
    safe_consult('flowchart_rules/eligibility_rules.pl'),

    % now load the program-specific rules
    program_rules(Prog,File),
    safe_consult(File),

    % mark which program is active
    asserta(current_program(Prog)).

% ── 5. always-loaded support rule files ─────────────────────────────
:- consult('flowchart_rules/eligibility_rules.pl').
:- consult('./planner_rules.pl').
:- consult('./course_titles.pl').
:- consult('./validator_rules.pl').  
:- reexport(validator_rules, [validate_id/4, needed_chain/3]).

