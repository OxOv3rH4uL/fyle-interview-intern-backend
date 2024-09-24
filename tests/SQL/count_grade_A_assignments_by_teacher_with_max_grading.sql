-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS total_grade_a_count
FROM assignments
WHERE grade = 'A'
AND teacher_id = (
    SELECT teacher_id
    FROM (
        SELECT teacher_id, COUNT(*) AS num_assignments
        FROM assignments
        WHERE grade IS NOT NULL
        GROUP BY teacher_id
        ORDER BY num_assignments DESC
        LIMIT 1
    ) AS most_assignments
);
