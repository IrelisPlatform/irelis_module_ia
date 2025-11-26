-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : mar. 25 nov. 2025 à 11:32
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `irelis`
--

-- --------------------------------------------------------

--
-- Structure de la table `applications`
--

CREATE TABLE `applications` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `applied_at` datetime(6) DEFAULT NULL,
  `cover_letter` varchar(255) DEFAULT NULL,
  `resume_url` varchar(255) DEFAULT NULL,
  `status` enum('ACCEPTED','PENDING','REJECTED','REVIEWED','WITHDRAWN') DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL,
  `job_offer_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `candidates`
--

CREATE TABLE `candidates` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `birth_date` datetime(6) DEFAULT NULL,
  `completion_rate` double DEFAULT NULL,
  `cv_url` varchar(255) DEFAULT NULL,
  `experience_level` enum('ADVANCED','BEGINNER','EXPERT','INTERMEDIATE','JUNIOR','SENIOR') DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `is_visible` bit(1) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `linked_in_url` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `motivation_letter_url` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `portfolio_url` varchar(255) DEFAULT NULL,
  `presentation` varchar(255) DEFAULT NULL,
  `professional_title` varchar(255) DEFAULT NULL,
  `school_level` enum('BAC','BTS','DEUG','DOCTORAL','DUT','LICENCE','MASTER','UNKNOWN') DEFAULT NULL,
  `user_id` binary(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `candidates`
--

INSERT INTO `candidates` (`id`, `created_at`, `updated_at`, `avatar_url`, `birth_date`, `completion_rate`, `cv_url`, `experience_level`, `first_name`, `is_visible`, `last_name`, `linked_in_url`, `city`, `country`, `region`, `motivation_letter_url`, `phone_number`, `portfolio_url`, `presentation`, `professional_title`, `school_level`, `user_id`) VALUES
(0xc6df689d65084916ab5dd23c9a506f91, '2025-11-24 18:06:27.000000', '2025-11-24 18:06:27.000000', NULL, NULL, NULL, NULL, NULL, NULL, b'1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0x9e17f8dc71f643c28004cffa436baa93),
(0xe1845774476049d4970d50a7c90f8111, '2025-11-24 18:13:39.000000', '2025-11-24 18:13:39.000000', NULL, NULL, NULL, NULL, NULL, NULL, b'1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0x9fd1023308994824bb6da9f26beabf13);

-- --------------------------------------------------------

--
-- Structure de la table `education`
--

CREATE TABLE `education` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `graduation_year` int(11) DEFAULT NULL,
  `institution` varchar(255) DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `email_otp`
--

CREATE TABLE `email_otp` (
  `id` bigint(20) NOT NULL,
  `code` varchar(255) NOT NULL,
  `consumed` bit(1) NOT NULL,
  `email` varchar(255) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `purpose` enum('LOGIN_REGISTER','PASSWORD_RESET') NOT NULL,
  `user_type` enum('ADMIN','CANDIDATE','RECRUITER') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `email_otp`
--

INSERT INTO `email_otp` (`id`, `code`, `consumed`, `email`, `expires_at`, `purpose`, `user_type`) VALUES
(3, '435262', b'0', 'averelldalton2504@gmail.com', '2025-11-24 17:18:11.000000', 'LOGIN_REGISTER', 'RECRUITER'),
(4, '862875', b'1', 'luqnleng5@gmail.com', '2025-11-24 17:19:28.000000', 'LOGIN_REGISTER', 'CANDIDATE');

-- --------------------------------------------------------

--
-- Structure de la table `experience`
--

CREATE TABLE `experience` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `is_current` bit(1) DEFAULT NULL,
  `position` varchar(255) DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `candidate_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `job_offer`
--

CREATE TABLE `job_offer` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `contract_type` enum('ALTERNATIVE','CDD','CDI','FREELANCE','INTERNSHIP') DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `experience_level` enum('ADVANCED','BEGINNER','EXPERT','INTERMEDIATE','JUNIOR','SENIOR') DEFAULT NULL,
  `expiration_date` datetime(6) DEFAULT NULL,
  `is_featured` bit(1) DEFAULT NULL,
  `is_urgent` bit(1) DEFAULT NULL,
  `job_type` enum('FULL_TIME','HYBRID','PART_TIME','REMOTE') DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `max_salary` double DEFAULT NULL,
  `min_salary` double DEFAULT NULL,
  `published_at` datetime(6) DEFAULT NULL,
  `school_level` enum('BAC','BTS','DEUG','DOCTORAL','DUT','LICENCE','MASTER','UNKNOWN') DEFAULT NULL,
  `show_salary` bit(1) DEFAULT NULL,
  `status` enum('CLOSED','DELETED','DRAFT','EXPIRED','PUBLISHED') DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `company_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `job_preferences`
--

CREATE TABLE `job_preferences` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `availability` varchar(255) DEFAULT NULL,
  `desired_position` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `pretentions_salarial` varchar(255) DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `job_preferences_contract_types`
--

CREATE TABLE `job_preferences_contract_types` (
  `job_preferences_id` binary(16) NOT NULL,
  `contract_type` enum('ALTERNATIVE','CDD','CDI','FREELANCE','INTERNSHIP') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `job_preferences_sectors`
--

CREATE TABLE `job_preferences_sectors` (
  `job_preferences_id` binary(16) NOT NULL,
  `sector_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `language`
