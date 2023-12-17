create schema if not exists analytical;

create table if not exists analytical.branch_location (
    id bigint not null
        primary key,
    country varchar(100) not null ,
    city varchar(100) not null,
    region varchar(100),
    street_address varchar(100) not null,
    latitude double precision not null ,
    longitude double precision not null
);

create table if not exists analytical.department (
    id bigint not null
        primary key,
    name varchar(100) not null
);

create table if not exists analytical.position (
    id bigint not null
        primary key,
    name varchar(100) not null,
    description varchar(400)
);

create table if not exists analytical.employee (
    id bigint not null
        primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    second_name varchar(100)
);

create table if not exists analytical.company_branch (
    id bigint not null
        primary key,
    name varchar(100) not null,
    foundation_date timestamptz not null
);

create table if not exists analytical.chief (
    id bigint not null
        primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    second_name varchar(100)
);

create table if not exists analytical.date (
    id bigint generated always as identity
        constraint analytical_date_pk
            primary key,
    year smallint not null,
    semester smallint not null,
    quarter smallint not null,
    month smallint not null,
    week smallint not null,
    day smallint not null,
    hour smallint not null,
    minute smallint not null
);

create table if not exists analytical.seniority (
    count_minutes_in_position smallint not null,
    salary double precision not null,

    employee_id bigint not null
        constraint seniority_employee_id_fk
            references analytical.employee,

    position_id bigint not null
        constraint seniority_position_id_fk
            references analytical.position,

    company_branch_id bigint not null
        constraint seniority_company_branch_id_fk
            references analytical.company_branch,

    branch_location_id bigint not null
        constraint seniority_branch_location_id_fk
            references analytical.branch_location,

    department_id bigint not null
        constraint seniority_department_id_fk
            references analytical.department,

    chief_id bigint not null
        constraint seniority_chief_id_fk
            references analytical.chief,

    date_id bigint not null
        constraint seniority_date_id_fk
            references analytical.date
);
