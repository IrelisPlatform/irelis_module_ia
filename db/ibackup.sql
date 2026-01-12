--
-- PostgreSQL database dump
--

\restrict bNObnwheRZQJBR3b68GSIe2U1NXbZt9DSemRJLofshHRNceCbI3XsOF9U8ySHEu

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.7 (Debian 17.7-3.pgdg13+1)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: application_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.application_status_enum AS ENUM (
    'ACCEPTED',
    'PENDING',
    'REJECTED',
    'REVIEWED',
    'WITHDRAWN'
);


--
-- Name: candidate_experience_level_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.candidate_experience_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE',
    'JUNIOR',
    'SENIOR'
);


--
-- Name: candidate_school_level_enum; Type: TYPE; Schema: public; Owner: -
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


--
-- Name: email_otp_purpose_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.email_otp_purpose_enum AS ENUM (
    'LOGIN_REGISTER',
    'PASSWORD_RESET'
);


--
-- Name: email_otp_user_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.email_otp_user_type_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


--
-- Name: job_offer_contract_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_offer_contract_enum AS ENUM (
    'ALTERNATIVE',
    'CDD',
    'CDI',
    'FREELANCE',
    'INTERNSHIP'
);


--
-- Name: job_offer_experience_level_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_offer_experience_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE',
    'JUNIOR',
    'SENIOR'
);


--
-- Name: job_offer_school_level_enum; Type: TYPE; Schema: public; Owner: -
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


--
-- Name: job_offer_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_offer_status_enum AS ENUM (
    'CLOSED',
    'DELETED',
    'DRAFT',
    'EXPIRED',
    'PUBLISHED'
);


--
-- Name: job_offer_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_offer_type_enum AS ENUM (
    'FULL_TIME',
    'HYBRID',
    'PART_TIME',
    'REMOTE'
);


--
-- Name: job_preferences_contract_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.job_preferences_contract_enum AS ENUM (
    'ALTERNATIVE',
    'CDD',
    'CDI',
    'FREELANCE',
    'INTERNSHIP'
);


--
-- Name: language_level_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.language_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'BILINGUAL',
    'INTERMEDIATE',
    'NATIVE_LANGUAGE'
);


--
-- Name: provider_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.provider_enum AS ENUM (
    'EMAIL',
    'FACEBOOK',
    'GOOGLE',
    'LINKEDIN'
);


--
-- Name: search_target_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.search_target_enum AS ENUM (
    'OFFRE',
    'CANDIDAT'
);


--
-- Name: search_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.search_type_enum AS ENUM (
    'BOOL',
    'NOT'
);


--
-- Name: skill_level_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.skill_level_enum AS ENUM (
    'ADVANCED',
    'BEGINNER',
    'EXPERT',
    'INTERMEDIATE'
);


--
-- Name: user_role_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.user_role_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


--
-- Name: user_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.user_type_enum AS ENUM (
    'ADMIN',
    'CANDIDATE',
    'RECRUITER'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: application_document; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.application_document (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    storage_url character varying(255),
    type character varying(255),
    application_id uuid,
    CONSTRAINT application_document_type_check CHECK (((type)::text = ANY ((ARRAY['CV'::character varying, 'COVER_LETTER'::character varying, 'PORTFOLIO'::character varying, 'CERTIFICATE'::character varying, 'IDENTITY_DOC'::character varying])::text[])))
);


--
-- Name: applications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.applications (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    applied_at timestamp(6) without time zone,
    message character varying(255),
    status character varying(255),
    candidate_id uuid NOT NULL,
    job_offer_id uuid NOT NULL,
    CONSTRAINT applications_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'REVIEWED'::character varying, 'ACCEPTED'::character varying, 'REJECTED'::character varying, 'WITHDRAWN'::character varying])::text[])))
);


--
-- Name: candidates; Type: TABLE; Schema: public; Owner: -
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
    last_viewed_month date,
    linked_in_url character varying(255),
    city character varying(255),
    country character varying(255),
    region character varying(255),
    monthly_profile_views integer,
    motivation_letter_url character varying(255),
    phone_number character varying(255),
    pitch_mail character varying(2000),
    portfolio_url character varying(255),
    presentation character varying(255),
    professional_title character varying(255),
    profile_views integer,
    school_level character varying(255),
    user_id uuid,
    CONSTRAINT candidates_experience_level_check CHECK (((experience_level)::text = ANY ((ARRAY['BEGINNER'::character varying, 'JUNIOR'::character varying, 'INTERMEDIATE'::character varying, 'ADVANCED'::character varying, 'SENIOR'::character varying, 'EXPERT'::character varying])::text[]))),
    CONSTRAINT candidates_school_level_check CHECK (((school_level)::text = ANY ((ARRAY['BAC'::character varying, 'DEUG'::character varying, 'BTS'::character varying, 'DUT'::character varying, 'LICENCE'::character varying, 'MASTER'::character varying, 'DOCTORAL'::character varying, 'UNKNOWN'::character varying])::text[])))
);


