--
-- PostgreSQL database dump
--

\restrict 9w0xlgw9FHUVamaBb8voRXU18f20cjTniUyHjNH3JtRW1kt1D88fZpGW5vJf4jA

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
-- Name: search_target_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.search_target_enum AS ENUM (
    'OFFRE',
    'CANDIDAT'
);


ALTER TYPE public.search_target_enum OWNER TO irelis;

--
-- Name: search_type_enum; Type: TYPE; Schema: public; Owner: irelis
--

CREATE TYPE public.search_type_enum AS ENUM (
    'BOOL',
    'NOT'
);


ALTER TYPE public.search_type_enum OWNER TO irelis;

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
-- Name: application_document; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.application_document (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    application_id uuid,
    id uuid NOT NULL,
    storage_url character varying(255),
    type character varying(255),
    CONSTRAINT application_document_type_check CHECK (((type)::text = ANY ((ARRAY['CV'::character varying, 'COVER_LETTER'::character varying, 'PORTFOLIO'::character varying, 'CERTIFICATE'::character varying, 'IDENTITY_DOC'::character varying])::text[])))
);


ALTER TABLE public.application_document OWNER TO irelis;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.applications (
    applied_at timestamp(6) without time zone,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    job_offer_id uuid NOT NULL,
    message character varying(255),
    status character varying(255),
    CONSTRAINT applications_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'REVIEWED'::character varying, 'ACCEPTED'::character varying, 'REJECTED'::character varying, 'WITHDRAWN'::character varying])::text[])))
);


ALTER TABLE public.applications OWNER TO irelis;

--
-- Name: candidates; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.candidates (
    completion_rate double precision,
    is_visible boolean,
    last_viewed_month date,
    monthly_profile_views integer,
    profile_views integer,
    birth_date timestamp(6) without time zone,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    user_id uuid,
    pitch_mail character varying(2000),
    avatar_url character varying(255),
    city character varying(255),
    country character varying(255),
    cv_url character varying(255),
    experience_level character varying(255),
    first_name character varying(255),
    last_name character varying(255),
    linked_in_url character varying(255),
    motivation_letter_url character varying(255),
    phone_number character varying(255),
    portfolio_url character varying(255),
    presentation character varying(255),
    professional_title character varying(255),
    region character varying(255),
    school_level character varying(255),
    CONSTRAINT candidates_experience_level_check CHECK (((experience_level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'JUNIOR'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'SENIOR'::character varying, 'EXPERT'::character varying])::text[]))),
    CONSTRAINT candidates_school_level_check CHECK (((school_level)::text = ANY ((ARRAY['BAC'::character varying, 'DEUG'::character varying, 'BTS'::character varying, 'DUT'::character varying, 'LICENCE'::character varying, 'MASTER'::character varying, 'DOCTORAL'::character varying, 'UNKNOWN'::character varying])::text[])))
);


ALTER TABLE public.candidates OWNER TO irelis;

--
-- Name: candidature_info; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.candidature_info (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    job_offer_id uuid NOT NULL,
    email_candidature character varying(255),
    instructions character varying(255),
    required_documents character varying(255),
    url_candidature character varying(255)
);


ALTER TABLE public.candidature_info OWNER TO irelis;

--
-- Name: education; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.education (
    graduation_year integer,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    city character varying(255),
    degree character varying(255),
    institution character varying(255)
);


ALTER TABLE public.education OWNER TO irelis;

--
-- Name: email_otp; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.email_otp (
    consumed boolean NOT NULL,
    expires_at timestamp(6) with time zone NOT NULL,
    id bigint NOT NULL,
    code character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
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
    is_current boolean,
    created_at timestamp(6) without time zone,
    end_date timestamp(6) without time zone,
    start_date timestamp(6) without time zone NOT NULL,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    city character varying(255),
    company_name character varying(255),
    description character varying(255),
    "position" character varying(255)
);


ALTER TABLE public.experience OWNER TO irelis;

