--
-- PostgreSQL database dump
--

\restrict 7zhDMSuMbbfrD6bctrwYgumbL0PD1uy2kv39KoGph2LW2VzEqnsH5cTIRCSRwf4

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.7 (Ubuntu 17.7-3.pgdg24.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: application_status_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.application_status_enum AS ENUM (
    'ACCEPTED',
    'PENDING',
    'REJECTED',
    'REVIEWED',
    'WITHDRAWN'
);


ALTER TYPE public.application_status_enum OWNER TO irelis;

--
-- Name: candidate_experience_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.candidate_experience_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE',
    'JUNIOR',
    'SENIOR'
);


ALTER TYPE public.candidate_experience_level_enum OWNER TO irelis;

--
-- Name: candidate_school_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.candidate_school_level_enum AS ENUM (
    'BAC',
    'BTS',
    'DEUG',
    'DOCTORAL',
    'DUT',
    'LICENCE',
    'MASTER',
    'UNKNOWN'
);


ALTER TYPE public.candidate_school_level_enum OWNER TO irelis;

--
-- Name: email_otp_purpose_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.email_otp_purpose_enum AS ENUM (
    'LOGIN_REGISTER',
    'PASSWORD_RESET'
);


ALTER TYPE public.email_otp_purpose_enum OWNER TO irelis;

--
-- Name: email_otp_user_type_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.email_otp_user_type_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


ALTER TYPE public.email_otp_user_type_enum OWNER TO irelis;

--
-- Name: job_offer_contract_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_offer_contract_enum AS ENUM (
    'ALTERNATIVE',
    'CDD',
    'CDI',
    'FREELANCE',
    'INTERNSHIP'
);


ALTER TYPE public.job_offer_contract_enum OWNER TO irelis;

--
-- Name: job_offer_experience_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_offer_experience_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE',
    'JUNIOR',
    'SENIOR'
);


ALTER TYPE public.job_offer_experience_level_enum OWNER TO irelis;

--
-- Name: job_offer_school_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_offer_school_level_enum AS ENUM (
    'BAC',
    'BTS',
    'DEUG',
    'DOCTORAL',
    'DUT',
    'LICENCE',
    'MASTER',
    'UNKNOWN'
);


ALTER TYPE public.job_offer_school_level_enum OWNER TO irelis;

--
-- Name: job_offer_status_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_offer_status_enum AS ENUM (
    'CLOSED',
    'DELETED',
    'DRAFT',
    'EXPIRED',
    'PUBLISHED'
);


ALTER TYPE public.job_offer_status_enum OWNER TO irelis;

--
-- Name: job_offer_type_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_offer_type_enum AS ENUM (
    'FULL_TIME',
    'HYBRID',
    'PART_TIME',
    'REMOTE'
);


ALTER TYPE public.job_offer_type_enum OWNER TO irelis;

--
-- Name: job_preferences_contract_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.job_preferences_contract_enum AS ENUM (
    'ALTERNATIVE',
    'CDD',
    'CDI',
    'FREELANCE',
    'INTERNSHIP'
);


ALTER TYPE public.job_preferences_contract_enum OWNER TO irelis;

--
-- Name: language_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.language_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'BILINGUAL',
    'INTERMEDIATE',
    'NATIVE_LANGUAGE'
);


ALTER TYPE public.language_level_enum OWNER TO irelis;

--
-- Name: provider_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.provider_enum AS ENUM (
    'EMAIL',
    'FACEBOOK',
    'GOOGLE',
    'LINKEDIN'
);


ALTER TYPE public.provider_enum OWNER TO irelis;

--
-- Name: skill_level_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.skill_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE'
);


ALTER TYPE public.skill_level_enum OWNER TO irelis;

--
-- Name: user_role_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.user_role_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


ALTER TYPE public.user_role_enum OWNER TO irelis;

--
-- Name: user_type_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.user_type_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


