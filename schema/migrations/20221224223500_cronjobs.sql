begin;

--add sql below here
create table cronjobs (
    cronjob_id uuid primary key not null default uuid_generate_v4(),
    schedule character varying(256) not null,
    path character varying(512) not null,
    randomness numeric not null default 0,
    last_queued timestamp with time zone default null,
    last_started timestamp with time zone default null,
    last_completed timestamp with time zone default null,
    is_running boolean not null default false,
    is_queued boolean not null default false,
    is_active boolean not null default true,
    run_now boolean not null default false,
    unique(path)
);

insert into 
    cronjobs (schedule, path, randomness)
values
    ('*/1 * * * *', 'tasks.cronjobs.crawlers.bbc_gossip_column.get_bbc_gossip_column', 0);

commit;
