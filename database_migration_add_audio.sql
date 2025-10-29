-- ============================================
-- Database Migration: Add Audio Fields to Stories Table
-- Date: 2024-10-23
-- Description: Add audio file support for story recordings
-- ============================================

-- Add audio-related columns to stories table
ALTER TABLE stories
ADD COLUMN audio_path VARCHAR(255) DEFAULT NULL COMMENT '音频文件相对路径',
ADD COLUMN audio_original_name VARCHAR(255) DEFAULT NULL COMMENT '原始音频文件名',
ADD COLUMN audio_duration INT DEFAULT NULL COMMENT '音频时长(秒)',
ADD COLUMN audio_format VARCHAR(10) DEFAULT NULL COMMENT '音频格式(webm/mp3/wav等)';

-- Verify the changes
SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'stories'
AND COLUMN_NAME IN ('audio_path', 'audio_original_name', 'audio_duration', 'audio_format');

-- Example of expected result:
-- +---------------------+-----------+---------------------------+
-- | COLUMN_NAME         | DATA_TYPE | COLUMN_COMMENT            |
-- +---------------------+-----------+---------------------------+
-- | audio_path          | varchar   | 音频文件相对路径          |
-- | audio_original_name | varchar   | 原始音频文件名            |
-- | audio_duration      | int       | 音频时长(秒)              |
-- | audio_format        | varchar   | 音频格式(webm/mp3/wav等)  |
-- +---------------------+-----------+---------------------------+
