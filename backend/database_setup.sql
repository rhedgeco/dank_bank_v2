create table
if not exists groups
(
    group_id text not null,
    name    text
);

create unique index groups_group_id_uindex
    on groups (group_id);

create table
if not exists users
(
    user_id          text not null,
    nickname        text,
    session_id      text,
    session_timeout text,
    photo           text
);

create unique index google_oauth_user_id_uindex
    on users (user_id);

create table
if not exists users_groups
(
    user_id  text,
    group_id text
);

create table
if not exists transactions
(
    trans_id     text not null,
    group_id     text not null,
    user_pay    text not null,
    users_paid  text not null,
    amount      text not null,
    description text
);

create unique index transactions_trans_id_uindex
    on transactions (trans_id);