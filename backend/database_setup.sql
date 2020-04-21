create table if not exists groups
(
    id   int not null
        constraint groups_pk
            primary key,
    name text
);

create unique index groups_id_uindex
    on groups (id);

create table if not exists users
(
    userid          text not null,
    session_id      text,
    session_timeout text
);

create unique index google_oauth_userid_uindex
    on users (userid);

create table if not exists users_groups
(
    user_id  text,
    group_id int
);