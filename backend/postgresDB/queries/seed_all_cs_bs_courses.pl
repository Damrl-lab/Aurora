BEGIN;

-- ───────────────────────────────────────────────────
-- 1) seed every CS-BS course into `courses`
-- ───────────────────────────────────────────────────
INSERT INTO courses(course_id, course_title, course_description, credits) VALUES
-- Core Math & Stats
('MAC_2311', 'Calculus I',             'Differential and integral calculus of one variable',         4),
('MAC_2312', 'Calculus II',            'Techniques and applications of integration; infinite series', 4),
('STA_3033', 'Probability & Statistics','Introduction to probability theory and statistical inference',3),

-- Core Computing Fundamentals
('COP_2210', 'Programming I',          'Introduction to programming concepts',                       4),
('CGS_1920', 'Introduction To Computing','Overview of computing fundamentals',                        1),
('ENC_3249', 'Professional & Technical Writing','Writing for technical audiences',                   3),
('ENC_3213', 'Professional & Technical Writing','Writing for technical audiences',                   3),

-- Core Discrete
('MAD_2104', 'Discrete Math',          'Sets, logic, proofs, graphs and basic combinatorics',        3),
('COT_3100', 'Discrete Structures',    'Discrete structures in computing; formal proofs',            3),

-- Core CS Sequence
('COP_3337', 'Programming II',         'Object-oriented programming and advanced data types',        3),
('CDA_3102', 'Computer Architecture',  'Structure and operation of computer systems',               3),
('COP_4338', 'Systems Programming',    'Low-level programming & OS interfaces',                     3),
('COP_3530', 'Data Structures',        'Data storage, algorithms, complexity analysis',             3),
('CIS_3950', 'Capstone I',             'Capstone project I (junior standing)',                      1),
('CEN_4010', 'Software Engineering I', 'Software development life-cycle & methodologies',            3),
('CGS_3095', 'Technology in the Global Arena','Global impacts of computing tech',                  3),
('COP_4610', 'Operating Systems',      'Design & implementation of operating systems',               3),
('CNT_4713', 'Net Centric Computing',  'Networking and distributed systems',                         3),
('COP_4555', 'Programming Languages',  'Study of programming language paradigms',                    3),
('CIS_4951', 'Capstone II',            'Capstone project II (senior standing)',                      2),

-- CS Electives: Foundations
('CAP_4506', 'Intro to Game Theory',            'Game theory and strategic decision making',             3),
('COP_4534', 'Algorithm Techniques',           'Design and analysis of advanced algorithms',            3),
('COT_3510', 'Applied Linear Structures',      'Linear algebraic structures with CS applications',      3),
('COT_3541', 'Logic for CS',                   'Logic principles and formal proof techniques',         3),
('COT_4521', 'Intro to Computational Geometry','Geometric algorithms & data structures',               3),
('COT_4601', 'Quantum Computing Fundamentals','Principles of quantum computing',                      3),
('MAD_3301', 'Graph Theory',                   'Graph models, algorithms, and applications',            3),
('MAD_3401', 'Numerical Analysis',             'Computational methods for numerical problems',          3),
('MAD_3512', 'Theory of Algorithms',           'Theoretical foundations of algorithm design',           3),
('MAD_4203', 'Combinatorics',                  'Counting, enumeration, combinatorial designs',         3),
('MHF_4302', 'Math Logic',                     'Mathematical logic and formal reasoning',               3),

