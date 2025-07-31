# Story Publishing System Documentation

## Overview

The Story Publishing System is a comprehensive feature that allows users to publish, manage, and share their stories with rich metadata, categorization, and multimedia support.

## Features

### Core Features
1. **Story Creation & Publishing**
   - Rich text story content
   - Dynamic title management
   - Auto-save drafts
   - Publication status control

2. **Language Detection & Management**
   - Automatic language detection using Google Language Detection API
   - Language-based story categorization
   - Multi-language support

3. **AI-Powered Descriptions**
   - Auto-generated story descriptions using Gemini AI
   - User-editable descriptions
   - SEO-friendly summaries

4. **Advanced Tagging System**
   - Hierarchical tag categories
   - Pre-defined tag library
   - Custom tag creation
   - Tag-based filtering and search

5. **Media Support**
   - Image upload and management
   - Image optimization and resizing
   - Multiple format support (JPEG, PNG, WebP)

6. **Analytics & Engagement**
   - View tracking
   - Like system
   - Comment system
   - Reading time estimation

## Database Schema

### Core Tables

#### 1. Stories Table
```sql
stories (
    id, user_id, title, content, language, language_name,
    description, image_path, reading_time, word_count,
    status, view_count, like_count, created_at, updated_at, published_at
)
```

#### 2. Tag System
```sql
tag_categories (id, name, description, color, icon)
tags (id, name, category_id, usage_count)
story_tags (story_id, tag_id) -- Junction table
```

#### 3. Engagement Tables
```sql
story_views (story_id, user_id, ip_address, viewed_at)
story_likes (story_id, user_id, created_at)
story_comments (story_id, user_id, content, parent_id)
```

### Tag Categories

The system includes 6 pre-defined tag categories:

1. **Genre** - Adventure, Romance, Mystery, Fantasy, Sci-Fi, Horror, Comedy, Drama, Thriller, Historical
2. **Mood** - Happy, Sad, Inspiring, Dark, Lighthearted, Nostalgic, Suspenseful, Peaceful
3. **Theme** - Family, Friendship, Coming of Age, Love, Loss, Identity, Justice, Freedom, Survival, Redemption
4. **Audience** - Children, Young Adult, Adult, Family Friendly, Educational
5. **Length** - Flash Fiction, Short Story, Novelette, Novella, Novel
6. **Setting** - Modern Day, Medieval, Future, Ancient, Urban, Rural, Fantasy World, Space

## File Structure

```
story_publishing/
├── models/
│   ├── story.py              # Story model and database operations
│   ├── tag.py                # Tag and category models
│   └── engagement.py         # Views, likes, comments models
├── services/
│   ├── language_service.py   # Google Language Detection integration
│   ├── description_service.py # Gemini description generation
│   ├── image_service.py      # Image upload and processing
│   └── search_service.py     # Story search and filtering
├── routes/
│   ├── story_routes.py       # Story CRUD API endpoints
│   ├── tag_routes.py         # Tag management endpoints
│   └── publish_routes.py     # Publishing workflow endpoints
├── templates/
│   ├── publish_story.html    # Story publishing page
│   ├── story_browser.html    # Story browsing and search
│   ├── story_detail.html     # Individual story view
│   └── my_stories.html       # User's story management
└── static/
    ├── css/story_styles.css  # Story-specific styles
    ├── js/story_editor.js    # Rich text editor
    ├── js/tag_manager.js     # Tag selection interface
    └── uploads/stories/      # Story image storage
```

## API Endpoints

### Story Management
- `POST /api/stories` - Create new story
- `GET /api/stories/{id}` - Get story details
- `PUT /api/stories/{id}` - Update story
- `DELETE /api/stories/{id}` - Delete story
- `POST /api/stories/{id}/publish` - Publish story
- `POST /api/stories/{id}/unpublish` - Unpublish story

### Language & Description
- `POST /api/detect-language` - Detect story language
- `POST /api/generate-description` - Generate AI description
- `GET /api/languages` - Get supported languages

### Tags & Categories
- `GET /api/tag-categories` - Get all tag categories
- `GET /api/tags` - Get tags by category
- `POST /api/tags` - Create custom tag
- `GET /api/stories/{id}/tags` - Get story tags
- `POST /api/stories/{id}/tags` - Add tags to story

### Media Upload
- `POST /api/upload-story-image` - Upload story image
- `DELETE /api/story-image/{id}` - Delete story image

