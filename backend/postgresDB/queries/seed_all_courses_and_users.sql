INSERT INTO public.courses (course_id, course_title, credits, department, level)
VALUES
    -- Core
('MAC_2311', 'Calculus I', 4, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAC_2312', 'Calculus II', 4, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('STA_3033', 'Probability & Statistics', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_2210', 'Programming I', 4, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_3337', 'Programming II', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_3530', 'Data Structures', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4338', 'Systems Programming', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CDA_3102', 'Computer Architecture', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4555', 'Programming Languages', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4610', 'Operating Systems', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CNT_4713', 'Net-Centric Computing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CEN_4010', 'Software Engineering I', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CIS_3950', 'Capstone I', 1, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CIS_4951', 'Capstone II', 2, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CGS_1920', 'Intro to Computing', 1, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('ENC_3249', 'Professional & Technical Writing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CGS_3095', 'Technology in the Global Arena', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAD_2104', 'Discrete Math', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_3100', 'Discrete Structures', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
-- Core (see CS-BS above for cross-listed)
('MAC_1147', 'Pre-Calculus Algebra & Trigonometry', 4, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4506', 'Intro to Game Theory', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4534', 'Algorithm Techniques', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_3510', 'Applied Linear Structures', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_3541', 'Logic for CS', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_4521', 'Intro to Computational Geometry', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_4601', 'Fundamentals of Quantum Computing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAD_3301', 'Graph Theory', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAD_3401', 'Numerical Analysis', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAD_3512', 'Theory of Algorithms', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MAD_4203', 'Combinatorics', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('MHF_4302', 'Math Logic', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4453', 'Robot Vision', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CDA_4625', 'Intro to Mobile Robotics', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CEN_4083', 'Cloud Computing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CIS_4203', 'Digital Forensics', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CIS_4731', 'Fund Blockchain Technologies', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4520', 'Intro to Parallel Computing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4604', 'Advanced UNIX Programming', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4710', 'Database Management', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4751', 'Advanced Database Management', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CTS_4408', 'Database Administration', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COT_4431', 'Applied Parallel Computing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4052', 'Game Design & Development', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4104', 'Human Computer Interaction', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4612', 'Introduction to Machine Learning', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4630', 'Artificial Intelligence', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4641', 'Natural Language Processing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4710', 'Computer Graphics', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4770', 'Intro to Data Mining', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CAP_4830', 'Modeling & Simulations', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CEN_4021', 'Software Engineering II', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('CEN_4072', 'Software Testing', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4226', 'Advanced Windows Programming', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG'),
('COP_4655', 'Mobile App Development', 3, 'Knight Foundation School of Computing and Information Sciences', 'UG')
ON CONFLICT (course_id) DO NOTHING;

INSERT INTO public.program_course (program_id, course_id, is_core, recommended_year)
VALUES
-- Cores
('CS-BS', 'MAC_2311', true, 1),
('CS-BS', 'MAC_2312', true, 1),
('CS-BS', 'STA_3033', true, 2),
('CS-BS', 'COP_2210', true, 1),
('CS-BS', 'COP_3337', true, 1),
('CS-BS', 'COP_3530', true, 2),
('CS-BS','COP_4338', true, 2),
('CS-BS','CDA_3102', true, 2),
('CS-BS','COP_4555', true, 3),
('CS-BS','COP_4610', true, 3),
('CS-BS','CNT_4713', true, 3),
('CS-BS','CEN_4010', true, 3),
('CS-BS','CIS_3950', true, 4),
('CS-BS','CIS_4951', true, 4),
('CS-BS','CGS_1920', true, 1),
('CS-BS','ENC_3249', true, 2),
('CS-BS','CGS_3095', true, 2),
('CS-BS','MAD_2104', true, 1),
('CS-BS','COT_3100', true, 1),
-- Electives (all below, is_core = false)
('CS-BS', 'CAP_4506', false, 3),
('CS-BS', 'COP_4534', false, 3),
-- ... (all other elective codes, is_core=false)
('CS-BS', 'COP_4655', false, 4)
ON CONFLICT (program_id, course_id) DO NOTHING;


INSERT INTO public.program_course (program_id, course_id, is_core, recommended_year)
VALUES
('CS-MINOR', 'MAC_1147', true, 1),
('CS-MINOR', 'COP_2210', true, 1),
('CS-MINOR', 'COP_3337', true, 2),
('CS-MINOR', 'MAD_2104', true, 2),
('CS-MINOR', 'COT_3100', true, 2),
('CS-MINOR', 'CDA_3102', true, 2),
-- Electives (all electives from minor sheet)
('CS-MINOR', 'COP_4555', false, 2),
('CS-MINOR', 'CAP_4104', false, 2),
-- ... (all other minor electives)
('CS-MINOR', 'COP_4655', false, 2)
ON CONFLICT (program_id, course_id) DO NOTHING;


-- ======================
-- 1. Add two users to users_students
-- ======================
INSERT INTO public.users_students (user_id, first_name, last_name, email, status, career_interest, password_hash)
VALUES
    (6362138, 'Abigail', 'Ryoou', 'aryoo123@fiu.edu', 'active', NULL, NULL),
    (6304012, 'Iba', 'Setareh', 'isetar123@fiu.edu', 'active', NULL, NULL)
ON CONFLICT (user_id) DO NOTHING;

-- ======================
-- 2. Add their current program
-- ======================
INSERT INTO public.user_program (user_id, program_id, start_date, end_date, status)
VALUES
    (6362138, 'CS-BS', '2024-08-21', NULL, 'active'),
    (6304012, 'CS-MINOR', '2024-08-21', NULL, 'active')
ON CONFLICT (user_id, program_id) DO NOTHING;

-- ======================
-- 3. Add their courses (from your earlier "Courses Taken")
--      Set status='completed', grade='A'/'B', semester_taken=NULL or the real value if you have it.
-- ======================
INSERT INTO public.user_course (user_id, course_id, semester_taken, grade, status)
VALUES
-- Abigail Ryoou (CS-BS)
(6362138, 'MAC_2311', NULL, 'A', 'completed'),
(6362138, 'COP_2210', NULL, 'A', 'completed'),
(6362138, 'MAC_2312', NULL, 'A', 'completed'),
(6362138, 'STA_3033', NULL, 'A', 'completed'),
(6362138, 'COP_3337', NULL, 'A', 'completed'),
(6362138, 'MAD_2104', NULL, 'A', 'completed'),
(6362138, 'CDA_3102', NULL, 'A', 'completed'),
(6362138, 'ENC_3249', NULL, 'A', 'completed'),
(6362138, 'CGS_3095', NULL, 'A', 'completed'),
(6362138, 'COP_3530', NULL, 'A', 'completed'),
(6362138, 'COP_4338', NULL, 'B', 'completed'),
(6362138, 'CEN_4010', NULL, 'A', 'completed'),
(6362138, 'CAP_4506', NULL, 'A', 'completed'),

-- Iba Setareh (CS-MINOR)
(6304012, 'MAC_1147', NULL, 'B', 'completed'),
(6304012, 'COP_2210', NULL, 'A', 'completed'),
(6304012, 'COP_3337', NULL, 'A', 'completed')
ON CONFLICT (user_id, course_id) DO NOTHING;
