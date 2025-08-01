-- Story Publishing System Database Schema
-- This file creates all necessary tables for the story publishing feature

-- =====================================================
-- 1. Tag Categories Table
-- =====================================================
CREATE TABLE IF NOT EXISTS tag_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7) DEFAULT '#6c757d', -- Hex color for UI display
    icon VARCHAR(50) DEFAULT 'fas fa-tag', -- FontAwesome icon class
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default tag categories
INSERT INTO tag_categories (name, description, color, icon) VALUES
('Genre', 'Story genres and types', '#007bff', 'fas fa-book'),
('Mood', 'Emotional tone and atmosphere', '#28a745', 'fas fa-heart'),
('Theme', 'Central themes and topics', '#ffc107', 'fas fa-lightbulb'),
('Audience', 'Target audience and age groups', '#17a2b8', 'fas fa-users'),
('Length', 'Story length categories', '#6f42c1', 'fas fa-clock'),
('Setting', 'Time period and location', '#fd7e14', 'fas fa-map-marker-alt');

-- =====================================================
-- 2. Tags Table
-- =====================================================
CREATE TABLE IF NOT EXISTS tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    description TEXT,
    usage_count INT DEFAULT 0, -- Track how many stories use this tag
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES tag_categories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_tag_per_category (name, category_id)
);

-- Insert simplified default tags for each category (6 core tags per category)
-- Genre tags (6 main genres)
INSERT INTO tags (name, category_id, description) VALUES
('Adventure', 1, 'Exciting journeys and quests'),
('Romance', 1, 'Love stories and relationships'),
('Fantasy', 1, 'Magical and supernatural elements'),
('Mystery', 1, 'Puzzles and unknown elements'),
('Comedy', 1, 'Humorous and funny stories'),
('Drama', 1, 'Serious and emotional narratives');

-- Mood tags (6 main moods)
INSERT INTO tags (name, category_id, description) VALUES
('Happy', 2, 'Joyful and uplifting stories'),
('Sad', 2, 'Melancholic and emotional stories'),
('Inspiring', 2, 'Motivational and uplifting content'),
('Dark', 2, 'Serious and somber tone'),
('Lighthearted', 2, 'Fun and carefree atmosphere'),
('Suspenseful', 2, 'Tense and exciting mood');

-- Theme tags (6 main themes)
INSERT INTO tags (name, category_id, description) VALUES
('Family', 3, 'Family relationships and bonds'),
('Friendship', 3, 'Bonds between friends'),
('Love', 3, 'Romantic and platonic love'),
('Growth', 3, 'Personal development and coming of age'),
('Adventure', 3, 'Exploration and discovery'),
('Life Lessons', 3, 'Moral and educational themes');

-- Audience tags (6 age groups)
INSERT INTO tags (name, category_id, description) VALUES
('Children', 4, 'Suitable for young children (0-12)'),
('Teens', 4, 'For teenage readers (13-17)'),
('Young Adults', 4, 'For young adults (18-25)'),
('Adults', 4, 'Mature content for adults (25+)'),
('Family', 4, 'Appropriate for all ages'),
('Educational', 4, 'Learning and instructional content');

-- Length tags (6 length categories)
INSERT INTO tags (name, category_id, description) VALUES
('Very Short', 5, 'Under 500 words'),
('Short', 5, '500-2000 words'),
('Medium', 5, '2000-5000 words'),
('Long', 5, '5000-10000 words'),
('Very Long', 5, '10000+ words'),
('Series', 5, 'Multi-part story series');

-- Setting tags (6 main settings)
INSERT INTO tags (name, category_id, description) VALUES
('Modern', 6, 'Contemporary present day'),
('Historical', 6, 'Past time periods'),
('Future', 6, 'Futuristic or sci-fi setting'),
('Fantasy World', 6, 'Imaginary or magical realms'),
('Urban', 6, 'City and metropolitan areas'),
('Nature', 6, 'Countryside, forests, outdoors');

-- =====================================================
-- 3. Stories Table (Main stories table)
-- =====================================================
CREATE TABLE IF NOT EXISTS stories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    language VARCHAR(10) NOT NULL, -- ISO language code (en-US, zh-CN, etc.)
    language_name VARCHAR(50), -- Human readable language name
    description TEXT, -- Short description/summary
    image_path VARCHAR(500), -- Path to uploaded image
    image_original_name VARCHAR(255), -- Original filename
    reading_time INT, -- Estimated reading time in minutes
    word_count INT, -- Number of words in the story
    status ENUM('draft', 'pending', 'published', 'rejected', 'private', 'archived') DEFAULT 'draft',
    view_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_language (language),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_published_at (published_at),
    FULLTEXT(title, content, description) -- For full-text search
);

-- =====================================================
-- 4. Story Tags Junction Table (Many-to-Many)
-- =====================================================
CREATE TABLE IF NOT EXISTS story_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    story_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE KEY unique_story_tag (story_id, tag_id)
);

-- =====================================================
-- 5. Story Views Table (Optional - for analytics)
-- =====================================================
CREATE TABLE IF NOT EXISTS story_views (
    id INT PRIMARY KEY AUTO_INCREMENT,
    story_id INT NOT NULL,
    user_id INT NULL, -- NULL for anonymous views
    ip_address VARCHAR(45), -- Store IP for anonymous tracking
    user_agent TEXT,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_story_id (story_id),
    INDEX idx_viewed_at (viewed_at)
);

-- =====================================================
-- 6. Story Likes Table (Optional - for user engagement)
-- =====================================================
CREATE TABLE IF NOT EXISTS story_likes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    story_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_story_like (story_id, user_id)
);

-- =====================================================
-- 7. Comments Table (Optional - for user feedback)
-- =====================================================
CREATE TABLE IF NOT EXISTS story_comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    story_id INT NOT NULL,
    user_id INT NOT NULL,
    parent_id INT NULL, -- For threaded comments/replies
    content TEXT NOT NULL,
    status ENUM('published', 'pending', 'hidden') DEFAULT 'published',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES story_comments(id) ON DELETE CASCADE,
    INDEX idx_story_id (story_id),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- Triggers to update tag usage count
-- =====================================================
DELIMITER $$

CREATE TRIGGER after_story_tag_insert
    AFTER INSERT ON story_tags
    FOR EACH ROW
BEGIN
    UPDATE tags SET usage_count = usage_count + 1 WHERE id = NEW.tag_id;
END$$

CREATE TRIGGER after_story_tag_delete
    AFTER DELETE ON story_tags
    FOR EACH ROW
BEGIN
    UPDATE tags SET usage_count = usage_count - 1 WHERE id = OLD.tag_id;
END$$

DELIMITER ;

-- =====================================================
-- Sample Data for Testing (Optional)
-- =====================================================
-- Uncomment the following lines to insert sample data

/*
-- Sample story (assuming user with id=1 exists)
INSERT INTO stories (user_id, title, content, language, language_name, description, word_count, reading_time, status, published_at) VALUES
(1, 'The Magical Forest Adventure', 'Once upon a time, in a land far away, there was a magical forest filled with talking animals and enchanted trees. A young girl named Luna discovered this forest during her summer vacation and embarked on an incredible adventure that would change her life forever...', 'en-US', 'English', 'A young girl discovers a magical forest and goes on an adventure with talking animals.', 150, 1, 'published', NOW());

-- Add tags to the sample story
INSERT INTO story_tags (story_id, tag_id) VALUES
(1, 1), -- Adventure
(1, 4), -- Fantasy
(1, 11), -- Happy
(1, 15), -- Family
(1, 19), -- Children
(1, 25), -- Short Story
(1, 31); -- Fantasy World
*/