/*  =============================================================
    Long-Term Planner  – quota-aware version
    =============================================================  */

:- module(planner_rules,
          [ make_plan/5          % +Prog,+Taken,+Cap,+Start,-Plan
          , prereq_plan/5        % +Prog,+Taken,+Cap,+Start,-Plan
          ]).

/*------------------------------------------------------------------ 0 */
:- multifile
       recommended/3,
       prerequisite/2, corequisite/2, one_of_prereqs_fact/2,
       required/1,     elective/1,
       credit/2,
       elective_quota/2,
       elective_box/2, box_quota/3,
       user:course/1.

:- dynamic   credit/2, user:course/1, built_catalogue_flag/0.

:- discontiguous prog_source/2, flowchart_course/2.
:- use_module(library(lists)).

/*------------------------------------------------------------------
   Visibility wrappers – every flow-chart file asserts into `user`
------------------------------------------------------------------*/
required(X)              :- user:required(X).
elective(X)              :- user:elective(X).

prerequisite(A,B)        :- user:prerequisite(A,B).
corequisite(A,B)         :- user:corequisite(A,B).
one_of_prereqs_fact(A,B) :- user:one_of_prereqs_fact(A,B).

recommended(P,G,L)       :- user:recommended(P,G,L).
elective_quota(P,N)      :- user:elective_quota(P,N).
elective_box(Box,C)      :- user:elective_box(Box,C).
box_quota(P,Box,N)       :- user:box_quota(P,Box,N).
/*------------------------------------------------------------------*/

/*------------------------------------------------------------------ 1  build course catalogue & default credits */
fill_missing_credits :-
    forall(
        (   user:required(C)
        ;   user:elective(C)
        ;   user:prerequisite(_,C)
        ;   user:prerequisite(C,_)
        ;   user:corequisite(_,C)
        ;   user:corequisite(C,_)
        ;   user:one_of_prereqs_fact(_,Opts), member(C,Opts)
        ),
        ( user:course(C) -> true ; assertz(user:course(C)) )
    ),
    forall(user:course(C),
           ( credit(C,_) -> true ; assertz(credit(C,3)) )).

ensure_catalogue :-                 % run only once per Prolog session
    ( built_catalogue_flag -> true
    ; assertz(built_catalogue_flag), fill_missing_credits ).

/*------------------------------------------------------------------ 2  helpers */
semester_cap(fall,18).   semester_cap(spring,18).  semester_cap(summer,12).
min_courses_per_semester(3).

next_semester(fall,spring).
next_semester(spring,summer).
next_semester(summer,fall).

char_type_digit(C) :- char_type(C,digit).
char_type_upper(C) :- char_type(C,upper).
char_type_lower(C) :- char_type(C,lower).

valid_course_id(A) :-
    atom_chars(A,[C1,C2,C3,D1,D2,D3,D4]),
    maplist(char_type_digit,[D1,D2,D3,D4]),
    ( maplist(char_type_upper,[C1,C2,C3])
    ; maplist(char_type_lower,[C1,C2,C3]) ).

cap_for(Sem,Def,Cap) :- semester_cap(Sem,L), !, Cap is min(Def,L).
cap_for(_,Def,Def).

min_credit(M) :-
    findall(Cr,(credit(_,Cr),Cr>0),Cs),
    ( Cs = [] -> M=0 ; min_list(Cs,M) ).

can_take_after(Taken,C) :-
    forall(user:prerequisite(C,P), memberchk(P,Taken)),
    (   \+ user:one_of_prereqs_fact(C,_)
    ->  true
    ;   user:one_of_prereqs_fact(C,Opts),
        member(Opt,Opts), memberchk(Opt,Taken)
    ),
    forall(user:corequisite(C,Co), \+ \+ (memberchk(Co,Taken); true)).

/*--- one-of pruning ---------------------------------------------------*/
remove_one_of_alternatives(BagIn,BagOut) :-
    foldl(prune_list,BagIn,BagIn,BagOut).

prune_list(Course,AccIn,AccOut) :-
    (   user:one_of_prereqs_fact(_,List),
        member(Course,List),
        append(_, [Course|Tail], List),
        intersection(Tail,AccIn,Victims),
        Victims \== []
    ->  subtract(AccIn,Victims,AccOut)
    ;   AccOut = AccIn).

