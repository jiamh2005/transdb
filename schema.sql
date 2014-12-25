drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists translations;
create table translations (
  id integer primary key autoincrement,
  area text not null,
  english text not null,
  chinese text not null
);