create table if not exists users(
      id integer primary key autoincrement,
      username text not null unique,
      password text not null
);