/*--- corequisite fixer ------------------------------------------------*/
ensure_coreqs(Taken,Pick0,Pick) :-
    foldl(add_missing_coreqs(Taken),Pick0,Pick0,Pick1),
    sort(Pick1,Pick).

add_missing_coreqs(Taken,C,Acc,Out) :-
    findall(Co,(user:corequisite(C,Co),
                \+ memberchk(Co,Taken),
                \+ memberchk(Co,Acc)),Miss),
    append(Acc,Miss,Out).

/*--- dependent score (for smarter ordering) ---------------------------*/
dependent_score(Course,Key) :-
    findall(D,predecessor(D,Course),Deps),
    sort(Deps,U), length(U,Cnt), Key is -Cnt.

/*--- when nothing is eligible, pull unlockers -------------------------*/
fill_until_cap_or_min(_,_,Acc,Cap,Acc) :-
    ( length(Acc,N), min_courses_per_semester(Min), N >= Min )
 ;  ( total_credits(Acc,Cr), Cr >= Cap ), !.

fill_until_cap_or_min(Taken,[Locked|Rest],Acc0,Cap,Acc) :-
    deps_of(Locked,Deps),
    subtract(Deps,Taken,Missing),
    append(Acc0,Missing,Acc1),
    fill_until_cap_or_min(Taken,Rest,Acc1,Cap,Acc).

total_credits(List,Sum) :-
    findall(Cr,(member(C,List),credit(C,Cr)),Cs), sum_list(Cs,Sum).


/*--- cap-trim & top-up helpers ------------------------------------*/
trim_to_cap(Pick0,CapLim,Pick) :-
    total_credits(Pick0,Cr),
    ( Cr =< CapLim ->
        Pick = Pick0
    ; predsort(inv_cmp_score, Pick0, S),   % weakest first
      trim_loop(S,CapLim,Pick) ).

trim_loop([_|Rest],CapLim,Pick) :-            % drop one, re-check
    total_credits(Rest,Cr),
    ( Cr =< CapLim -> Pick = Rest
    ; trim_loop(Rest,CapLim,Pick) ).

fill_to_min(PickIn,CapLim,Taken,Need,PickOut) :-
    append(Taken,PickIn,Context),               % ← courses *already* available
    length(PickIn,N), min_courses_per_semester(Min),
    ( N >= Min ->
        PickOut = PickIn                        % already ≥ Min courses
    ; subtract(Need,PickIn,Remaining),
      include({Context}/[C]>>can_take_after(Context,C),Remaining,Cands),
      total_credits(PickIn,Used),
      RemCap is CapLim - Used,                 % spare credits this block
      pick_within_credit(Cands,RemCap,Extra),
      append(PickIn,Extra,Temp),
      sort(Temp,PickOut)
    ).


/*--- prerequisite fixer -----------------------------------------------*/
ensure_prereqs(Taken,Pick0,Pick) :-
    % give each callback access to the *full* pick-list (Pick0)
    foldl(add_missing_prereqs(Taken,Pick0),Pick0,Pick0,Temp),
    sort(Temp,Pick).

add_missing_prereqs(Taken,Full,C,Acc,Out) :-
    % hard prereqs ------------------------------------------------------
    findall(P,(user:prerequisite(C,P),
               \+ memberchk(P,Taken),
               \+ memberchk(P,Acc)),Hard),
    % one-of list -------------------------------------------------------
    (   user:one_of_prereqs_fact(C,Opts),
        \+ (member(O,Opts),
            (   memberchk(O,Taken)              % already completed
            ;   memberchk(O,Acc)                % already in Acc
            ;   memberchk(O,Full)               % will be taken *this* term
            ))
    ->  % pick the *earliest* candidate that is still in Need
        member(Choice,Opts),
        \+ memberchk(Choice,Full),              % avoid duplicates
        OneOf = [Choice]
    ;   OneOf = []
    ),
    append(Acc,Hard,R1),
    append(R1,OneOf,Out).


/*------------------------------------------------------------------ 3  elective-quota logic (unchanged) */
take_first_n(N,List,FirstN) :- length(FirstN,N), append(FirstN,_,List), !.