### Search & Browse
- `GET /api/stories/search` - Search stories
- `GET /api/stories/browse` - Browse with filters
- `GET /api/stories/by-language/{lang}` - Get stories by language
- `GET /api/stories/by-tag/{tag}` - Get stories by tag

### Analytics
- `POST /api/stories/{id}/view` - Record story view
- `POST /api/stories/{id}/like` - Like/unlike story
- `GET /api/stories/{id}/stats` - Get story statistics

## Image Storage Strategy

### Recommended Approach: File System Storage

**Benefits:**
- Fast access and serving
- Easy backup and migration
- No database bloat
- Direct web server serving

**Directory Structure:**
```
static/uploads/stories/
├── 2024/
│   ├── 01/
│   │   ├── user_123/
│   │   │   ├── story_456_thumb.jpg
│   │   │   ├── story_456_medium.jpg
│   │   │   └── story_456_original.jpg
```

**Implementation:**
- Store images in date-based folders
- Generate multiple sizes (thumbnail, medium, original)
- Store relative path in database
- Use unique filenames to prevent conflicts

### Alternative: Cloud Storage
For production deployments, consider:
- AWS S3
- Google Cloud Storage
- Cloudinary (with automatic optimization)

## Frontend Components

### Story Publishing Page
```javascript
// Key components
- Rich Text Editor (TinyMCE or Quill)
- Tag Selection Interface
- Image Upload with Preview
- Auto-save Functionality
- Language Detection Display
- Description Generator
- Publication Controls
```

### Tag Management Interface
```javascript
// Features
- Category-based tag organization
- Visual tag selection with colors
- Search and filter tags
- Custom tag creation
- Tag popularity indicators
```

## Security Considerations

### Input Validation
- Sanitize all user input
- Validate story content length
- Check image file types and sizes
- Prevent SQL injection in search

### File Upload Security
- Validate file types (whitelist)
- Limit file sizes
- Scan for malware
- Generate unique filenames
- Store outside web root

### Access Control
- Users can only edit their own stories
- Private stories hidden from public
- Admin moderation capabilities
- Rate limiting on uploads

## Performance Optimization

### Database Indexes
- Full-text search on title, content, description
- Indexes on user_id, language, status, created_at
- Composite indexes for common query patterns

### Caching Strategy
- Redis cache for popular stories
- Browser cache for images
- CDN for static assets

### Search Optimization
- Elasticsearch for advanced search (optional)
- Full-text MySQL search for basic needs
- Tag-based filtering with proper indexes

## Implementation Phases

### Phase 1: Core Publishing
1. Database schema creation
2. Basic story CRUD operations
3. Simple publishing interface
4. Image upload functionality

### Phase 2: AI Features
1. Google Language Detection integration
2. Gemini description generation
3. Auto-categorization suggestions

### Phase 3: Advanced Features
1. Rich tag system implementation
2. Advanced search and filtering
3. Analytics and engagement tracking

### Phase 4: Polish & Optimization
1. Performance optimization
2. Advanced caching
3. Mobile responsiveness
4. SEO optimization

## Testing Strategy

### Unit Tests
- Story model validation
- Tag assignment logic
- Image processing functions
- Language detection accuracy

### Integration Tests
- API endpoint functionality
- Database transaction handling
- File upload workflows
- Search result accuracy

### User Acceptance Tests
- Publishing workflow
- Tag selection experience
- Image upload process
- Story browsing functionality

## Future Enhancements

### Content Features
- Story series/collections
- Collaborative writing
- Version history
- Story templates

### Social Features
- User following system
- Story recommendations
- Reading lists/favorites
- Social sharing integration

### Advanced AI
- Content quality scoring
- Plagiarism detection
- Reading difficulty analysis
- Personalized recommendations

---

## Getting Started

1. **Run Database Setup:**
   ```bash
   mysql -u username -p database_name < create_story_tables.sql
   ```

2. **Install Dependencies:**
   ```bash
   pip install google-cloud-translate pillow
   ```

3. **Configure Environment:**
   ```bash
   export GOOGLE_CLOUD_CREDENTIALS_PATH=/path/to/credentials.json
   export STORY_UPLOAD_PATH=/path/to/uploads
   ```

4. **Start Development:**
   - Implement Story model class
   - Create publishing page frontend
   - Add API endpoints
   - Test with sample data

This documentation provides a comprehensive roadmap for implementing the story publishing system with all requested features and room for future growth.