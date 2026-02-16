-- ================================================================
-- BASE DE DONNÉES : Agence de Location de Voitures
-- ================================================================

-- ================================================================
-- CRÉATION DES TABLES
-- ================================================================

CREATE TABLE IF NOT EXISTS Agences (
    id_agence INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    adresse TEXT NOT NULL,
    ville TEXT NOT NULL,
    telephone TEXT
);

CREATE TABLE IF NOT EXISTS Utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telephone TEXT,
    date_naissance DATE
);

CREATE TABLE IF NOT EXISTS Voitures (
    id_voiture INTEGER PRIMARY KEY,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    annee INTEGER,
    categorie TEXT NOT NULL,
    prix_journalier REAL NOT NULL,
    id_agence INTEGER NOT NULL,
    FOREIGN KEY (id_agence) REFERENCES Agences(id_agence)
);

CREATE TABLE IF NOT EXISTS Option (
    id_option INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    description TEXT,
    prix_journalier REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS Location (
    id_location INTEGER PRIMARY KEY,
    id_utilisateur INTEGER NOT NULL,
    id_voiture INTEGER NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    statut TEXT DEFAULT 'en_cours',
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_voiture) REFERENCES Voitures(id_voiture)
);

CREATE TABLE IF NOT EXISTS Avis (
    id_avis INTEGER PRIMARY KEY,
    id_utilisateur INTEGER NOT NULL,
    id_voiture INTEGER NOT NULL,
    note INTEGER CHECK(note BETWEEN 1 AND 5),
    commentaire TEXT,
    date_avis DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_voiture) REFERENCES Voitures(id_voiture)
);

CREATE TABLE IF NOT EXISTS Facture (
    id_facture INTEGER PRIMARY KEY,
    id_location INTEGER NOT NULL,
    montant REAL NOT NULL,
    date_facture DATE,
    statut_paiement TEXT DEFAULT 'en_attente',
    FOREIGN KEY (id_location) REFERENCES Location(id_location)
);

CREATE TABLE IF NOT EXISTS Location_Option (
    id_location INTEGER NOT NULL,
    id_option INTEGER NOT NULL,
    PRIMARY KEY (id_location, id_option),
    FOREIGN KEY (id_location) REFERENCES Location(id_location),
    FOREIGN KEY (id_option) REFERENCES Option(id_option)
);

-- ================================================================
-- PEUPLEMENT DES TABLES
-- ================================================================

-- Agences
INSERT INTO Agences VALUES (1, 'AutoLoc Paris', '10 Rue de Rivoli', 'Paris', '0145678901');
INSERT INTO Agences VALUES (2, 'AutoLoc Lyon', '25 Avenue Jean Jaurès', 'Lyon', '0478901234');
INSERT INTO Agences VALUES (3, 'AutoLoc Marseille', '5 Boulevard du Prado', 'Marseille', '0491234567');

-- Utilisateurs
INSERT INTO Utilisateurs VALUES (1, 'Dupont', 'Marie', 'marie.dupont@email.com', '0612345678', '1995-03-15');
INSERT INTO Utilisateurs VALUES (2, 'Martin', 'Jean', 'jean.martin@email.com', '0623456789', '1990-07-22');
INSERT INTO Utilisateurs VALUES (3, 'Bernard', 'Sophie', 'sophie.bernard@email.com', '0634567890', '1998-11-08');
INSERT INTO Utilisateurs VALUES (4, 'Petit', 'Lucas', 'lucas.petit@email.com', '0645678901', '1985-01-30');
INSERT INTO Utilisateurs VALUES (5, 'Durand', 'Emma', 'emma.durand@email.com', '0656789012', '2000-06-17');
INSERT INTO Utilisateurs VALUES (6, 'Leroy', 'Thomas', 'thomas.leroy@email.com', '0667890123', '1992-09-25');

-- Voitures
INSERT INTO Voitures VALUES (1, 'Peugeot', '3008', 2022, 'SUV', 75.00, 1);
INSERT INTO Voitures VALUES (2, 'Renault', 'Clio', 2023, 'Citadine', 40.00, 1);
INSERT INTO Voitures VALUES (3, 'BMW', 'Série 3', 2021, 'Berline', 90.00, 2);
INSERT INTO Voitures VALUES (4, 'Citroën', 'Berlingo', 2022, 'Utilitaire', 55.00, 2);
INSERT INTO Voitures VALUES (5, 'Toyota', 'RAV4', 2023, 'SUV', 80.00, 3);
INSERT INTO Voitures VALUES (6, 'Volkswagen', 'Golf', 2022, 'Citadine', 45.00, 3);
INSERT INTO Voitures VALUES (7, 'Mercedes', 'Classe C', 2023, 'Berline', 95.00, 1);
INSERT INTO Voitures VALUES (8, 'Fiat', '500', 2021, 'Citadine', 35.00, 2);

-- Options
INSERT INTO Option VALUES (1, 'GPS', 'Système de navigation GPS', 5.00);
INSERT INTO Option VALUES (2, 'Siège bébé', 'Siège auto pour bébé', 8.00);
INSERT INTO Option VALUES (3, 'Assurance tous risques', 'Couverture complète', 15.00);
INSERT INTO Option VALUES (4, 'Conducteur additionnel', 'Ajout d''un conducteur supplémentaire', 10.00);
INSERT INTO Option VALUES (5, 'WiFi embarqué', 'Connexion internet dans le véhicule', 7.00);

