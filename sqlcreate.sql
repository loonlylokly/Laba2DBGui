CREATE EXTENSION IF NOT EXISTS dblink ;

do $$ begin
    if not exists(select * from pg_shadow where usename='newuser') then
        CREATE USER newuser WITH PASSWORD '123';
    end if;
end $$;


CREATE OR REPLACE FUNCTION createDB()
RETURNS void AS $$ begin
    if not exists(select * from pg_database where datname='lababase') then
        perform   dblink_exec('dbname=' || 'postgres' || ' user=' || "current_user"() || ' password=' || 'root',
                'create database ' || quote_ident('lababase') ||
                ' with owner ' || quote_ident('newuser'));
    end if;
end; $$
language plpgsql;

CREATE OR REPLACE FUNCTION dropDB()
  RETURNS void AS
$$ begin
	if exists(select * from pg_database where datname='lababase') then
		perform  dblink_exec('dbname=' || 'postgres' || ' user=' || "current_user"() || ' password=' || 'root',
					'drop database ' || quote_ident('lababase'));
	end if;
end; $$
language plpgsql;