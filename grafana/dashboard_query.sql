-- Общее число должностей 

SELECT COUNT(DISTINCT id) AS total_positions
FROM analytical.position;

-- Общее кол-во работников

SELECT COUNT(*) AS total_employees_count
FROM analytical.employee;

-- Общее число компаний

SELECT COUNT(DISTINCT id) AS total_companies
FROM analytical.company_branch;

-- Персонал и время в должности

SELECT
  analytical.department.name AS Название_отдела,
  COUNT(analytical.employee.id) AS Всего_сотрудников,
  analytical.company_branch.name AS Название_филиала,
  AVG(analytical.seniority.salary) AS Средняя_зарплата,
  analytical.branch_location.city AS Город_расположения,
  SUM(analytical.seniority.count_minutes_in_position) AS среднее_время_в_должности
FROM analytical.employee
JOIN analytical.seniority ON analytical.employee.id = analytical.seniority.employee_id
JOIN analytical.department ON analytical.seniority.department_id = analytical.department.id
JOIN analytical.company_branch ON analytical.seniority.company_branch_id = analytical.company_branch.id
JOIN analytical.branch_location ON analytical.seniority.branch_location_id = analytical.branch_location.id
GROUP BY Название_отдела, Название_филиала, Город_расположения
ORDER BY Всего_сотрудников DESC, Средняя_зарплата DESC, среднее_время_в_должности DESC;

-- Продолжительностьь работы сотрудников в компании

SELECT
  analytical.department.name AS department_name,
  AVG(analytical.seniority.count_minutes_in_position) AS average_tenure
FROM analytical.seniority
JOIN analytical.department ON analytical.seniority.department_id = analytical.department.id
GROUP BY department_name
ORDER BY department_name;

-- Средняя зарплата

SELECT
  TO_TIMESTAMP(CONCAT(da.year, '-', da.month, '-', da.day, ' ', da.hour, ':', da.minute), 'YYYY-MM-DD HH24:MI') AS время,
  AVG(s.salary) AS средняя_зарплата
FROM analytical.seniority s
JOIN analytical.date da ON s.date_id = da.id
GROUP BY время
ORDER BY время;

--Среднее время

SELECT
  TO_TIMESTAMP(CONCAT(da.year, '-', da.month, '-', da.day, ' ', da.hour, ':', da.minute), 'YYYY-MM-DD HH24:MI') AS время,
  AVG(s.count_minutes_in_position) AS среднее_время_в_должности
FROM analytical.seniority s
JOIN analytical.date da ON s.date_id = da.id
GROUP BY время
ORDER BY время;

-- Средняя зарплата и время

SELECT p.name, (AVG(s.salary) - MIN(s.salary)) / (MAX(s.salary) - MIN(s.salary)) AS
    "Средняя зарплата",
    (AVG(s.count_minutes_in_position) - MIN(s.count_minutes_in_position)) / (MAX(s.count_minutes_in_position) - MIN(s.count_minutes_in_position)) AS
        "Среднее время в должности"
FROM analytical.seniority s JOIN analytical.position p on p.id = s.position_id GROUP BY p.name;

-- Средняя зарплата под должностям

SELECT
  p.name AS position,
  AVG(s.salary) AS average_salary
FROM analytical.seniority s
JOIN analytical.position p ON s.position_id = p.id
GROUP BY position
ORDER BY average_salary DESC;

-- Средняя зарплата по отделам

SELECT
  d.name AS department,
  AVG(s.salary) AS average_salary
FROM analytical.seniority s
JOIN analytical.department d ON s.department_id = d.id
GROUP BY department;

