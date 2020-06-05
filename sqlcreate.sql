do $$ begin
    if not exists(select * from pg_shadow where usename='newuser') then
        CREATE USER newuser WITH PASSWORD '123';
    end if;
end $$;

do $$ begin
	if not exists(select * from pg_database where datname='lababase') then
		CREATE DATABASE lababase WITH OWNER newuser
			ENCODING='UTF8'
			LC_COLLATE='English_United States.1251'
			LC_CTYPE='English_United States.1251';
	end if;
end $$;