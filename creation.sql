use TTMS;
show tables;

CREATE TABLE Player (
    player_id     INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    playing_style VARCHAR(20)  NOT NULL,
    grip_type     VARCHAR(20)  NOT NULL
);
 
CREATE TABLE Blade (
    blade_id   INT AUTO_INCREMENT PRIMARY KEY,
    brand      VARCHAR(80)   NOT NULL,
    model      VARCHAR(100)  NOT NULL,
    ply_count  INT,
    weight     DECIMAL(5,1),
    material   VARCHAR(50),
    price      DECIMAL(10,2) NOT NULL
);
 
CREATE TABLE Rubber (
    rubber_id  INT AUTO_INCREMENT PRIMARY KEY,
    brand      VARCHAR(80)   NOT NULL,
    model      VARCHAR(100)  NOT NULL,
    sponge     VARCHAR(20),
    price      DECIMAL(10,2) NOT NULL
);
 
CREATE TABLE Glue (
    glue_id   INT AUTO_INCREMENT PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    brand     VARCHAR(80)  NOT NULL,
    price     DECIMAL(10,2) NOT NULL
);

CREATE TABLE Setup (
    setup_id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    player_id           INT NOT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    blade_id            INT NOT NULL,
    rubber_id           INT,
    forehand_rubber_id  INT NOT NULL,
    backhand_rubber_id  INT NOT NULL,
    glue_id             INT NOT NULL,
 
    CONSTRAINT fk_setup_player
        FOREIGN KEY (player_id) REFERENCES Player(player_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_setup_blade
        FOREIGN KEY (blade_id) REFERENCES Blade(blade_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_setup_rubber
        FOREIGN KEY (rubber_id) REFERENCES Rubber(rubber_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_setup_fh_rubber
        FOREIGN KEY (forehand_rubber_id) REFERENCES Rubber(rubber_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_setup_bh_rubber
        FOREIGN KEY (backhand_rubber_id) REFERENCES Rubber(rubber_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_setup_glue
        FOREIGN KEY (glue_id) REFERENCES Glue(glue_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

ALTER TABLE Player
    ADD CONSTRAINT chk_playing_style CHECK (playing_style IN ('offensive','defensive','all_round')),
    ADD CONSTRAINT chk_grip_type CHECK (grip_type IN ('shakehand','penhold')),
    MODIFY COLUMN grip_type VARCHAR(20) NOT NULL DEFAULT 'shakehand';

ALTER TABLE Blade
    ADD CONSTRAINT uq_blade_brand_model UNIQUE (brand, model),
    ADD CONSTRAINT chk_blade_price CHECK (price >= 0),
    ADD CONSTRAINT chk_blade_ply CHECK (ply_count IS NULL OR ply_count BETWEEN 1 AND 9),
    MODIFY COLUMN price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    ADD COLUMN discontinued BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE Rubber
    ADD CONSTRAINT uq_rubber_brand_model UNIQUE (brand, model),
    ADD CONSTRAINT chk_rubber_price CHECK (price >= 0),
    MODIFY COLUMN price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    ADD COLUMN discontinued BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE Glue
    ADD CONSTRAINT uq_glue_brand_name UNIQUE (brand, name),
    ADD CONSTRAINT chk_glue_price CHECK (price >= 0),
    MODIFY COLUMN price DECIMAL(10,2) NOT NULL DEFAULT 0.00;

ALTER TABLE Setup
    ADD CONSTRAINT uq_setup_weak_key UNIQUE (player_id, created_at),
    ADD COLUMN notes VARCHAR(255) DEFAULT NULL;

ALTER TABLE Blade RENAME COLUMN weight TO weight_g;
