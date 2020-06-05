create or replace function createTables ()
returns void as $$ begin
	if not exists(select * from information_schema.tables where table_schema = 'public' and  table_name='usertable') then
    	CREATE TABLE usertable(
        	phone bigint PRIMARY KEY		not null,
	        username		char(50)	not null,
			address		char(50)	not null,
			idTarif		int			not null);
    end if;

	if not exists(select * from information_schema.tables where table_schema = 'public' and  table_name='tariftable') then
    	CREATE TABLE tariftable(
        	id int PRIMARY KEY		not null,
	        tarif		char(50)	not null,
        	price		int			not null,
			countUsers	int			);
    end if;
end; $$
language plpgsql;


create or replace function insertUser (arg1 bigint, arg2 char(50), arg3 char(50), arg4 int)
returns void as $$ begin
	if not exists(select * from usertable where phone = arg1) then
		INSERT INTO usertable VALUES(arg1, arg2, arg3, arg4);
	end if;
end; $$
language plpgsql;

create or replace function insertTarif (arg1 int, arg2 char(50), arg3 int)
returns void as $$ begin
	if not exists(select * from tariftable where id = arg1) then
		INSERT INTO tariftable VALUES(arg1, arg2, arg3);
	end if;
end; $$
language plpgsql;


create or replace function selectUsers (arg char(50))
returns table (arg1 bigint, arg2 char(50), arg3 char(50), arg4 int)
as $$ begin
	return query select * from usertable where username = arg;
end; $$
language plpgsql;


create or replace function selectTarifs (arg char(50))
returns table (arg1 int, arg2 char(50), arg3 int, arg4 int)
as $$ begin
	return query select * from tariftable where tarif = arg;
end; $$
language plpgsql;


create or replace function deleteFromUsertable (arg varchar(20))
returns void as $$ begin
	if exists(select * from usertable where username = arg) then
		DELETE FROM usertable WHERE username = arg;
	end if;
end; $$
language plpgsql;


create or replace function deleteFromTarifTable (arg varchar(20))
returns void as $$ begin
	if exists(select * from tariftable where tarif = arg) then
		DELETE FROM tariftable WHERE tarif = arg;
	end if;
end; $$
language plpgsql;


create or replace function cleanUsertable ()
returns void as $$ begin
	if exists(select * from information_schema.tables where table_schema = 'public' and  table_name='usertable') then
		DELETE FROM usertable;
	end if;
end; $$
language plpgsql;


create or replace function cleanTarifTable ()
returns void as $$ begin
	if exists(select * from information_schema.tables where table_schema = 'public' and  table_name='tariftable') then
		DELETE FROM tariftable;
	end if;
end; $$
language plpgsql;


create or replace function cleanAllTables ()
returns void as $$ begin
	if exists(select * from information_schema.tables where table_schema = 'public' and  table_name='usertable') then
		DELETE FROM usertable;
	end if;

	if exists(select * from information_schema.tables where table_schema = 'public' and  table_name='tariftable') then
		DELETE FROM tariftable;
	end if;
end; $$
language plpgsql;


create or replace function setIndex ()
returns void as $$ begin
	if not exists(SELECT * FROM pg_indexes WHERE tablename = 'tariftable') then
		create index countindex on tariftable(countusers);
	end if;
end; $$
language plpgsql;


create or replace function selectAllUsers ()
returns table (arg1 bigint, arg2 char(50), arg3 char(50), arg4 int)
as $$ begin
	return query select * from usertable;
end; $$
language plpgsql;


create or replace function selectAllTarifs ()
returns table (arg1 int, arg2 char(50), arg3 int, arg4 int)
as $$ begin
	return query select * from tariftable;
end; $$
language plpgsql;