ALTER TYPE public.user_type_enum OWNER TO irelis;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.applications (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    applied_at timestamp(6) without time zone,
    cover_letter character varying(255),
    resume_url character varying(255),
    status character varying(255),
    candidate_id uuid NOT NULL,
    job_offer_id uuid NOT NULL,
    CONSTRAINT applications_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'REVIEWED'::character varying, 'ACCEPTED'::character varying, 'REJECTED'::character varying, 'WITHDRAWN'::character varying])::text[])))
);


ALTER TABLE public.applications OWNER TO irelis;

--
-- Name: candidates; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.candidates (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    avatar_url character varying(255),
    birth_date timestamp(6) without time zone,
    completion_rate double precision,
    cv_url character varying(255),
    experience_level character varying(255),
    first_name character varying(255),
    is_visible boolean,
    last_name character varying(255),
    linked_in_url character varying(255),
    city character varying(255),
    country character varying(255),
    region character varying(255),
    motivation_letter_url character varying(255),
    phone_number character varying(255),
    pitch_mail character varying(2000),
    portfolio_url character varying(255),
    presentation character varying(255),
    professional_title character varying(255),
    school_level character varying(255),
    user_id uuid,
    CONSTRAINT candidates_experience_level_check CHECK (((experience_level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'JUNIOR'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'SENIOR'::character varying, 'EXPERT'::character varying])::text[]))),
    CONSTRAINT candidates_school_level_check CHECK (((school_level)::text = ANY ((ARRAY['BAC'::character varying, 'DEUG'::character varying, 'BTS'::character varying, 'DUT'::character varying, 'LICENCE'::character varying, 'MASTER'::character varying, 'DOCTORAL'::character varying, 'UNKNOWN'::character varying])::text[])))
);


ALTER TABLE public.candidates OWNER TO irelis;

--
-- Name: education; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.education (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    city character varying(255),
    degree character varying(255),
    graduation_year integer,
    institution character varying(255),
    candidate_id uuid NOT NULL
);


ALTER TABLE public.education OWNER TO irelis;

--
-- Name: email_otp; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.email_otp (
    id bigint NOT NULL,
    code character varying(255) NOT NULL,
    consumed boolean NOT NULL,
    email character varying(255) NOT NULL,
    expires_at timestamp(6) with time zone NOT NULL,
    purpose character varying(255) NOT NULL,
    user_type character varying(255),
    CONSTRAINT email_otp_purpose_check CHECK (((purpose)::text = ANY ((ARRAY['LOGIN_REGISTER'::character varying, 'PASSWORD_RESET'::character varying, 'OAUTH2'::character varying])::text[]))),
    CONSTRAINT email_otp_user_type_check CHECK (((user_type)::text = ANY ((ARRAY['ADMIN'::character varying, 'CANDIDATE'::character varying, 'RECRUITER'::character varying])::text[])))
);


ALTER TABLE public.email_otp OWNER TO irelis;

--
-- Name: email_otp_id_seq; Type: SEQUENCE; Schema: public; Owner: irelis
--

ALTER TABLE public.email_otp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.email_otp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: experience; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.experience (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    city character varying(255),
    company_name character varying(255),
    description character varying(255),
    end_date timestamp(6) without time zone,
    is_current boolean,
    "position" character varying(255),
    start_date timestamp(6) without time zone NOT NULL,
    candidate_id uuid NOT NULL
);


ALTER TABLE public.experience OWNER TO irelis;

