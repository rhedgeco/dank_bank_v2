create table if not exists google_oauth
(
    userid text not null
);

create unique index if not exists google_oauth_userid_uindex
    on google_oauth (userid);
