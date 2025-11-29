:- module(validator_rules,
          [ validate_id/4,
            needed_chain/3,
            title_or_stub/2,
            in_program/1,
            top_sort/3,
            missing_courses/3
          ]).

:- use_module(library(apply)).
:- use_module(library(yall)).

%──────────────────────────────────────────────────────────────────────────────
%  Import flow-chart facts from the *user* module (visibility wrappers only)
%──────────────────────────────────────────────────────────────────────────────
:- multifile user:one_of_prereqs_fact/2,
             user:required/1,
             user:elective/1, user:elective/2,
             user:prerequisite/2, user:corequisite/2,
             user:credit/2, user:offered/2.

one_of_prereqs_fact(A,B) :- user:one_of_prereqs_fact(A,B).

required(X)       :- user:required(X).
elective(X)       :- user:elective(X).
elective(G,X)     :- user:elective(G,X).
prerequisite(A,B) :- user:prerequisite(A,B).
corequisite(A,B)  :- user:corequisite(A,B).
credit(A,B)       :- user:credit(A,B).
offered(A,B)      :- user:offered(A,B).

%──────────────────────────────────────────────────────────────────────────────
%  Quick membership helper
%──────────────────────────────────────────────────────────────────────────────
in_program(ID) :- required(ID), !.
in_program(ID) :- elective(ID) ; elective(_,ID), !.
in_program(ID) :- prerequisite(ID,_), !.
in_program(ID) :- prerequisite(_,ID), !.
in_program(ID) :- corequisite(ID,_), !.
in_program(ID) :- corequisite(_,ID).

% ------------------------------------------------------------------
%  Filters term:
%     filters(+Taken:list, +CreditCap:int/var, +Semester:any|fall|spring|summer)
% ------------------------------------------------------------------
credit_ok(Cap, _)       :- var(Cap), !.          % no cap filter
credit_ok(Cap, Credits) :- Credits =< Cap.

semester_ok(any, _).
semester_ok(Sem, Off)   :- Sem == Off.

prereqs_met(Course, []) :-
    \+ prerequisite(Course, _),
    \+ user:one_of_prereqs_fact(Course, _).

prereqs_met(Course, Taken) :-
    ( user:one_of_prereqs_fact(Course, Alts)
    -> memberchk(Alt, Alts), memberchk(Alt, Taken)
    ;  forall(prerequisite(Course,P), memberchk(P,Taken))
    ).

% ---- flat_maplist(+Pred,+In,-FlatOut) --------------------------------------
flat_maplist(Pred, In, Out) :-
    maplist(Pred, In, Nested),
    append(Nested, Out).

% ---- helper: explode "..._and_..." composite atoms -------------------------
explode_and_bundle(ID, Parts) :-
    atom(ID),
    sub_atom(ID,_,_,_,'_and_'), !,
    atomic_list_concat(Parts, '_and_', ID).
explode_and_bundle(ID, [ID]).

% ───────────────────────────────────────────────────────────────────
%  Rule-level violations (produce *tag* list)
% ───────────────────────────────────────────────────────────────────
rule_violation(ID, _, not_in_program) :-
    \+ in_program(ID).

rule_violation(ID, filters(_, Cap, _), credit_over_cap) :-
    nonvar(Cap),
    credit(ID, Cr),
    Cr > Cap.

rule_violation(ID, filters(_, _, Sem), wrong_semester) :-
    Sem \== any,
    offered(ID, Off),
    Sem \== Off.

rule_violation(ID, filters(Taken, _, _), missing_prereq) :-
    % true when *any* required prerequisite (simple or alternative) is
    % still unmet
    \+ prereqs_met(ID, Taken).

missing_courses(ID, Taken, Missing) :-
  % if there are “one of” alternatives, filter out the ones already taken
  ( user:one_of_prereqs_fact(ID, Alts) ->
      findall(Alt,
              ( member(Alt, Alts),
                \+ memberchk(Alt, Taken)
              ),
              AltMissing)
  ; AltMissing = []
  ),
  % now gather any simple prereqs not yet in Taken
  findall(P, ( prerequisite(ID,P),
               \+ memberchk(P, Taken)
             ),
          Prims),
  append(Prims, AltMissing, All),
  sort(All, Missing).


% ---- master validator ------------------------------------------------------
validate_id(ID, Filters, keep, []) :-
    \+ rule_violation(ID, Filters, _), !.

validate_id(ID, Filters, reject, Tags) :-
    findall(Tag, rule_violation(ID, Filters, Tag), Raw),
    sort(Raw, Tags),
    Tags \= [].

% ---------------------------------------------------------------------------
%  needed_chain(+Course, +Taken:list, -Chain:list)
%    produce a topo‐sorted list of *all* the missing dependencies,
%    including any one‐of‐prereqs, so the UI can show them.
% ---------------------------------------------------------------------------
needed_chain(Course, Taken, Chain) :-
    needed_(Taken, Course, [], Raw0),
    flat_maplist(explode_and_bundle, Raw0, Raw),
    sort(Raw, Dedup),
    findall(A-B, prerequisite(A,B), Edges),  % simple edges for ordering
    top_sort(Dedup, Edges, Chain).

% ---- depth-first gather including one_of_prereqs_fact ----------------------
needed_(Taken, C, Acc, Acc) :-
    memberchk(C, Taken), !.
needed_(Taken, C, Acc0, Acc) :-
    % missing_courses/3 already expands both:
    %  - all simple prerequisite(C,P)
    %  - any one_of_prereqs_fact(C,Alts) alternatives not in Taken
    missing_courses(C, Taken, Ps),
    foldl(needed_(Taken), Ps, Acc0, Acc1),
    Acc = [C|Acc1].

% ---- simple topo-sort using prerequisite/2 as edges ------------------------
top_sort([], _, []).
top_sort(Nodes, Edges, [H|T]) :-
    select(H, Nodes, Ns1),
    \+ member(H-_, Edges),              % no outgoing prereq edge
    exclude(edge_involves(H), Edges, Es1),
    top_sort(Ns1, Es1, T).

edge_involves(N, A-B) :- A==N ; B==N.

% ---------------------------------------------------------------------------
%  course_title/2 helper (fallback stub)
% ---------------------------------------------------------------------------
:- multifile course_title/2.
course_title(_, "(title unavailable)").          % default stub

title_or_stub(ID, Title) :-
    ( course_title(ID, T) -> Title = T
    ; atom_string(ID, S),  Title = S ).