--
-- Name: job_offer; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_offer (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    contract_type character varying(255),
    description character varying(255),
    experience_level character varying(255),
    expiration_date timestamp(6) without time zone,
    is_featured boolean,
    is_urgent boolean,
    job_type character varying(255),
    city character varying(255),
    country character varying(255),
    region character varying(255),
    max_salary double precision,
    min_salary double precision,
    published_at timestamp(6) without time zone,
    school_level character varying(255),
    show_salary boolean,
    status character varying(255),
    title character varying(255),
    company_id uuid NOT NULL,
    CONSTRAINT job_offer_contract_type_check CHECK (((contract_type)::text = ANY ((ARRAY['CDI'::character varying, 'CDD'::character varying, 'INTERNSHIP'::character varying, 'ALTERNATIVE'::character varying, 'FREELANCE'::character varying])::text[]))),
    CONSTRAINT job_offer_experience_level_check CHECK (((experience_level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'JUNIOR'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'SENIOR'::character varying, 'EXPERT'::character varying])::text[]))),
    CONSTRAINT job_offer_job_type_check CHECK (((job_type)::text = ANY ((ARRAY['FULL_TIME'::character varying, 'PART_TIME'::character varying, 'REMOTE'::character varying, 'HYBRID'::character varying])::text[]))),
    CONSTRAINT job_offer_school_level_check CHECK (((school_level)::text = ANY ((ARRAY['BAC'::character varying, 'DEUG'::character varying, 'BTS'::character varying, 'DUT'::character varying, 'LICENCE'::character varying, 'MASTER'::character varying, 'DOCTORAL'::character varying, 'UNKNOWN'::character varying])::text[]))),
    CONSTRAINT job_offer_status_check CHECK (((status)::text = ANY ((ARRAY['DRAFT'::character varying, 'PUBLISHED'::character varying, 'EXPIRED'::character varying, 'CLOSED'::character varying, 'DELETED'::character varying])::text[])))
);


ALTER TABLE public.job_offer OWNER TO irelis;

--
-- Name: job_offer_tags; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_offer_tags (
    job_offer_id uuid NOT NULL,
    tag_id uuid NOT NULL
);


ALTER TABLE public.job_offer_tags OWNER TO irelis;

--
-- Name: job_preferences; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_preferences (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    availability character varying(255),
    desired_position character varying(255),
    city character varying(255),
    country character varying(255),
    region character varying(255),
    pretentions_salarial character varying(255),
    candidate_id uuid NOT NULL
);


ALTER TABLE public.job_preferences OWNER TO irelis;

--
-- Name: job_preferences_contract_types; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_preferences_contract_types (
    job_preferences_id uuid NOT NULL,
    contract_type character varying(255) NOT NULL,
    CONSTRAINT job_preferences_contract_types_contract_type_check CHECK (((contract_type)::text = ANY ((ARRAY['CDI'::character varying, 'CDD'::character varying, 'INTERNSHIP'::character varying, 'ALTERNATIVE'::character varying, 'FREELANCE'::character varying])::text[])))
);


ALTER TABLE public.job_preferences_contract_types OWNER TO irelis;

--
-- Name: job_preferences_sectors; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_preferences_sectors (
    job_preferences_id uuid NOT NULL,
    sector_id uuid NOT NULL
);


ALTER TABLE public.job_preferences_sectors OWNER TO irelis;

--
-- Name: language; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.language (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    language character varying(255),
    level character varying(255),
    candidate_id uuid NOT NULL,
    CONSTRAINT language_level_check CHECK (((level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'BILINGUAL'::character varying, 'NATIVE_LANGUAGE'::character varying])::text[])))
);


ALTER TABLE public.language OWNER TO irelis;

--
-- Name: recruiters; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.recruiters (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    company_description character varying(255),
    company_email character varying(255),
    company_length integer,
    company_linked_in_url character varying(255),
    company_logo_url character varying(255),
    company_name character varying(255),
    company_phone character varying(255),
    company_website character varying(255),
    first_name character varying(255),
    function character varying(255),
    last_name character varying(255),
    city character varying(255),
    country character varying(255),
    region character varying(255),
    phone_number character varying(255),
    sector_id uuid,
    user_id uuid
);


ALTER TABLE public.recruiters OWNER TO irelis;

--
-- Name: saved_job_offers; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.saved_job_offers (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    saved_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    job_offer_id uuid NOT NULL
);


ALTER TABLE public.saved_job_offers OWNER TO irelis;

--
-- Name: sector; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.sector (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    description character varying(255),
    name character varying(255)
);


ALTER TABLE public.sector OWNER TO irelis;