-- Locations
INSERT INTO Location VALUES (1, 1, 1, '2025-01-10', '2025-01-15', 'terminee');
INSERT INTO Location VALUES (2, 1, 4, '2025-02-01', '2025-02-05', 'terminee');
INSERT INTO Location VALUES (3, 1, 5, '2025-03-10', '2025-03-14', 'terminee');
INSERT INTO Location VALUES (4, 1, 7, '2025-04-01', '2025-04-03', 'terminee');
INSERT INTO Location VALUES (5, 1, 2, '2025-05-15', '2025-05-18', 'terminee');
INSERT INTO Location VALUES (6, 2, 3, '2025-01-20', '2025-01-25', 'terminee');
INSERT INTO Location VALUES (7, 2, 6, '2025-03-05', '2025-03-08', 'terminee');
INSERT INTO Location VALUES (8, 3, 2, '2025-02-10', '2025-02-14', 'terminee');
INSERT INTO Location VALUES (9, 3, 5, '2025-04-20', '2025-04-25', 'en_cours');
INSERT INTO Location VALUES (10, 4, 1, '2025-01-05', '2025-01-08', 'terminee');
INSERT INTO Location VALUES (11, 4, 2, '2025-02-15', '2025-02-20', 'terminee');
INSERT INTO Location VALUES (12, 4, 3, '2025-03-01', '2025-03-05', 'terminee');
INSERT INTO Location VALUES (13, 4, 4, '2025-04-10', '2025-04-15', 'terminee');
INSERT INTO Location VALUES (14, 4, 6, '2025-05-01', '2025-05-05', 'terminee');
INSERT INTO Location VALUES (15, 5, 8, '2025-02-20', '2025-02-22', 'terminee');
INSERT INTO Location VALUES (16, 6, 7, '2025-03-15', '2025-03-20', 'annulee');

-- Avis
INSERT INTO Avis VALUES (1, 1, 1, 5, 'Excellent SUV, très confortable', '2025-01-16');
INSERT INTO Avis VALUES (2, 1, 4, 3, 'Utilitaire correct mais bruyant', '2025-02-06');
INSERT INTO Avis VALUES (3, 2, 3, 4, 'Belle berline, conduite agréable', '2025-01-26');
INSERT INTO Avis VALUES (4, 2, 6, 5, 'Parfaite petite citadine', '2025-03-09');
INSERT INTO Avis VALUES (5, 3, 2, 4, 'Bon rapport qualité-prix', '2025-02-15');
INSERT INTO Avis VALUES (6, 4, 1, 4, 'Très bon SUV pour la famille', '2025-01-09');
INSERT INTO Avis VALUES (7, 4, 3, 5, 'Excellente berline BMW', '2025-03-06');
INSERT INTO Avis VALUES (8, 5, 8, 2, 'Voiture un peu vieille', '2025-02-23');
INSERT INTO Avis VALUES (9, 1, 5, 4, 'Bon SUV Toyota', '2025-03-15');
INSERT INTO Avis VALUES (10, 4, 6, 3, 'Correct sans plus', '2025-05-06');

-- Factures
INSERT INTO Facture VALUES (1, 1, 375.00, '2025-01-15', 'payee');
INSERT INTO Facture VALUES (2, 2, 220.00, '2025-02-05', 'payee');
INSERT INTO Facture VALUES (3, 3, 320.00, '2025-03-14', 'payee');
INSERT INTO Facture VALUES (4, 4, 190.00, '2025-04-03', 'payee');
INSERT INTO Facture VALUES (5, 5, 120.00, '2025-05-18', 'payee');
INSERT INTO Facture VALUES (6, 6, 450.00, '2025-01-25', 'payee');
INSERT INTO Facture VALUES (7, 7, 135.00, '2025-03-08', 'payee');
INSERT INTO Facture VALUES (8, 8, 160.00, '2025-02-14', 'payee');
INSERT INTO Facture VALUES (9, 9, 400.00, '2025-04-25', 'en_attente');
INSERT INTO Facture VALUES (10, 10, 225.00, '2025-01-08', 'payee');
INSERT INTO Facture VALUES (11, 11, 200.00, '2025-02-20', 'payee');
INSERT INTO Facture VALUES (12, 12, 360.00, '2025-03-05', 'payee');
INSERT INTO Facture VALUES (13, 13, 275.00, '2025-04-15', 'payee');
INSERT INTO Facture VALUES (14, 14, 180.00, '2025-05-05', 'en_attente');
INSERT INTO Facture VALUES (15, 15, 70.00, '2025-02-22', 'payee');
INSERT INTO Facture VALUES (16, 16, 0.00, '2025-03-20', 'annulee');

-- Location_Option (table associative)
INSERT INTO Location_Option VALUES (1, 1);
INSERT INTO Location_Option VALUES (1, 3);
INSERT INTO Location_Option VALUES (2, 1);
INSERT INTO Location_Option VALUES (3, 3);
INSERT INTO Location_Option VALUES (4, 1);
INSERT INTO Location_Option VALUES (4, 4);
INSERT INTO Location_Option VALUES (6, 1);
INSERT INTO Location_Option VALUES (6, 2);
INSERT INTO Location_Option VALUES (6, 3);
INSERT INTO Location_Option VALUES (9, 5);
INSERT INTO Location_Option VALUES (10, 3);
INSERT INTO Location_Option VALUES (12, 1);
INSERT INTO Location_Option VALUES (13, 2);
INSERT INTO Location_Option VALUES (15, 1);
