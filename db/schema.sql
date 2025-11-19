CREATE DATABASE IF NOT EXISTS irelis_db;

\c irelis_db;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role_enum') THEN CREATE TYPE user_role_enum AS ENUM ('CANDIDATE', 'RECRUITER', 'ADMIN'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'candidate_mobility_enum') THEN CREATE TYPE candidate_mobility_enum AS ENUM ('ON_SITE', 'REMOTE', 'HYBRID'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'notification_delay_enum') THEN CREATE TYPE notification_delay_enum AS ENUM ('DAY', 'WEEK', 'MONTH'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'recommendation_target_enum') THEN CREATE TYPE recommendation_target_enum AS ENUM ('CANDIDATE', 'RECRUITER'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'search_type_enum') THEN CREATE TYPE search_type_enum AS ENUM ('BOOLEAN', 'DEFAULT'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'search_target_enum') THEN CREATE TYPE search_target_enum AS ENUM ('OFFER', 'CANDIDATE'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'search_contract_enum') THEN CREATE TYPE search_contract_enum AS ENUM ('CDI', 'CDD', 'STAGE', 'FREELANCE', 'ALTERNANCE', 'OTHER'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'desired_position_type_enum') THEN CREATE TYPE desired_position_type_enum AS ENUM ('CDI', 'CDD', 'STAGE', 'FREELANCE', 'ALTERNANCE', 'OTHER'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'desired_position_level_enum') THEN CREATE TYPE desired_position_level_enum AS ENUM ('JUNIOR', 'SENIOR'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'language_level_enum') THEN CREATE TYPE language_level_enum AS ENUM ('A1', 'A2', 'B1', 'B2', 'C1', 'C2'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_mobility_enum') THEN CREATE TYPE offer_mobility_enum AS ENUM ('ON_SITE', 'REMOTE', 'HYBRID'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_position_type_enum') THEN CREATE TYPE offer_position_type_enum AS ENUM ('CDI', 'CDD', 'STAGE', 'FREELANCE', 'ALTERNANCE', 'OTHER'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_seniority_enum') THEN CREATE TYPE offer_seniority_enum AS ENUM ('JUNIOR', 'SENIOR'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_salary_type_enum') THEN CREATE TYPE offer_salary_type_enum AS ENUM ('AVERAGE', 'MIN', 'MAX', 'INTERVAL'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_instance_mobility_enum') THEN CREATE TYPE offer_instance_mobility_enum AS ENUM ('ON_SITE', 'REMOTE', 'HYBRID'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_instance_position_type_enum') THEN CREATE TYPE offer_instance_position_type_enum AS ENUM ('CDI', 'CDD', 'STAGE', 'FREELANCE', 'ALTERNANCE', 'OTHER'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_instance_seniority_enum') THEN CREATE TYPE offer_instance_seniority_enum AS ENUM ('JUNIOR', 'SENIOR'); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'offer_instance_salary_type_enum') THEN CREATE TYPE offer_instance_salary_type_enum AS ENUM ('AVERAGE', 'MIN', 'MAX', 'INTERVAL'); END IF; END $$;


CREATE TABLE users (
	id UUID NOT NULL, 
	first_name VARCHAR(150) NOT NULL, 
	last_name VARCHAR(150) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	phone VARCHAR(50), 
	role user_role_enum NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id)
)

;


CREATE TABLE candidates (
	id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	mobility candidate_mobility_enum, 
	country VARCHAR(150), 
	city VARCHAR(150), 
	town VARCHAR(150), 
	address VARCHAR(255), 
	salary_min NUMERIC(12, 2), 
	salary_avg NUMERIC(12, 2), 
	salary_max NUMERIC(12, 2), 
	notification_delay notification_delay_enum, 
	notification_enabled BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE chat_sessions (
	id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	other_user_id UUID, 
	token VARCHAR(255) NOT NULL, 
	bot BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(other_user_id) REFERENCES users (id), 
	UNIQUE (token)
)

;


CREATE TABLE recommendations (
	id UUID NOT NULL, 
	label VARCHAR(255) NOT NULL, 
	target recommendation_target_enum NOT NULL, 
	user_id UUID NOT NULL, 
	number INTEGER NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE recruiters (
	id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	organization_name VARCHAR(255) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE searches (
	id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	query VARCHAR(255), 
	type search_type_enum NOT NULL, 
	target search_target_enum NOT NULL, 
	country VARCHAR(150), 
	city VARCHAR(150), 
	town VARCHAR(150), 
	contract_type search_contract_enum, 
	education_level VARCHAR(150), 
	experience VARCHAR(150), 
	language VARCHAR(150), 
	date_publication TIMESTAMP WITH TIME ZONE, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;


CREATE TABLE candidate_skills (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE desired_position_types (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	type desired_position_type_enum NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE desired_positions (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	level desired_position_level_enum, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE educations (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	school VARCHAR(255), 
	description TEXT, 
	start_date DATE, 
	end_date DATE, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE experiences (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	company VARCHAR(255), 
	description TEXT, 
	start_date DATE, 
	end_date DATE, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE languages (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	level language_level_enum, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE messages (
	id UUID NOT NULL, 
	session_id UUID NOT NULL, 
	sender_id UUID NOT NULL, 
	receiver_id UUID NOT NULL, 
	content TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES chat_sessions (id), 
	FOREIGN KEY(sender_id) REFERENCES users (id), 
	FOREIGN KEY(receiver_id) REFERENCES users (id)
)

;


CREATE TABLE offer_templates (
	id UUID NOT NULL, 
	recruiter_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT, 
	mobility offer_mobility_enum, 
	position_type offer_position_type_enum NOT NULL, 
	seniority offer_seniority_enum, 
	duration_months INTEGER, 
	salary_min NUMERIC(12, 2), 
	salary_max NUMERIC(12, 2), 
	salary_avg NUMERIC(12, 2), 
	salary_type offer_salary_type_enum, 
	experience_years INTEGER, 
	priority_level INTEGER, 
	country VARCHAR(150), 
	city VARCHAR(150), 
	town VARCHAR(150), 
	address VARCHAR(255), 
	language VARCHAR(150), 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	ended_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recruiter_id) REFERENCES recruiters (id)
)

;


CREATE TABLE projects (
	id UUID NOT NULL, 
	candidate_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT, 
	start_date DATE, 
	end_date DATE, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (id)
)

;


CREATE TABLE offers (
	id UUID NOT NULL, 
	template_id UUID, 
	recruiter_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	description TEXT, 
	mobility offer_instance_mobility_enum, 
	position_type offer_instance_position_type_enum NOT NULL, 
	seniority offer_instance_seniority_enum, 
	duration_months INTEGER, 
	salary_min NUMERIC(12, 2), 
	salary_max NUMERIC(12, 2), 
	salary_avg NUMERIC(12, 2), 
	salary_type offer_instance_salary_type_enum, 
	experience_years INTEGER, 
	priority_level INTEGER, 
	country VARCHAR(150), 
	city VARCHAR(150), 
	town VARCHAR(150), 
	address VARCHAR(255), 
	language VARCHAR(150), 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	ended_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(template_id) REFERENCES offer_templates (id), 
	FOREIGN KEY(recruiter_id) REFERENCES recruiters (id)
)

;


CREATE TABLE offer_skills (
	id UUID NOT NULL, 
	offer_id UUID NOT NULL, 
	title VARCHAR(255) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(offer_id) REFERENCES offers (id)
)

;