quota_electives(Prog,All,Kept) :-
    findall(Box-Q, box_quota(Prog,Box,Q), BoxQs0),
    sort(BoxQs0,BoxQs),
    ( BoxQs \== []
    -> pick_boxes(BoxQs,All,[],Tmp), sort(Tmp,Kept0)
    ; ( elective_quota(Prog,Q), length(All,L), L >= Q
      -> take_first_n(Q,All,Kept0)
      ;  Kept0 = All )
    ),
    %------------------------------------------------------------------
    %  Fallback: if for any reason no electives were retained
    %  (e.g. mis-labelled box facts), fall back to *all* electives
    %------------------------------------------------------------------
    ( Kept0 == [] -> Kept = All
    ;                Kept = Kept0
    ).

pick_boxes([],_,Kept,Kept).
/*-------------------------------------------------------------
   pick_boxes(+BoxQs,+AllElectives,+Acc0,-Kept)
   ‣  Prefer “bridge” electives: ones that are pre/core-requisites
      (or an option in a one-of list) of *any* other elective.
   ‣  Fill the rest of the quota with the remaining courses
      in the original alphabetical order.
-------------------------------------------------------------*/
pick_boxes([Box-Q|Rest],All,Acc0,Kept) :-
    include(elective_in(Box),All,BoxEls0),
    sort(BoxEls0,BoxEls),                 % deterministic order

    include(is_bridge,BoxEls,Bridges),
    subtract(BoxEls,Bridges,NonBridges),

    append(Bridges,NonBridges,Pref),
    ( length(Pref,Len), Len >= Q
    -> take_first_n(Q,Pref,Chosen0)
    ;  Chosen0 = Pref                      % not enough – keep what exists
    ),
    sort(Chosen0,Chosen),

    append(Acc0,Chosen,Acc1),
    pick_boxes(Rest,All,Acc1,Kept).

/*  An elective is a *bridge* if it is referenced as a prerequisite,
    corequisite, or inside a one-of list of another course.            */
is_bridge(C) :-
    (   user:prerequisite(_X,C)
    ;   user:corequisite(_X,C)
    ;   user:one_of_prereqs_fact(_X,Opts),
        member(C,Opts)
    ), !.

elective_in(Box,C) :- elective_box(Box,C).

/*------------------------------------------------------------------ 4  course harvest */
base_courses(Prog,Base) :-
    findall(C,required(C),Required),

    findall(E,user:elective(E),AllE0),
    sort(AllE0,AllE),
    quota_electives(Prog,AllE,Electives),

    /*------------------------------------------------------------
       4a.  “Hidden” prerequisites
            (things that appear only on the RHS of a pre-/co-req
             or in a one-of list, e.g. MAC1140 for COP 2210)
    ------------------------------------------------------------*/
    findall(D,
            ( flowchart_course(Prog,C),
              (   user:prerequisite(C,D)
              ;   user:corequisite(C,D)
              ;   user:one_of_prereqs_fact(C,Opts), member(D,Opts)
              ),
              \+ memberchk(D,Required),
              \+ memberchk(D,Electives)
            ),
            Hidden0),
    sort(Hidden0,Hidden),            % dedupe – keep Prolog order

    /*------------------------------------------------------------
       4b.  Everything else that lives on the flow-chart
            but isn’t required, elective, or hidden.
    ------------------------------------------------------------*/
    findall(C,
            ( flowchart_course(Prog,C),
              \+ memberchk(C,Required),
              \+ memberchk(C,Electives),
              \+ memberchk(C,Hidden),
              \+ ( user:one_of_prereqs_fact(_,Opts),
                   member(C,Opts)
                 )
            ),
            Others),

    include({Required}/[C]>>can_take_after(Required,C), Electives, _ElectivesOk),
    remove_one_of_alternatives(Hidden, HiddenPruned),

    % now rebuild the bag, putting your electives *all* back in
    append([Required,Electives,HiddenPruned,Others],Bag0),
    include(valid_course_id, Bag0, Bag1),
    sort(Bag1,Base).

/*------------------------------------------------------------------ 5  greedy picker */
pick_within_credit(Cands,Cap,Pick) :-
    predsort(cmp_score,Cands,Sorted),
    greedy_pick(Sorted,Cap,[],R),
    reverse(R,Pick).             

cmp_score(<,A,B) :- dependent_score(A,KA), dependent_score(B,KB), KA < KB.
cmp_score(>,A,B) :- dependent_score(A,KA), dependent_score(B,KB), KA > KB.
cmp_score(=,A,B) :- dependent_score(A,K),  dependent_score(B,K).

