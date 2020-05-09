create table if not exists groups
(
    groupid text not null,
    name    text
);

create unique index groups_groupid_uindex
    on groups (groupid);

create table if not exists users
(
    userid          text not null,
    nickname        text,
    session_id      text,
    session_timeout text
);

create unique index google_oauth_userid_uindex
    on users (userid);

create table if not exists users_groups
(
    user_id  text,
    group_id text
);

create table if not exists transactions
(
    transid     text not null,
    user_pay    text not null,
    users_paid  text not null,
    amount      text not null,
    description text
);

create unique index transactions_transid_uindex
    on transactions (transid);