--
-- Name: job_offer; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.job_offer (
    is_featured boolean,
    is_urgent boolean,
    post_number integer,
    created_at timestamp(6) without time zone,
    expiration_date timestamp(6) without time zone,
    published_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    company_id uuid NOT NULL,
    id uuid NOT NULL,
    contract_type character varying(255),
    description character varying(255),
    instructions character varying(255),
    job_type character varying(255),
    required_language character varying(255),
    salary character varying(255),
    status character varying(255),
    title character varying(255),
    work_city_location character varying(255),
    work_country_location character varying(255),
    benefits oid,
    requirements oid,
    responsibilities oid,
    CONSTRAINT job_offer_contract_type_check CHECK (((contract_type)::text = ANY ((ARRAY['CDI'::character varying, 'CDD'::character varying, 'INTERNSHIP'::character varying, 'ALTERNATIVE'::character varying, 'FREELANCE'::character varying])::text[]))),
    CONSTRAINT job_offer_job_type_check CHECK (((job_type)::text = ANY ((ARRAY['FULL_TIME'::character varying, 'PART_TIME'::character varying, 'REMOTE'::character varying, 'HYBRID'::character varying])::text[]))),
    CONSTRAINT job_offer_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'PUBLISHED'::character varying, 'EXPIRED'::character varying, 'CLOSED'::character varying])::text[])))
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
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    availability character varying(255),
    city character varying(255),
    country character varying(255),
    desired_position character varying(255),
    pretentions_salarial character varying(255),
    region character varying(255)
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
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    language character varying(255),
    level character varying(255),
    CONSTRAINT language_level_check CHECK (((level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'BILINGUAL'::character varying, 'NATIVE_LANGUAGE'::character varying])::text[])))
);


ALTER TABLE public.language OWNER TO irelis;

--
-- Name: recruiters; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.recruiters (
    company_length integer,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    sector_id uuid,
    user_id uuid,
    city character varying(255),
    company_description character varying(255),
    company_email character varying(255),
    company_linked_in_url character varying(255),
    company_logo_url character varying(255),
    company_name character varying(255),
    company_phone character varying(255),
    company_website character varying(255),
    country character varying(255),
    first_name character varying(255),
    function character varying(255),
    last_name character varying(255),
    phone_number character varying(255),
    region character varying(255)
);


ALTER TABLE public.recruiters OWNER TO irelis;

--
-- Name: required_documents; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.required_documents (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    job_offer_id uuid,
    type character varying(255),
    CONSTRAINT required_documents_type_check CHECK (((type)::text = ANY ((ARRAY['CV'::character varying, 'COVER_LETTER'::character varying, 'PORTFOLIO'::character varying, 'CERTIFICATE'::character varying, 'IDENTITY_DOC'::character varying])::text[])))
);


ALTER TABLE public.required_documents OWNER TO irelis;

--
-- Name: saved_job_offers; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.saved_job_offers (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    job_offer_id uuid NOT NULL
);


ALTER TABLE public.saved_job_offers OWNER TO irelis;

--
-- Name: searches; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.searches (
    id uuid NOT NULL,
    query character varying(255) NOT NULL,
    type public.search_type_enum NOT NULL,
    target public.search_target_enum NOT NULL,
    country character varying(255),
    city character varying(255),
    town character varying(255),
    type_contrat character varying(255),
    niveau_etude character varying(255),
    experience character varying(255),
    language character varying(255),
    date_publication timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.searches OWNER TO irelis;

--
-- Name: sector; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.sector (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    description character varying(255),
    name character varying(255)
);


ALTER TABLE public.sector OWNER TO irelis;

--
-- Name: skill; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.skill (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    id uuid NOT NULL,
    level character varying(255),
    name character varying(255),
    CONSTRAINT skill_level_check CHECK (((level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'EXPERT'::character varying])::text[])))
);


ALTER TABLE public.skill OWNER TO irelis;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.tag (
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    name character varying(255),
    type character varying(255)
);


ALTER TABLE public.tag OWNER TO irelis;

--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.user_sessions (
    is_active boolean,
    created_at timestamp(6) without time zone,
    expired_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    user_id uuid,
    device_info character varying(255),
    ip_address character varying(255),
    token character varying(255)
);


ALTER TABLE public.user_sessions OWNER TO irelis;

--
-- Name: users; Type: TABLE; Schema: public; Owner: irelis
--

