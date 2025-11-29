%  Prolog KB for the Ph.D. in Computer Science (PhD-CS) program

% === Required Core Courses (9 credits, min grade B) ===
required(cop5614).            % Operating Systems
required(cot5310).            % Theory of Computation I
required(cot6405).            % Analysis of Algorithms

minimum_grade(cop5614, b).
minimum_grade(cot5310, b).
minimum_grade(cot6405, b).
minimum_gpa(3.0).

% === Alternative Core (for Telecom/Networking students only)
alternative_core_track(telecom_focus, [tcn5010, tcn5030, tcn5060]).  % optional override (customizable)

% === Electives
% At least 21 credits in CIS electives
% At least 30 total credits (includes research, electives, etc.)
% Dissertation: 15 credits minimum of CIS7980, 3 per semester once in candidacy

min_cis_elective_credits(21).
min_total_credits(75).             % beyond bachelor’s
min_coursework_credits(30).        % in SCIS courses
dissertation(cis7980, 15).         % minimum required

% === Qualifying Exams and Milestones
qualifying_exam_window(start_after(credits15), deadline_within(years2)).
phd_candidacy_requirements([d1_form_approved]).
dissertation_requirements([committee_approval, oral_defense]).

% === MS en route eligibility
en_route_ms_eligibility([ms_completed, candidacy_reached, proposal_defended, d3_approved]).
no_transfer_credit_required(ms_en_route).

% === Seminar Requirement
seminar_required.

% === CIS Electives (partial list from handbook)
elective(cap5011). elective(cap5109). elective(cap5507). elective(cap5602).
elective(cap5610). elective(cap5627). elective(cap5640). elective(cap5701).
elective(cap5738). elective(cap5768). elective(cap5771). elective(cap6736).
elective(cap6776). elective(cap6778). elective(cda5655). elective(cda6939).
elective(cen5011). elective(cen5064). elective(cen5076). elective(cen5079).
elective(cen5082). elective(cen5120). elective(cen6070). elective(cen6075).
elective(cot5428). elective(cot5443). elective(cot5520). elective(cot6930).
elective(cot6931). elective(cot6936). elective(cis5208). elective(cis5346).
elective(cis5370). elective(cis5372). elective(cis5373). elective(cis5374).
elective(cis5432). elective(cis6612). elective(cis6930). elective(cis6931).
elective(cnt6207). elective(cnt6208). elective(cop5614). elective(cop5621).
elective(cop5725). elective(cop6556). elective(cop6611). elective(cop6727).
elective(cop6795). elective(cot6421). elective(cot6446). elective(tcn5080).
elective(tcn5150). elective(tcn5421). elective(tcn5440). elective(tcn5445).
elective(tcn5640). elective(tcn5710). elective(tcn6210). elective(tcn6215).
elective(tcn6230). elective(tcn6260). elective(tcn6270). elective(tcn6275).
elective(tcn6420). elective(tcn6430). elective(tcn6450). elective(tcn6820).
elective(tcn6880). elective(cnt5109). elective(cnt5415).

% === External Electives (1 allowed from this list)
non_scis_elective(eel6167). non_scis_elective(eel5500).
non_scis_elective(eel5718). non_scis_elective(eel5813).
non_scis_elective(eel5820). non_scis_elective(eel6787).
non_scis_elective(eee5348). non_scis_elective(esi6546).
non_scis_elective(sta5236). non_scis_elective(sta6807).
