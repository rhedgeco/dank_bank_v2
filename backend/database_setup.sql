create table google_oauth
(
    userid text not null
);

create unique index google_oauth_userid_uindex
    on google_oauth (userid);
