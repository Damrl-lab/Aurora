%  Prolog KB for the M.S. in Information Technology (MS-IT) program

% === Required Core Courses (9 credits, min grade C) ===
required(cen5087).        % Software and Data Modeling
required(cis5372).        % Fundamentals of Computer Security
required(cis5027).        % Computer Systems Fundamentals

minimum_grade(cen5087, c).
minimum_grade(cis5372, c).
minimum_grade(cis5027, c).
minimum_gpa(3.0).

% === Focus Areas (6 credits: pick 2 from one area) ===

focus_area(security, [
    cis5373, cis5374, eel6787, tcn5080
]).

focus_area(software, [
    cen5011, cen5064, cen6075, cen6070, cen5076,
    cis6612, cop5725
]).

focus_area(sys_admin, [
    cis5346, cis5432, cen5011, cop5614, cop6611
]).

focus_area(networks, [
    tcn5030, tcn6260, tcn6270, tcn6430
]).

% === General Electives (15 credits) ===
% - Up to 3 credits of independent study (cis5900 or cis5910)
% - Up to 3 credits from approved external electives (section 7.2)

max_independent_study(3).
max_non_scis_electives(3).

% === SCIS Electives (subset from handbook) ===
elective(cap5011).  elective(cap5109).  elective(cap5507).
elective(cap5510c). elective(cap5602).  elective(cap5610).
elective(cap5627).  elective(cap5640).  elective(cap5701).
elective(cap5738).  elective(cap5768).  elective(cap5771).
elective(cap6736).  elective(cap6776).  elective(cap6778).
elective(cda5655).  elective(cda6939).  elective(cen5064).
elective(cen5076).  elective(cen5079).  elective(cen5082).
elective(cen5120).  elective(cen6070).  elective(cen6075).
elective(cot5428).  elective(cot5520).  elective(cot5407).
elective(cot6421).  elective(cot6446).  elective(cot6930).
elective(cot6931).  elective(cot6936).  elective(cis5208).
elective(cis5346).  elective(cis5370).  elective(cis5373).
elective(cis5374).  elective(cis5432).  elective(cis6612).
elective(cis6930).  elective(cis6931).  elective(cgs6834).
elective(cnt5109).  elective(cnt6207).  elective(cnt6208).
elective(cop5614).  elective(cop5621).  elective(cop5725).
elective(cop6556).  elective(cop6611).  elective(cop6727).
elective(cop6795).  elective(tcn5010).  elective(tcn5030).
elective(tcn5060).  elective(tcn5080).  elective(tcn5150).
elective(tcn5421).  elective(tcn5440).  elective(tcn5445).
elective(tcn5455).  elective(tcn5640).  elective(tcn5710).
elective(tcn6210).  elective(tcn6215).  elective(tcn6230).
elective(tcn6260).  elective(tcn6270).  elective(tcn6275).
elective(tcn6420).  elective(tcn6430).  elective(tcn6450).
elective(tcn6820).  elective(tcn6880).

% === External Electives Allowed (max 1 course) ===
non_scis_elective(eel6167). non_scis_elective(eel5500).
non_scis_elective(eel5718). non_scis_elective(eel5813).
non_scis_elective(eel5820). non_scis_elective(eel6787).
non_scis_elective(eee5348). non_scis_elective(esi6546).
non_scis_elective(sta5236). non_scis_elective(sta6807).
