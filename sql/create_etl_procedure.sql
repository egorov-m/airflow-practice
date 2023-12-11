create or replace procedure insertion_main_dimensions()
language plpgsql
as $$
begin
    insert into analytical.branch_location
    select * from location l
    on conflict (id)
    do nothing;

    insert into analytical.department (id, name)
    select d.id, d.name from department d
    on conflict (id)
    do nothing;

    insert into analytical.position
    select * from position p
    on conflict (id)
    do nothing;

    insert into analytical.employee (id,
                                     first_name,
                                     last_name,
                                     second_name)
    select e.id,
           e.first_name,
           e.last_name,
           e.second_name from employee e
    on conflict (id)
    do nothing;

    insert into analytical.company_branch (id,
                                           name,
                                           foundation_date)
    select cb.id,
           cb.name,
           cb.foundation_date from company_branch cb
    on conflict (id)
    do nothing;

    insert into analytical.chief (id,
                                  first_name,
                                  last_name,
                                  second_name)
    select e.id,
           e.first_name,
           e.last_name,
           e.second_name from department d
    join employee e on d.chief_id = e.id
    on conflict (id)
    do nothing;
end;
$$;

create or replace procedure etl_process()
language plpgsql
as $$
declare
    date_id bigint;
    current_timestamp_val timestamptz := current_timestamp;
begin
    call insertion_main_dimensions();

    insert into analytical.date(year,
                                semester,
                                quarter,
                                month,
                                week,
                                day,
                                hour,
                                minute)
    values (extract(year from current_timestamp_val),
            case when extract(month from current_timestamp) <= 6 then 1 else 2 end,
            extract(quarter from current_timestamp_val),
            extract(month from current_timestamp_val),
            extract(week from current_timestamp_val),
            extract(day from current_timestamp_val),
            extract(hour from current_timestamp_val),
            extract(minute from current_timestamp_val))
    returning id into date_id;

    insert into analytical.seniority(count_minutes_in_position,
                                     salary,
                                     employee_id,
                                     position_id,
                                     company_branch_id,
                                     branch_location_id,
                                     department_id,
                                     chief_id,
                                     date_id)
    select count_minutes_in_position,
           salary,
           employee_id,
           position_id,
           company_branch_id,
           location_id,
           department_id,
           chief_id,
           date_id
    from (select (extract(epoch from current_timestamp - max(pr.date)) / 60)::integer count_minutes_in_position,
                 pr.salary,
                 pr.employee_id,
                 e.position_id,
                 pr.company_branch_id,
                 cb.location_id,
                 pr.department_id,
                 d.chief_id,
                 pr.date,
                 dense_rank() over (
                     partition by pr.employee_id
                     order by pr.date desc
                     ) rank
          from personnel_records pr
              join employee e on pr.employee_id = e.id
              join company_branch cb on pr.company_branch_id = cb.id
              join department d on pr.department_id = d.id
          group by pr.employee_id,
                   pr.date,
                   pr.company_branch_id,
                   cb.location_id,
                   pr.department_id,
                   d.chief_id,
                   e.position_id,
                   pr.salary
          ) subquery
    where rank = 1;
end;
$$;
