SELECT jp.job_title, cj.similarity_score
FROM Course_Job cj
JOIN Job_Postings jp ON cj.job_id = jp.job_id
WHERE cj.course_id = %s
ORDER BY cj.similarity_score DESC;