--
-- Name: candidature_info; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.candidature_info (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    email_candidature character varying(255),
    instructions character varying(255),
    required_documents character varying(255),
    url_candidature character varying(255),
    job_offer_id uuid NOT NULL
);


--
-- Name: chatbot_faq_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_faq_entries (
    id uuid NOT NULL,
    question text NOT NULL,
    answer text NOT NULL,
    category character varying(255),
    lang character varying(10),
    keywords character varying(255)[],
    is_active boolean NOT NULL,
    source character varying(255),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    version integer NOT NULL
);


--
-- Name: chatbot_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_feedback (
    id uuid NOT NULL,
    user_id uuid,
    session_id uuid,
    response_message_id uuid NOT NULL,
    faq_entry_id uuid,
    rating smallint NOT NULL,
    comment text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: chatbot_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_messages (
    id uuid NOT NULL,
    session_id uuid,
    user_id uuid,
    content text NOT NULL,
    type character varying(8) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    channel character varying(8),
    lang character varying(10),
    token character varying(255),
    faq_entry_id uuid,
    confidence double precision,
    handoff boolean NOT NULL
);


--
-- Name: chatbot_sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_sessions (
    id uuid NOT NULL,
    user_id uuid,
    state character varying(7) NOT NULL,
    channel character varying(8) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    ended_at timestamp with time zone,
    last_activity_at timestamp with time zone,
    metadata jsonb
);


--
-- Name: chatbot_unmatched_questions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chatbot_unmatched_questions (
    id uuid NOT NULL,
    user_id uuid,
    session_id uuid,
    request_message_id uuid NOT NULL,
    content text NOT NULL,
    lang character varying(10),
    channel character varying(8),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    top_candidates jsonb,
    reason character varying(14),
    status character varying(11) NOT NULL,
    reviewed_at timestamp with time zone,
    resolved_faq_entry_id uuid
);


--
-- Name: education; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: email_otp; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: email_otp_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- Name: experience; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: flyway_schema_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.flyway_schema_history (
    installed_rank integer NOT NULL,
    version character varying(50),
    description character varying(200) NOT NULL,
    type character varying(20) NOT NULL,
    script character varying(1000) NOT NULL,
    checksum integer,
    installed_by character varying(100) NOT NULL,
    installed_on timestamp without time zone DEFAULT now() NOT NULL,
    execution_time integer NOT NULL,
    success boolean NOT NULL
);


--
-- Name: job_offer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_offer (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    contract_type character varying(255),
    description oid,
    expiration_date timestamp(6) without time zone,
    instructions character varying(255),
    is_featured boolean,
    is_urgent boolean,
    job_type character varying(255),
    post_number integer,
    published_at timestamp(6) without time zone,
    reject_reason character varying(255),
    rejected_at timestamp(6) without time zone,
    salary character varying(255),
    status character varying(255),
    title character varying(255),
    work_country_location character varying(255),
    company_id uuid NOT NULL,
    CONSTRAINT job_offer_contract_type_check CHECK (((contract_type)::text = ANY ((ARRAY['CDI'::character varying, 'CDD'::character varying, 'INTERNSHIP'::character varying, 'ALTERNATIVE'::character varying, 'FREELANCE'::character varying])::text[]))),
    CONSTRAINT job_offer_job_type_check CHECK (((job_type)::text = ANY ((ARRAY['FULL_TIME'::character varying, 'PART_TIME'::character varying, 'REMOTE'::character varying, 'HYBRID'::character varying])::text[]))),
    CONSTRAINT job_offer_status_check CHECK (((status)::text = ANY ((ARRAY['PENDING'::character varying, 'PUBLISHED'::character varying, 'EXPIRED'::character varying, 'REJECTED'::character varying, 'CLOSED'::character varying])::text[])))
);


--
-- Name: job_offer_cities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_offer_cities (
    job_offer_id uuid NOT NULL,
    city character varying(255)
);


--
-- Name: job_offer_languages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_offer_languages (
    job_offer_id uuid NOT NULL,
    language character varying(255)
);


--
-- Name: job_offer_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_offer_tags (
    job_offer_id uuid NOT NULL,
    tag_id uuid NOT NULL
);


--
-- Name: job_preferences; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: job_preferences_contract_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_preferences_contract_types (
    job_preferences_id uuid NOT NULL,
    contract_type character varying(255) NOT NULL,
    CONSTRAINT job_preferences_contract_types_contract_type_check CHECK (((contract_type)::text = ANY ((ARRAY['CDI'::character varying, 'CDD'::character varying, 'INTERNSHIP'::character varying, 'ALTERNATIVE'::character varying, 'FREELANCE'::character varying])::text[])))
);


--
-- Name: job_preferences_sectors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.job_preferences_sectors (
    job_preferences_id uuid NOT NULL,
    sector_id uuid NOT NULL
);


--
-- Name: language; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: recruiters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recruiters (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    company_description oid,
    company_email character varying(255),
    company_length character varying(255),
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


--
-- Name: required_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.required_documents (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    type character varying(255),
    job_offer_id uuid,
    CONSTRAINT required_documents_type_check CHECK (((type)::text = ANY ((ARRAY['CV'::character varying, 'COVER_LETTER'::character varying, 'PORTFOLIO'::character varying, 'CERTIFICATE'::character varying, 'IDENTITY_DOC'::character varying])::text[])))
);


--
-- Name: saved_job_offers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.saved_job_offers (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    candidate_id uuid NOT NULL,
    job_offer_id uuid NOT NULL
);


--
-- Name: searches; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: sector; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sector (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    description character varying(255),
    name character varying(255)
);


--
-- Name: skill; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tag (
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    name character varying(255),
    type character varying(255)
);


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
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


--
-- Name: application_document application_document_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_document
    ADD CONSTRAINT application_document_pkey PRIMARY KEY (id);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_pkey PRIMARY KEY (id);


--
-- Name: candidature_info candidature_info_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidature_info
    ADD CONSTRAINT candidature_info_pkey PRIMARY KEY (id);


--
-- Name: chatbot_faq_entries chatbot_faq_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_faq_entries
    ADD CONSTRAINT chatbot_faq_entries_pkey PRIMARY KEY (id);


--
-- Name: chatbot_feedback chatbot_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_pkey PRIMARY KEY (id);


--
-- Name: chatbot_feedback chatbot_feedback_response_message_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_response_message_id_key UNIQUE (response_message_id);


--
-- Name: chatbot_messages chatbot_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_messages
    ADD CONSTRAINT chatbot_messages_pkey PRIMARY KEY (id);


--
-- Name: chatbot_sessions chatbot_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_sessions
    ADD CONSTRAINT chatbot_sessions_pkey PRIMARY KEY (id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_pkey PRIMARY KEY (id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_request_message_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_request_message_id_key UNIQUE (request_message_id);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (id);


--
-- Name: email_otp email_otp_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_otp
    ADD CONSTRAINT email_otp_pkey PRIMARY KEY (id);


--
-- Name: experience experience_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_pkey PRIMARY KEY (id);


--
-- Name: flyway_schema_history flyway_schema_history_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.flyway_schema_history
    ADD CONSTRAINT flyway_schema_history_pk PRIMARY KEY (installed_rank);


--
-- Name: users idx_user_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT idx_user_email UNIQUE (email);


--
-- Name: job_offer job_offer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer
    ADD CONSTRAINT job_offer_pkey PRIMARY KEY (id);


--
-- Name: job_offer_tags job_offer_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT job_offer_tags_pkey PRIMARY KEY (job_offer_id, tag_id);


--
-- Name: job_preferences job_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT job_preferences_pkey PRIMARY KEY (id);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (id);


--
-- Name: recruiters recruiters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT recruiters_pkey PRIMARY KEY (id);


--
-- Name: required_documents required_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.required_documents
    ADD CONSTRAINT required_documents_pkey PRIMARY KEY (id);


--
-- Name: saved_job_offers saved_job_offers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT saved_job_offers_pkey PRIMARY KEY (id);


--
-- Name: searches searches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.searches
    ADD CONSTRAINT searches_pkey PRIMARY KEY (id);


--
-- Name: sector sector_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sector
    ADD CONSTRAINT sector_pkey PRIMARY KEY (id);


--
-- Name: skill skill_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_pkey PRIMARY KEY (id);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- Name: candidature_info uk8atf9puoqpr0npdqd23gyl4fr; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidature_info
    ADD CONSTRAINT uk8atf9puoqpr0npdqd23gyl4fr UNIQUE (job_offer_id);


--
-- Name: applications ukbigbiiy8iifquorgjvxockq5s; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT ukbigbiiy8iifquorgjvxockq5s UNIQUE (candidate_id, job_offer_id);


--
-- Name: saved_job_offers ukdi40lkjc3xf3pc6x1e58l3oao; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT ukdi40lkjc3xf3pc6x1e58l3oao UNIQUE (candidate_id, job_offer_id);


--
-- Name: candidates ukdoi1o7iyehcrqrrrbxjostvv5; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT ukdoi1o7iyehcrqrrrbxjostvv5 UNIQUE (user_id);


--
-- Name: recruiters uklhuhr3tmewk16uubn7q6w28t6; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT uklhuhr3tmewk16uubn7q6w28t6 UNIQUE (user_id);


--
-- Name: job_preferences uknvexlhg48x64953a0bgp77l5p; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT uknvexlhg48x64953a0bgp77l5p UNIQUE (candidate_id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: flyway_schema_history_s_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX flyway_schema_history_s_idx ON public.flyway_schema_history USING btree (success);


--
-- Name: idx_emailotp_email; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_emailotp_email ON public.email_otp USING btree (email);


--
-- Name: idx_job_contract_published; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_job_contract_published ON public.job_offer USING btree (contract_type, published_at);


--
-- Name: idx_job_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_job_status ON public.job_offer USING btree (status);


--
-- Name: idx_sector_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sector_name ON public.sector USING btree (name);


--
-- Name: ix_chatbot_feedback_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_feedback_session_id ON public.chatbot_feedback USING btree (session_id);


--
-- Name: ix_chatbot_feedback_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_feedback_user_id ON public.chatbot_feedback USING btree (user_id);


--
-- Name: ix_chatbot_messages_session_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_messages_session_created_at ON public.chatbot_messages USING btree (session_id, created_at);


--
-- Name: ix_chatbot_messages_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_messages_session_id ON public.chatbot_messages USING btree (session_id);


--
-- Name: ix_chatbot_messages_user_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_messages_user_created_at ON public.chatbot_messages USING btree (user_id, created_at);


--
-- Name: ix_chatbot_messages_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_messages_user_id ON public.chatbot_messages USING btree (user_id);


--
-- Name: ix_chatbot_sessions_current_user_channel; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_chatbot_sessions_current_user_channel ON public.chatbot_sessions USING btree (user_id, channel) WHERE ((state)::text = 'current'::text);


--
-- Name: ix_chatbot_sessions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_sessions_user_id ON public.chatbot_sessions USING btree (user_id);


--
-- Name: ix_chatbot_unmatched_questions_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_unmatched_questions_session_id ON public.chatbot_unmatched_questions USING btree (session_id);


--
-- Name: ix_chatbot_unmatched_questions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_chatbot_unmatched_questions_user_id ON public.chatbot_unmatched_questions USING btree (user_id);


--
-- Name: chatbot_feedback chatbot_feedback_faq_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_faq_entry_id_fkey FOREIGN KEY (faq_entry_id) REFERENCES public.chatbot_faq_entries(id);


--
-- Name: chatbot_feedback chatbot_feedback_response_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_response_message_id_fkey FOREIGN KEY (response_message_id) REFERENCES public.chatbot_messages(id);


--
-- Name: chatbot_feedback chatbot_feedback_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.chatbot_sessions(id);


--
-- Name: chatbot_feedback chatbot_feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_feedback
    ADD CONSTRAINT chatbot_feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: chatbot_messages chatbot_messages_faq_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_messages
    ADD CONSTRAINT chatbot_messages_faq_entry_id_fkey FOREIGN KEY (faq_entry_id) REFERENCES public.chatbot_faq_entries(id);


--
-- Name: chatbot_messages chatbot_messages_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_messages
    ADD CONSTRAINT chatbot_messages_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.chatbot_sessions(id);


--
-- Name: chatbot_messages chatbot_messages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_messages
    ADD CONSTRAINT chatbot_messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: chatbot_sessions chatbot_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_sessions
    ADD CONSTRAINT chatbot_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_request_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_request_message_id_fkey FOREIGN KEY (request_message_id) REFERENCES public.chatbot_messages(id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_resolved_faq_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_resolved_faq_entry_id_fkey FOREIGN KEY (resolved_faq_entry_id) REFERENCES public.chatbot_faq_entries(id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.chatbot_sessions(id);


--
-- Name: chatbot_unmatched_questions chatbot_unmatched_questions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chatbot_unmatched_questions
    ADD CONSTRAINT chatbot_unmatched_questions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: saved_job_offers fk163wmkbymiydh1ir5kjde0eqb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT fk163wmkbymiydh1ir5kjde0eqb FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: recruiters fk1edjvp9udx35rophqr7imremb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT fk1edjvp9udx35rophqr7imremb FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: recruiters fk4ypj6go37b5hrjhjsfl28rau8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recruiters
    ADD CONSTRAINT fk4ypj6go37b5hrjhjsfl28rau8 FOREIGN KEY (sector_id) REFERENCES public.sector(id);


--
-- Name: job_offer_tags fk6jo4l36cdbmkoql3gtv4wbl3c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT fk6jo4l36cdbmkoql3gtv4wbl3c FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: experience fk86hiusttkmjri79aaq768i0j3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT fk86hiusttkmjri79aaq768i0j3 FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: user_sessions fk8klxsgb8dcjjklmqebqp1twd5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT fk8klxsgb8dcjjklmqebqp1twd5 FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_offer_tags fk9nva3u1mo012bhly1t9psi9a8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer_tags
    ADD CONSTRAINT fk9nva3u1mo012bhly1t9psi9a8 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: job_offer_cities fk_job_offer_cities_on_job_offer; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer_cities
    ADD CONSTRAINT fk_job_offer_cities_on_job_offer FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: job_offer_languages fk_job_offer_languages_on_job_offer; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer_languages
    ADD CONSTRAINT fk_job_offer_languages_on_job_offer FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: application_document fkb7xr983jbgy8cj40aobikcqlk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.application_document
    ADD CONSTRAINT fkb7xr983jbgy8cj40aobikcqlk FOREIGN KEY (application_id) REFERENCES public.applications(id);


--
-- Name: job_preferences_contract_types fkddnfcbtlslmj1c81pejbephjs; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences_contract_types
    ADD CONSTRAINT fkddnfcbtlslmj1c81pejbephjs FOREIGN KEY (job_preferences_id) REFERENCES public.job_preferences(id);


--
-- Name: applications fkg4e16cwk1qrad923bpx4hamdh; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fkg4e16cwk1qrad923bpx4hamdh FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: job_preferences_sectors fkh22ofid78evyq4aa932avuixc; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences_sectors
    ADD CONSTRAINT fkh22ofid78evyq4aa932avuixc FOREIGN KEY (sector_id) REFERENCES public.sector(id);


--
-- Name: saved_job_offers fkhh7wuufl6mhswp2im5xs861ws; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.saved_job_offers
    ADD CONSTRAINT fkhh7wuufl6mhswp2im5xs861ws FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: applications fkikabhgl3ia44efd9qfx8g28j6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fkikabhgl3ia44efd9qfx8g28j6 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- Name: job_preferences_sectors fkiuhpfwg6lw8goeuskjigo81jn; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences_sectors
    ADD CONSTRAINT fkiuhpfwg6lw8goeuskjigo81jn FOREIGN KEY (job_preferences_id) REFERENCES public.job_preferences(id);


--
-- Name: skill fkkxy886wf7ie5kmx5e4vkcn6pb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT fkkxy886wf7ie5kmx5e4vkcn6pb FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: candidates fkme4fkelukmx2s63tlcrft6hio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT fkme4fkelukmx2s63tlcrft6hio FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: job_preferences fkmiksqcnneg5r2lyq72wvh7w4n; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_preferences
    ADD CONSTRAINT fkmiksqcnneg5r2lyq72wvh7w4n FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: job_offer fkmixspuwrg25qymhwv5k6mytgw; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.job_offer
    ADD CONSTRAINT fkmixspuwrg25qymhwv5k6mytgw FOREIGN KEY (company_id) REFERENCES public.recruiters(id);


--
-- Name: education fknrikpllw36vuqeihc5ur19tvy; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.education
    ADD CONSTRAINT fknrikpllw36vuqeihc5ur19tvy FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: language fkpsfy57hlwjiep5x3y8eyqgtp2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT fkpsfy57hlwjiep5x3y8eyqgtp2 FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: required_documents fkslnbpgit0aban0a4k5ji54gk8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.required_documents
    ADD CONSTRAINT fkslnbpgit0aban0a4k5ji54gk8 FOREIGN KEY (job_offer_id) REFERENCES public.job_offer(id);


--
-- PostgreSQL database dump complete
--

\unrestrict bNObnwheRZQJBR3b68GSIe2U1NXbZt9DSemRJLofshHRNceCbI3XsOF9U8ySHEu

