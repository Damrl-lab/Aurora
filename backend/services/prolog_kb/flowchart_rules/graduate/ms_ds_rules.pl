% Prolog KB for the M.S. in Data Science / Artificial Intelligence (MS-DS/AI)

% === Required Core Courses (12 credits, min grade C) ===
required(cap5602).           % Intro to Artificial Intelligence
required(cap5768).           % Intro to Data Science
required(cap5771).           % Principles of Data Mining
required(sta6244).           % Data Analysis I

% Alternate core options
alternate(cap5771, cop5577).        % Principles of Data Mining OR COP5577
alternate(sta6244, qmb6357).        % Business Stat Analysis
alternate(sta6244, qmb6315).        % Quantitative Analytical Methods
alternate(sta6244, phc6052).        % Biostatistics I

minimum_grade(cap5602, c).
minimum_grade(cap5768, c).
minimum_grade(cap5771, c).
minimum_grade(sta6244, c).
minimum_gpa(3.0).

% === Capstone (3 credits, pick 1) ===
capstone(idc6940).                  % Core Capstone Course in Data Science
alternate_capstone(idc6940, ism6930).
alternate_capstone(idc6940, ism6307).

% === Specialization Tracks: pick 5 courses (15 credits) ===

% Artificial Intelligence Track
ai_track([
    cap5109, cap5507, cap5510c, cap5627, cap5640,
    cap5610, cap6619, cen5120, eel5820, eel5813, sta6247
]).

% Computational Data Analytics Track
cda_track([
    cap5109, cap5510c, cap5610, cap5640, cap5738,
    cap6776, cap6778, cen5082, cis5372, cis5374,
    cis6931, cop5725, cop6727, cot6405, cot6936,
    tcn6420, eel6803, sta6247, sta6636, eel5820, eel5813
]).

% Public Policy Analytics Track
ppa_track([
    pad6306, pad6053, pad5256, pup6006, pad6434, sta6247
]).

% Business Data Analytics Track
bda_track([
    ism6136, ism6642, ism6205, cop5725, ism6208,
    ism6404, ism6418, cap5738, sta6247, cap6778,
    cop6727, sta6636, cap5610, cap5622
]).

% Biostatistics Track
bio_track([
    phc6056, phc6059, phc6064, phc6067, phc6080,
    phc6099, phc7083, phc7719, phc6091
]).

% === Notes ===
% All tracks require 5 courses from the respective list
% sta6247 appears in several tracks and can be reused if applicable