CREATE TABLE public.users (
    deleted boolean NOT NULL,
    created_at timestamp(6) without time zone,
    deleted_at timestamp(6) without time zone,
    email_verified_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
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
-- Data for Name: application_document; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.application_document (created_at, updated_at, application_id, id, storage_url, type) FROM stdin;
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.applications (applied_at, created_at, updated_at, candidate_id, id, job_offer_id, message, status) FROM stdin;
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.candidates (completion_rate, is_visible, last_viewed_month, monthly_profile_views, profile_views, birth_date, created_at, updated_at, id, user_id, pitch_mail, avatar_url, city, country, cv_url, experience_level, first_name, last_name, linked_in_url, motivation_letter_url, phone_number, portfolio_url, presentation, professional_title, region, school_level) FROM stdin;
\.


--
-- Data for Name: candidature_info; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.candidature_info (created_at, updated_at, id, job_offer_id, email_candidature, instructions, required_documents, url_candidature) FROM stdin;
\.


--
-- Data for Name: education; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.education (graduation_year, created_at, updated_at, candidate_id, id, city, degree, institution) FROM stdin;
\.


--
-- Data for Name: email_otp; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.email_otp (consumed, expires_at, id, code, email, purpose, user_type) FROM stdin;
\.


--
-- Data for Name: experience; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.experience (is_current, created_at, end_date, start_date, updated_at, candidate_id, id, city, company_name, description, "position") FROM stdin;
\.


--
-- Data for Name: job_offer; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_offer (is_featured, is_urgent, post_number, created_at, expiration_date, published_at, updated_at, company_id, id, contract_type, description, instructions, job_type, required_language, salary, status, title, work_city_location, work_country_location, benefits, requirements, responsibilities) FROM stdin;
\.


--
-- Data for Name: job_offer_tags; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_offer_tags (job_offer_id, tag_id) FROM stdin;
\.


--
-- Data for Name: job_preferences; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.job_preferences (created_at, updated_at, candidate_id, id, availability, city, country, desired_position, pretentions_salarial, region) FROM stdin;
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

COPY public.language (created_at, updated_at, candidate_id, id, language, level) FROM stdin;
\.


--
-- Data for Name: recruiters; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.recruiters (company_length, created_at, updated_at, id, sector_id, user_id, city, company_description, company_email, company_linked_in_url, company_logo_url, company_name, company_phone, company_website, country, first_name, function, last_name, phone_number, region) FROM stdin;
\.


--
-- Data for Name: required_documents; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.required_documents (created_at, updated_at, id, job_offer_id, type) FROM stdin;
\.


--
-- Data for Name: saved_job_offers; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.saved_job_offers (created_at, updated_at, candidate_id, id, job_offer_id) FROM stdin;
\.


--
-- Data for Name: searches; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.searches (id, query, type, target, country, city, town, type_contrat, niveau_etude, experience, language, date_publication, created_at, user_id) FROM stdin;
\.


--
-- Data for Name: sector; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.sector (created_at, updated_at, id, description, name) FROM stdin;
2025-12-08 10:52:13.039894	2025-12-08 10:52:13.039972	da601c62-f366-4e52-b4b1-3cb5cd4deb03	\N	IT
2025-12-08 10:52:13.058831	2025-12-08 10:52:13.058877	7cf6f16c-6248-4fb1-a2e0-c2a94b520740	\N	Marketing
\.


--
-- Data for Name: skill; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.skill (created_at, updated_at, candidate_id, id, level, name) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.tag (created_at, updated_at, id, name, type) FROM stdin;
2025-12-08 10:52:13.088996	2025-12-08 10:52:13.089038	aa1cc550-561f-418f-bd4d-26d707c04953	Java	SKILL
2025-12-08 10:52:13.091833	2025-12-08 10:52:13.091875	b2af8b66-47b1-432a-8ed1-d71087ada5e4	Spring Boot	SKILL
2025-12-08 10:52:13.093774	2025-12-08 10:52:13.093817	2f5f8e2c-bab6-4a3e-b64a-8d5f40fcec63	Marketing Digital	SKILL
2025-12-08 10:52:13.096324	2025-12-08 10:52:13.09636	199101e7-e903-4a4f-898c-926ca05200f6	Remote	WORK_STYLE
2025-12-08 10:52:13.098144	2025-12-08 10:52:13.098177	624d2797-0dd5-4430-a426-d90d59c34f3a	Full-time	WORK_STYLE
2025-12-08 10:52:13.100484	2025-12-08 10:52:13.100519	2fd89c75-c8d1-47c4-ad0d-b006ff5bf5b1	Urgent	PRIORITY
2025-12-08 10:52:13.101877	2025-12-08 10:52:13.101904	4071bd88-7391-48ad-9ab0-f3737526acb6	Featured	PRIORITY
\.


--
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.user_sessions (is_active, created_at, expired_at, updated_at, id, user_id, device_info, ip_address, token) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: irelis
--

COPY public.users (deleted, created_at, deleted_at, email_verified_at, updated_at, id, email, password, provider, role, user_type) FROM stdin;
\.


--
-- Name: email_otp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: irelis
--

SELECT pg_catalog.setval('public.email_otp_id_seq', 1, false);


--
-- Name: application_document application_document_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.application_document
    ADD CONSTRAINT application_document_pkey PRIMARY KEY (id);


--
-- Name: applications applications_candidate_id_job_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_candidate_id_job_offer_id_key UNIQUE (candidate_id, job_offer_id);


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
-- Name: candidates candidates_user_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_user_id_key UNIQUE (user_id);


--
-- Name: candidature_info candidature_info_job_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidature_info
    ADD CONSTRAINT candidature_info_job_offer_id_key UNIQUE (job_offer_id);


--
-- Name: candidature_info candidature_info_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidature_info
    ADD CONSTRAINT candidature_info_pkey PRIMARY KEY (id);


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
-- Name: job_preferences job_preferences_candidate_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT job_preferences_candidate_id_key UNIQUE (candidate_id);


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
-- Name: recruiters recruiters_user_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT recruiters_user_id_key UNIQUE (user_id);


--
-- Name: required_documents required_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.required_documents
    ADD CONSTRAINT required_documents_pkey PRIMARY KEY (id);


--
-- Name: saved_job_offers saved_job_offers_candidate_id_job_offer_id_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT saved_job_offers_candidate_id_job_offer_id_key UNIQUE (candidate_id, job_offer_id);


--
-- Name: saved_job_offers saved_job_offers_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT saved_job_offers_pkey PRIMARY KEY (id);


--
-- Name: searches searches_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.searches
    ADD CONSTRAINT searches_pkey PRIMARY KEY (id);


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
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


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
-- Name: job_offer_tags fk6jo4l36cdbmkoql3gtv4wbl3c; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT fk6jo4l36cdbmkoql3gtv4wbl3c FOREIGN KEY (tag_id) REFERENCES public.tag(id);


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
-- Name: job_offer_tags fk9nva3u1mo012bhly1t9psi9a8; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT fk9nva3u1mo012bhly1t9psi9a8 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: application_document fkb7xr983jbgy8cj40aobikcqlk; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.application_document
    ADD CONSTRAINT fkb7xr983jbgy8cj40aobikcqlk FOREIGN KEY (application_id) REFERENCES public.applications(id);


--
-- Name: job_preferences_contract_types fkddnfcbtlslmj1c81pejbephjs; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.job_preferences_contract_types
    ADD CONSTRAINT fkddnfcbtlslmj1c81pejbephjs FOREIGN KEY (job_preferences_id) REFERENCES public.job_preferences(id);


--
-- Name: candidature_info fke4rv6kmi64ct7pnu9461ec43b; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.candidature_info
    ADD CONSTRAINT fke4rv6kmi64ct7pnu9461ec43b FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


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
-- Name: required_documents fkslnbpgit0aban0a4k5ji54gk8; Type: FK CONSTRAINT; Schema: public; Owner: irelis
--

ALTER TABLE ONLY public.required_documents
    ADD CONSTRAINT fkslnbpgit0aban0a4k5ji54gk8 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 9w0xlgw9FHUVamaBb8voRXU18f20cjTniUyHjNH3JtRW1kt1D88fZpGW5vJf4jA

