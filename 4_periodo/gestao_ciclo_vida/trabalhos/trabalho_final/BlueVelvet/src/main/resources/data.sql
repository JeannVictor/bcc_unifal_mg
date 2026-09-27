-- Desabilitar verificação de foreign keys temporariamente
SET FOREIGN_KEY_CHECKS = 0;

-- Limpar dados existentes
TRUNCATE TABLE category;

-- Reabilitar verificação de foreign keys
SET FOREIGN_KEY_CHECKS = 1;

-- Resetar auto-increment
ALTER TABLE category AUTO_INCREMENT = 1;

-- Categorias Raiz (Top-Level)
INSERT INTO category (name, image, enabled, parent_id) VALUES
                                                           ('Music', 'music.jpg', true, NULL),
                                                           ('Books', 'books.jpg', true, NULL),
                                                           ('Instruments', 'instruments.jpg', true, NULL),
                                                           ('Merchandise', 'merchandise.jpg', true, NULL);

-- Subcategorias de Music (parent_id = 1)
INSERT INTO category (name, image, enabled, parent_id) VALUES
                                                           ('Vinyl', 'vinyl.jpg', true, 1),
                                                           ('CD', 'cd.jpg', true, 1),
                                                           ('MP3', 'mp3.jpg', true, 1),
                                                           ('Cassette', 'cassette.jpg', true, 1);

-- Subcategorias de Books (parent_id = 2)
INSERT INTO category (name, image, enabled, parent_id) VALUES
                                                           ('Music Theory', 'theory.jpg', true, 2),
                                                           ('Biographies', 'biographies.jpg', true, 2);

-- Subcategorias de Instruments (parent_id = 3)
INSERT INTO category (name, image, enabled, parent_id) VALUES
                                                           ('Acoustic Guitar', 'acoustic-guitar.jpg', true, 3),
                                                           ('Electric Guitar', 'electric-guitar.jpg', true, 3),
                                                           ('Bass', 'bass.jpg', true, 3),
                                                           ('Drums', 'drums.jpg', true, 3);

-- Subcategorias de Merchandise (parent_id = 4)
INSERT INTO category (name, image, enabled, parent_id) VALUES
                                                           ('T-Shirts', 'tshirts.jpg', true, 4),
                                                           ('Posters', 'posters.jpg', true, 4),
                                                           ('Accessories', 'accessories.jpg', true, 4);