--

CREATE TABLE `language` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `level` enum('ADVANCED','BEGINNER','BILINGUAL','INTERMEDIATE','NATIVE_LANGUAGE') DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `recruiters`
--

CREATE TABLE `recruiters` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `company_description` varchar(255) DEFAULT NULL,
  `company_email` varchar(255) DEFAULT NULL,
  `company_length` int(11) DEFAULT NULL,
  `company_linked_in_url` varchar(255) DEFAULT NULL,
  `company_logo_url` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_phone` varchar(255) DEFAULT NULL,
  `company_website` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `function` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `region` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `sector_id` binary(16) DEFAULT NULL,
  `user_id` binary(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `saved_job_offers`
--

CREATE TABLE `saved_job_offers` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `saved_at` datetime(6) DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL,
  `job_offer_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `sector`
--

CREATE TABLE `sector` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `skill`
--

CREATE TABLE `skill` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `level` enum('ADVANCED','BEGINNER','EXPERT','INTERMEDIATE') DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `candidate_id` binary(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `deleted` bit(1) NOT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` datetime(6) DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `provider` enum('EMAIL','FACEBOOK','GOOGLE','LINKEDIN') NOT NULL,
  `role` enum('ADMIN','CANDIDATE','RECRUITER') NOT NULL,
  `user_type` enum('ADMIN','CANDIDATE','RECRUITER') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `created_at`, `updated_at`, `deleted`, `deleted_at`, `email`, `email_verified_at`, `last_login`, `password`, `provider`, `role`, `user_type`) VALUES
(0x9e17f8dc71f643c28004cffa436baa93, '2025-11-24 18:06:27.000000', '2025-11-24 18:06:27.000000', b'0', NULL, 'luqnleng5@gmail.com', NULL, NULL, NULL, 'GOOGLE', 'CANDIDATE', 'CANDIDATE'),
(0x9fd1023308994824bb6da9f26beabf13, '2025-11-24 18:13:39.000000', '2025-11-24 18:13:39.000000', b'0', NULL, 'averelldalton2504@gmail.com', NULL, NULL, NULL, 'GOOGLE', 'CANDIDATE', 'CANDIDATE');

-- --------------------------------------------------------

--
-- Structure de la table `user_sessions`
--

CREATE TABLE `user_sessions` (
  `id` binary(16) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `device_info` varchar(255) DEFAULT NULL,
  `expired_at` datetime(6) DEFAULT NULL,
  `ip_address` varchar(255) DEFAULT NULL,
  `is_active` bit(1) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `user_id` binary(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user_sessions`
--

INSERT INTO `user_sessions` (`id`, `created_at`, `updated_at`, `device_info`, `expired_at`, `ip_address`, `is_active`, `token`, `user_id`) VALUES
(0x57daa4c5443f4b0998236bb187f92cc4, '2025-11-24 18:13:39.000000', '2025-11-24 18:13:39.000000', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-24 19:13:39.000000', '0:0:0:0:0:0:0:1', b'1', 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhdmVyZWxsZGFsdG9uMjUwNEBnbWFpbC5jb20iLCJyb2xlIjpbIkNBTkRJREFURSJdLCJpYXQiOjE3NjQwMDQ0MTksImV4cCI6MTc2NDA5MDgxOX0.RjWOscCgR2JC52-iQnI5IeZzKJqbHDAPV69HsjVfb5E', 0x9fd1023308994824bb6da9f26beabf13),
(0xe0a2b5f5db704313b844730c63af67e8, '2025-11-24 18:06:27.000000', '2025-11-24 18:09:59.000000', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-24 19:09:59.000000', '0:0:0:0:0:0:0:1', b'1', 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsdXFubGVuZzVAZ21haWwuY29tIiwicm9sZSI6WyJDQU5ESURBVEUiXSwiaWF0IjoxNzY0MDA0MTk5LCJleHAiOjE3NjQwOTA1OTl9.noT7MMqdyVExOMWsDNKzQpSRQ9cpptumCZBeIUezUeY', 0x9e17f8dc71f643c28004cffa436baa93);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKbigbiiy8iifquorgjvxockq5s` (`candidate_id`,`job_offer_id`),
  ADD KEY `FKikabhgl3ia44efd9qfx8g28j6` (`job_offer_id`);

--
-- Index pour la table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKdoi1o7iyehcrqrrrbxjostvv5` (`user_id`);

--
-- Index pour la table `education`
--
ALTER TABLE `education`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKnrikpllw36vuqeihc5ur19tvy` (`candidate_id`);

--
-- Index pour la table `email_otp`
--
ALTER TABLE `email_otp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_emailotp_email` (`email`);

--
-- Index pour la table `experience`
--
ALTER TABLE `experience`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK86hiusttkmjri79aaq768i0j3` (`candidate_id`);

--
-- Index pour la table `job_offer`
--
ALTER TABLE `job_offer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKmixspuwrg25qymhwv5k6mytgw` (`company_id`);

--
-- Index pour la table `job_preferences`
--
ALTER TABLE `job_preferences`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKnvexlhg48x64953a0bgp77l5p` (`candidate_id`);

--
-- Index pour la table `job_preferences_contract_types`
--
ALTER TABLE `job_preferences_contract_types`
  ADD KEY `FKddnfcbtlslmj1c81pejbephjs` (`job_preferences_id`);

--
-- Index pour la table `job_preferences_sectors`
--
ALTER TABLE `job_preferences_sectors`
  ADD KEY `FKh22ofid78evyq4aa932avuixc` (`sector_id`),
  ADD KEY `FKiuhpfwg6lw8goeuskjigo81jn` (`job_preferences_id`);

--
-- Index pour la table `language`
--
ALTER TABLE `language`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKpsfy57hlwjiep5x3y8eyqgtp2` (`candidate_id`);

--
-- Index pour la table `recruiters`
--
ALTER TABLE `recruiters`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKlhuhr3tmewk16uubn7q6w28t6` (`user_id`),
  ADD KEY `FK4ypj6go37b5hrjhjsfl28rau8` (`sector_id`);

--
-- Index pour la table `saved_job_offers`
--
ALTER TABLE `saved_job_offers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UKdi40lkjc3xf3pc6x1e58l3oao` (`candidate_id`,`job_offer_id`),
  ADD KEY `FK163wmkbymiydh1ir5kjde0eqb` (`job_offer_id`);

--
-- Index pour la table `sector`
--
ALTER TABLE `sector`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `skill`
--
ALTER TABLE `skill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKkxy886wf7ie5kmx5e4vkcn6pb` (`candidate_id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `UK6dotkott2kjsp8vw4d0m25fb7` (`email`);

--
-- Index pour la table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK8klxsgb8dcjjklmqebqp1twd5` (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `email_otp`
--
ALTER TABLE `email_otp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `FKg4e16cwk1qrad923bpx4hamdh` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`),
  ADD CONSTRAINT `FKikabhgl3ia44efd9qfx8g28j6` FOREIGN KEY (`job_offer_id`) REFERENCES `job_offer` (`id`);

--
-- Contraintes pour la table `candidates`
--
ALTER TABLE `candidates`
  ADD CONSTRAINT `FKme4fkelukmx2s63tlcrft6hio` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Contraintes pour la table `education`
--
ALTER TABLE `education`
  ADD CONSTRAINT `FKnrikpllw36vuqeihc5ur19tvy` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `experience`
--
ALTER TABLE `experience`
  ADD CONSTRAINT `FK86hiusttkmjri79aaq768i0j3` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `job_offer`
--
ALTER TABLE `job_offer`
  ADD CONSTRAINT `FKmixspuwrg25qymhwv5k6mytgw` FOREIGN KEY (`company_id`) REFERENCES `recruiters` (`id`);

--
-- Contraintes pour la table `job_preferences`
--
ALTER TABLE `job_preferences`
  ADD CONSTRAINT `FKmiksqcnneg5r2lyq72wvh7w4n` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `job_preferences_contract_types`
--
ALTER TABLE `job_preferences_contract_types`
  ADD CONSTRAINT `FKddnfcbtlslmj1c81pejbephjs` FOREIGN KEY (`job_preferences_id`) REFERENCES `job_preferences` (`id`);

--
-- Contraintes pour la table `job_preferences_sectors`
--
ALTER TABLE `job_preferences_sectors`
  ADD CONSTRAINT `FKh22ofid78evyq4aa932avuixc` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`id`),
  ADD CONSTRAINT `FKiuhpfwg6lw8goeuskjigo81jn` FOREIGN KEY (`job_preferences_id`) REFERENCES `job_preferences` (`id`);

--
-- Contraintes pour la table `language`
--
ALTER TABLE `language`
  ADD CONSTRAINT `FKpsfy57hlwjiep5x3y8eyqgtp2` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `recruiters`
--
ALTER TABLE `recruiters`
  ADD CONSTRAINT `FK1edjvp9udx35rophqr7imremb` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `FK4ypj6go37b5hrjhjsfl28rau8` FOREIGN KEY (`sector_id`) REFERENCES `sector` (`id`);

--
-- Contraintes pour la table `saved_job_offers`
--
ALTER TABLE `saved_job_offers`
  ADD CONSTRAINT `FK163wmkbymiydh1ir5kjde0eqb` FOREIGN KEY (`job_offer_id`) REFERENCES `job_offer` (`id`),
  ADD CONSTRAINT `FKhh7wuufl6mhswp2im5xs861ws` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `skill`
--
ALTER TABLE `skill`
  ADD CONSTRAINT `FKkxy886wf7ie5kmx5e4vkcn6pb` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`);

--
-- Contraintes pour la table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD CONSTRAINT `FK8klxsgb8dcjjklmqebqp1twd5` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