--
-- Name: skill; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.skill (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    level character varying(255),
    name character varying(255),
    candidate_id uuid NOT NULL,
    CONSTRAINT skill_level_check CHECK (((level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'EXPERT'::character varying])::text[])))
);


ALTER TABLE public.skill OWNER TO irelis;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.tag (
    id uuid NOT NULL,
    nom character varying(255) NOT NULL
);


ALTER TABLE public.tag OWNER TO irelis;

--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.user_sessions (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    device_info character varying(255),
    expired_at timestamp(6) without time zone,
    ip_address character varying(255),
    is_active boolean,
    token character varying(255),
    user_id uuid
);


ALTER TABLE public.user_sessions OWNER TO irelis;

--
-- Name: users; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    deleted boolean NOT NULL,
    deleted_at timestamp(6) without time zone,
    email character varying(255) NOT NULL,
    email_verified_at timestamp(6) without time zone,
    password character varying(255),
    provider character varying(255) NOT NULL,
    role character varying(255) NOT NULL,
    user_type character varying(255),
    CONSTRAINT users_provider_check CHECK (((provider)::text = ANY ((ARRAY['EMAIL'::character varying, 'GOOGLE'::character varying, 'FACEBOOK'::character varying, 'LINKEDIN'::character varying])::text[]))),
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['ADMIN'::character varying, 'CANDIDATE'::character varying, 'RECRUITER'::character varying])::text[]))),
    CONSTRAINT users_user_type_check CHECK (((user_type)::text = ANY ((ARRAY['ADMIN'::character varying, 'CANDIDATE'::character varying, 'RECRUITER'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO irelis;

--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.applications (id, created_at, updated_at, applied_at, cover_letter, resume_url, status, candidate_id, job_offer_id) FROM stdin;
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.candidates (id, created_at, updated_at, avatar_url, birth_date, completion_rate, cv_url, experience_level, first_name, is_visible, last_name, linked_in_url, city, country, region, motivation_letter_url, phone_number, pitch_mail, portfolio_url, presentation, professional_title, school_level, user_id) FROM stdin;
daaf0ae7-669e-40ab-ac98-4ec134b15d4a	2025-11-27 22:59:43.684998	2025-11-27 22:59:43.685025	\N	\N	\N	\N	\N	\N	t	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	40078e0c-0ad4-4124-9d4c-8564b244ffcc
\.


--
-- Data for Name: education; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.education (id, created_at, updated_at, city, degree, graduation_year, institution, candidate_id) FROM stdin;
\.


--
-- Data for Name: email_otp; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.email_otp (id, code, consumed, email, expires_at, purpose, user_type) FROM stdin;
1	668535	t	averelldalton2504@gmail.com	2025-11-27 23:07:54.973848+00	LOGIN_REGISTER	CANDIDATE
\.


--
-- Data for Name: experience; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.experience (id, created_at, updated_at, city, company_name, description, end_date, is_current, "position", start_date, candidate_id) FROM stdin;
\.


--
-- Data for Name: job_offer; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_offer (id, created_at, updated_at, contract_type, description, experience_level, expiration_date, is_featured, is_urgent, job_type, city, country, region, max_salary, min_salary, published_at, school_level, show_salary, status, title, company_id) FROM stdin;
\.


--
-- Data for Name: job_offer_tags; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_offer_tags (job_offer_id, tag_id) FROM stdin;
\.


--
-- Data for Name: job_preferences; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_preferences (id, created_at, updated_at, availability, desired_position, city, country, region, pretentions_salarial, candidate_id) FROM stdin;
\.


--
-- Data for Name: job_preferences_contract_types; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_preferences_contract_types (job_preferences_id, contract_type) FROM stdin;
\.


--
-- Data for Name: job_preferences_sectors; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_preferences_sectors (job_preferences_id, sector_id) FROM stdin;
\.


--
-- Data for Name: language; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.language (id, created_at, updated_at, language, level, candidate_id) FROM stdin;
\.


--
-- Data for Name: recruiters; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.recruiters (id, created_at, updated_at, company_description, company_email, company_length, company_linked_in_url, company_logo_url, company_name, company_phone, company_website, first_name, function, last_name, city, country, region, phone_number, sector_id, user_id) FROM stdin;
\.


--
-- Data for Name: saved_job_offers; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.saved_job_offers (id, created_at, updated_at, saved_at, candidate_id, job_offer_id) FROM stdin;
\.


--
-- Data for Name: sector; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.sector (id, created_at, updated_at, description, name) FROM stdin;
2dc648ee-c01f-4584-9662-1a85783e34a9	2025-11-27 23:23:05.084829	2025-11-27 23:23:05.084875	\N	IT
1acc5355-ef25-45ed-92c9-20499c396ee3	2025-11-27 23:23:05.297261	2025-11-27 23:23:05.297316	\N	Marketing
\.


--
-- Data for Name: skill; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.skill (id, created_at, updated_at, level, name, candidate_id) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.tag (id, nom) FROM stdin;
\.


--
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.user_sessions (id, created_at, updated_at, device_info, expired_at, ip_address, is_active, token, user_id) FROM stdin;
746435b4-a871-47dd-90ad-4cc8201c728c	2025-11-27 22:59:43.691086	2025-11-27 22:59:43.691103	bruno-runtime/2.14.2	2025-11-27 23:59:43.665884	127.0.0.1	t	eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhdmVyZWxsZGFsdG9uMjUwNEBnbWFpbC5jb20iLCJyb2xlIjpbIkNBTkRJREFURSJdLCJpYXQiOjE3NjQyODQzODMsImV4cCI6MTc2NDM3MDc4M30.4EssJwGsxhWHXmtYyR6B0h91ofLJZKCKnIiaBHMk1KE	40078e0c-0ad4-4124-9d4c-8564b244ffcc
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.users (id, created_at, updated_at, deleted, deleted_at, email, email_verified_at, password, provider, role, user_type) FROM stdin;
40078e0c-0ad4-4124-9d4c-8564b244ffcc	2025-11-27 22:59:43.675083	2025-11-27 22:59:43.675116	f	\N	averelldalton2504@gmail.com	\N	\N	EMAIL	CANDIDATE	CANDIDATE
\.


--
-- Name: email_otp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: irelis
--

SELECT pg_catalog.setval('public.email_otp_id_seq', 1, true);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_pkey PRIMARY KEY (id);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (id);


--
-- Name: email_otp email_otp_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.email_otp
    ADD CONSTRAINT email_otp_pkey PRIMARY KEY (id);


--
-- Name: experience experience_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_pkey PRIMARY KEY (id);


--
-- Name: users idx_user_email; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT idx_user_email UNIQUE (email);


--
-- Name: job_offer job_offer_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer
    ADD CONSTRAINT job_offer_pkey PRIMARY KEY (id);


--
-- Name: job_offer_tags job_offer_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT job_offer_tags_pkey PRIMARY KEY (job_offer_id, tag_id);


--
-- Name: job_preferences job_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT job_preferences_pkey PRIMARY KEY (id);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (id);


--
-- Name: recruiters recruiters_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT recruiters_pkey PRIMARY KEY (id);


--
-- Name: saved_job_offers saved_job_offers_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT saved_job_offers_pkey PRIMARY KEY (id);


--
-- Name: sector sector_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.sector
    ADD CONSTRAINT sector_pkey PRIMARY KEY (id);


--
-- Name: skill skill_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_pkey PRIMARY KEY (id);


--
-- Name: tag tag_nom_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_nom_key UNIQUE (nom);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- Name: applications ukbigbiiy8iifquorgjvxockq5s; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT ukbigbiiy8iifquorgjvxockq5s UNIQUE (candidate_id, job_offer_id);


--
-- Name: saved_job_offers ukdi40lkjc3xf3pc6x1e58l3oao; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT ukdi40lkjc3xf3pc6x1e58l3oao UNIQUE (candidate_id, job_offer_id);


--
-- Name: candidates ukdoi1o7iyehcrqrrrbxjostvv5; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT ukdoi1o7iyehcrqrrrbxjostvv5 UNIQUE (user_id);


--
-- Name: recruiters uklhuhr3tmewk16uubn7q6w28t6; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT uklhuhr3tmewk16uubn7q6w28t6 UNIQUE (user_id);


--
-- Name: job_preferences uknvexlhg48x64953a0bgp77l5p; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT uknvexlhg48x64953a0bgp77l5p UNIQUE (candidate_id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: idx_emailotp_email; Type: INDEX; Schema: public; Owner: irelis
--

CREATE INDEX idx_emailotp_email ON public.email_otp USING btree (email);


--
-- Name: saved_job_offers fk163wmkbymiydh1ir5kjde0eqb; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT fk163wmkbymiydh1ir5kjde0eqb FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: recruiters fk1edjvp9udx35rophqr7imremb; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT fk1edjvp9udx35rophqr7imremb FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: recruiters fk4ypj6go37b5hrjhjsfl28rau8; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT fk4ypj6go37b5hrjhjsfl28rau8 FOREIGN KEY (sector_id) REFERENCES public.sector(id);


--
-- Name: experience fk86hiusttkmjri79aaq768i0j3; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT fk86hiusttkmjri79aaq768i0j3 FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: user_sessions fk8klxsgb8dcjjklmqebqp1twd5; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT fk8klxsgb8dcjjklmqebqp1twd5 FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_preferences_contract_types fkddnfcbtlslmj1c81pejbephjs; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences_contract_types
    ADD CONSTRAINT fkddnfcbtlslmj1c81pejbephjs FOREIGN KEY (job_preferences_id) REFERENCES public.job_preferences(id);


--
-- Name: applications fkg4e16cwk1qrad923bpx4hamdh; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fkg4e16cwk1qrad923bpx4hamdh FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: job_preferences_sectors fkh22ofid78evyq4aa932avuixc; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences_sectors
    ADD CONSTRAINT fkh22ofid78evyq4aa932avuixc FOREIGN KEY (sector_id) REFERENCES public.sector(id);


--
-- Name: saved_job_offers fkhh7wuufl6mhswp2im5xs861ws; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT fkhh7wuufl6mhswp2im5xs861ws FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: applications fkikabhgl3ia44efd9qfx8g28j6; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fkikabhgl3ia44efd9qfx8g28j6 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: job_preferences_sectors fkiuhpfwg6lw8goeuskjigo81jn; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences_sectors
    ADD CONSTRAINT fkiuhpfwg6lw8goeuskjigo81jn FOREIGN KEY (job_preferences_id) REFERENCES public.job_preferences(id);


--
-- Name: skill fkkxy886wf7ie5kmx5e4vkcn6pb; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT fkkxy886wf7ie5kmx5e4vkcn6pb FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidates fkme4fkelukmx2s63tlcrft6hio; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT fkme4fkelukmx2s63tlcrft6hio FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_preferences fkmiksqcnneg5r2lyq72wvh7w4n; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT fkmiksqcnneg5r2lyq72wvh7w4n FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: job_offer fkmixspuwrg25qymhwv5k6mytgw; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer
    ADD CONSTRAINT fkmixspuwrg25qymhwv5k6mytgw FOREIGN KEY (company_id) REFERENCES public.recruiters(id);


--
-- Name: education fknrikpllw36vuqeihc5ur19tvy; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT fknrikpllw36vuqeihc5ur19tvy FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: language fkpsfy57hlwjiep5x3y8eyqgtp2; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT fkpsfy57hlwjiep5x3y8eyqgtp2 FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: job_offer_tags job_offer_tags_job_offer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT job_offer_tags_job_offer_id_fkey FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: job_offer_tags job_offer_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT job_offer_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 7zhDMSuMbbfrD6bctrwYgumbL0PD1uy2kv39KoGph2LW2VzEqnsH5cTIRCSRwf4