inv_cmp_score(<,A,B) :- dependent_score(A,KA), dependent_score(B,KB), KA > KB.
inv_cmp_score(>,A,B) :- dependent_score(A,KA), dependent_score(B,KB), KA < KB.
inv_cmp_score(=,A,B) :- dependent_score(A,K),  dependent_score(B,K).


greedy_pick([],_,Acc,Acc).
greedy_pick([C|Rs],Cap,Acc,Out) :-
    credit(C,Cr),
    ( Cr =< Cap
    -> Cap1 is Cap-Cr, greedy_pick(Rs,Cap1,[C|Acc],Out)
    ;  greedy_pick(Rs,Cap ,Acc,Out) ).

/*------------------------------------------------------------------ 6  scheduler */
schedule(_,[],_,_,[]) :- !.
schedule(Taken,Need,Cap0,Sem,[block(Sem,Pick)|Rest]) :-
    cap_for(Sem,Cap0,CapLim),
    include(can_take_after(Taken),Need,Elig),

    (   Elig == []
    ->  Need = [FirstLocked|_],
        fill_until_cap_or_min(Taken,Need,[FirstLocked],CapLim,PickSeed)
    ;   pick_within_credit(Elig,CapLim,Pick0),
        ( Pick0 == [] ->
              Elig = [Fallback|_], PickSeed = [Fallback]
        ;     PickSeed = Pick0 )
    ),
    ensure_coreqs(Taken,PickSeed,Pick1),
    ensure_prereqs(Taken,Pick1,Pick2),
    trim_to_cap(Pick2,CapLim,Pick3),
    fill_to_min(Pick3,CapLim,Taken,Need,Pick),
    subtract(Need,Pick,Left),
    append(Taken,Pick,NewTaken),
    next_semester(Sem,Next),
    schedule(NewTaken,Left,Cap0,Next,Rest).

/*------------------------------------------------------------------ 7  flow-chart helpers */
prog_source(Prog,F) :- atom_concat(Prog,'_rules.pl',Tail),
                       sub_atom(F,_,_,0,Tail).

flowchart_course(_P,C) :- required(C), !.
flowchart_course(_P,C) :- user:elective(C), !.
flowchart_course(P,C)  :-
    recommended(P,_,L), member(C,L),
    valid_course_id(C),          
    !.
flowchart_course(P,C) :-
    ( clause(user:prerequisite(C,_),_,R)
    ; clause(user:corequisite(C,_),_,R)
    ; clause(user:one_of_prereqs_fact(C,_),_,R)
    ),
    clause_property(R,file(F)),
    prog_source(P,F),
    valid_course_id(C). 

/*------------------------------------------------------------------ 8  dependency utils */
predecessor(C,P)         :- predecessor(C,P,[C]).
predecessor(C,P,_)       :- user:prerequisite(C,P).
predecessor(C,P,Seen)    :-
       user:prerequisite(C,Q),
       \+ memberchk(Q,Seen),
       predecessor(Q,P,[Q|Seen]).

deps_of(C,Deps) :-
    findall(D,( predecessor(C,D)
              ; user:corequisite(C,D)
              ; user:one_of_prereqs_fact(C,Opts), member(D,Opts)
              ),Bag),
    sort(Bag,Deps).

/*------------------------------------------------------------------ 9  public entry points */
make_plan(Prog,Taken,Cap,Start,Plan) :-
    ensure_catalogue,
    min_credit(Min), Cap >= Min,
    % 1) collect every course we could ever schedule
    base_courses(Prog,All0),

    % 2) strip out any “hidden” prereqs of courses they’ve already taken
    findall(D,
        ( member(TakenCourse,Taken),
          ( prerequisite(TakenCourse,D)
          ; corequisite(TakenCourse,D)
          ; one_of_prereqs_fact(TakenCourse,Opts), member(D,Opts)
          )
        ),
        ToRemove0
    ),
    sort(ToRemove0, HiddenTaken),
    subtract(All0, HiddenTaken, All1),

    % 3) drop everything they’ve already completed
    subtract(All1, Taken, Need),

    % 4) run the scheduler
    schedule(Taken, Need, Cap, Start, Plan).

prereq_plan(Prog,Taken,Cap,Start,Plan) :-
    ensure_catalogue,
    min_credit(Min), Cap >= Min,
    findall(C,user:course(C),All),
    subtract(All,Taken,Need),
    schedule(Taken,Need,Cap,Start,Plan).