-- CS Electives: Systems
('CAP_4453', 'Robot Vision',               'Computer vision techniques for robotics',                3),
('CDA_4625', 'Intro to Mobile Robotics',   'Foundations of mobile robotic systems',                  3),
('CEN_4083', 'Cloud Computing',            'Principles & architectures of cloud systems',            3),
('CIS_4203', 'Digital Forensics',          'Techniques for digital forensic analysis',               3),
('CIS_4731', 'Fund Blockchain Technologies','Blockchain systems & applications',                     3),
('COP_4520', 'Intro to Parallel Computing', 'Parallel architectures & programming models',            3),
('COP_4604', 'Advanced UNIX Programming',   'UNIX system programming & shell scripting',              3),
('COP_4710', 'Database Management',        'Database design & SQL (Coreq: COP_3530)',                3),
('COP_4751', 'Advanced Database Management','Advanced topics in database administration',            3),
('CTS_4408', 'Database Administration',    'Database administration practices & tools',             3),
('COT_4431', 'Applied Parallel Computing', 'Applied parallel programming paradigms',                 3),

-- CS Electives: Applications
('CAP_4052', 'Game Design & Dev',            'Game design and development principles',              3),
('CAP_4104', 'Human Computer Interaction',    'Design and evaluation of user interfaces',             3),
('CAP_4612', 'Introduction to Machine Learning','Machine learning algorithms & applications',       3),
('CAP_4630', 'Artificial Intelligence',      'Fundamentals of AI techniques',                        3),
('CAP_4641', 'Natural Language Processing',  'Techniques for processing & understanding language',   3),
('CAP_4710', 'Computer Graphics',            'Computer graphics and visualization',                  3),
('CAP_4770', 'Intro to Data Mining',         'Data mining techniques & applications',                3),
('CAP_4830', 'Modeling & Simulations',       'Modeling & simulation of dynamic systems',             3),
('CEN_4021', 'Software Engineering II',      'Advanced software engineering practices',              3),
('CEN_4072', 'Software Testing',             'Software QA and testing methodologies',                3),
('COP_4226', 'Advanced Windows Programming', 'Windows application development',                       3),
('COP_4655', 'Mobile App Development',       'Mobile application development for smartphones',       3);

-- ───────────────────────────────────────────────────
-- 2) link them all to the CS-BS program
-- ───────────────────────────────────────────────────
INSERT INTO program_course(program_id, course_id) VALUES
-- Core
('CS-BS','MAC_2311'),('CS-BS','MAC_2312'),('CS-BS','STA_3033'),
('CS-BS','COP_2210'),('CS-BS','CGS_1920'),('CS-BS','ENC_3249'),
('CS-BS','ENC_3213'),('CS-BS','MAD_2104'),('CS-BS','COT_3100'),
('CS-BS','COP_3337'),('CS-BS','CDA_3102'),('CS-BS','COP_4338'),
('CS-BS','COP_3530'),('CS-BS','CIS_3950'),('CS-BS','CEN_4010'),
('CS-BS','CGS_3095'),('CS-BS','COP_4610'),('CS-BS','CNT_4713'),
('CS-BS','COP_4555'),('CS-BS','CIS_4951'),
-- Electives
('CS-BS','CAP_4506'),('CS-BS','COP_4534'),('CS-BS','COT_3510'),
('CS-BS','COT_3541'),('CS-BS','COT_4521'),('CS-BS','COT_4601'),
('CS-BS','MAD_3301'),('CS-BS','MAD_3401'),('CS-BS','MAD_3512'),
('CS-BS','MAD_4203'),('CS-BS','MHF_4302'),('CS-BS','CAP_4453'),
('CS-BS','CDA_4625'),('CS-BS','CEN_4083'),('CS-BS','CIS_4203'),
('CS-BS','CIS_4731'),('CS-BS','COP_4520'),('CS-BS','COP_4604'),
('CS-BS','COP_4710'),('CS-BS','COP_4751'),('CS-BS','CTS_4408'),
('CS-BS','COT_4431'),('CS-BS','CAP_4052'),('CS-BS','CAP_4104'),
('CS-BS','CAP_4612'),('CS-BS','CAP_4630'),('CS-BS','CAP_4641'),
('CS-BS','CAP_4710'),('CS-BS','CAP_4770'),('CS-BS','CAP_4830'),
('CS-BS','CEN_4021'),('CS-BS','CEN_4072'),('CS-BS','COP_4226'),
('CS-BS','COP_4655');

COMMIT;
