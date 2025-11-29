import os
import glob
import pandas as pd

BASE_PATH = r"D:\Research\DaRML\Actual Project\Course-Job-Fit"

# Code to join all jobs to test RAG setup but not really needed 

# Pattern to match all job files ending with "_jobs.xlsx"
job_files_pattern = os.path.join(BASE_PATH, "Cleaned Dataset", "*_jobs.xlsx")

# Collecting file paths in a list
job_files = glob.glob(job_files_pattern)

# Combining
df_jobs_list = []
for job_file in job_files:
    df_temp = pd.read_excel(job_file)
    df_jobs_list.append(df_temp)

df_jobs = pd.concat(df_jobs_list, ignore_index=True)

print("Merged Job DataFrame shape:", df_jobs.shape)
print(df_jobs.head())
