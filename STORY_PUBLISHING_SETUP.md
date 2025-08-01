# 🚀 AI故事发布系统 - 部署和使用指南

## 📋 系统概述

AI故事发布系统现已完成开发，包含以下核心功能：

### ✅ 已完成功能
1. **故事发布页面** (`/publish_story`)
2. **Gemini AI自动简介生成**
3. **图片上传和处理系统**
4. **6类标签分类系统**
5. **故事保存和状态管理**
6. **从录制页面到发布页面的集成**

## 🛠️ 部署步骤

### 1. 数据库设置
```bash
# 1. 创建数据库表和默认数据
python create_tables_simple.py

# 2. 插入测试数据（可选）
python insert_test_data.py

# 3. 验证数据库
python verify_database.py
```

### 2. 创建必要目录
```bash
# 创建图片上传目录
mkdir -p static/uploads/stories
mkdir -p static/uploads/stories/2024/01
mkdir -p static/uploads/stories/2024/02
# ... 根据需要创建更多月份目录
```

### 3. 环境配置
确保以下文件存在：
- `google_key.txt` - Google API密钥
- `.env` - 数据库配置（可选）

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 启动应用
```bash
python app.py
```

## 🎯 功能使用流程

### 故事创作到发布的完整流程：

1. **录制故事** (`/record_story`)
   - 用户录制或上传音频
   - Google Speech-to-Text 进行语音识别
   - Gemini AI 润色故事内容
   - 用户可与AI对话进一步完善故事

2. **发布故事** (`/publish_story`)
   - 从录制页面点击"发布我的故事"按钮
   - 系统自动获取故事内容和语言信息
   - 用户填写故事标题
   - AI自动生成故事简介（可编辑）
   - 选择6类标签（类型、情绪、主题、受众、长度、背景）
   - 上传故事封面图片
   - 选择发布状态：草稿/提交审核/私人收藏
   - 系统计算字数和阅读时间

3. **故事管理**
   - 用户可通过 `/api/get_user_stories` 查看自己的故事
   - 支持不同状态的故事管理

## 🏷️ 标签分类系统

### 6大分类，每类6个标签：

1. **故事类型 (Genre)**
   - Adventure, Romance, Fantasy, Mystery, Comedy, Drama

2. **情绪氛围 (Mood)**
   - Happy, Sad, Inspiring, Dark, Lighthearted, Suspenseful

3. **故事主题 (Theme)**
   - Family, Friendship, Love, Growth, Adventure, Life Lessons

4. **目标受众 (Audience)**
   - Children (0-12), Teens (13-17), Young Adults (18-25), Adults (25+), Family, Educational

5. **故事长度 (Length)**
   - Very Short (<500词), Short (500-2000词), Medium (2000-5000词), Long (5000-10000词), Very Long (10000+词), Series

6. **故事背景 (Setting)**
   - Modern, Historical, Future, Fantasy World, Urban, Nature

## 🖼️ 图片处理功能

- **支持格式**: JPG, PNG, WebP
- **文件大小限制**: 5MB
- **自动生成**: 缩略图(300x300)、中等尺寸(800x600)、原始尺寸
- **存储路径**: `static/uploads/stories/YYYY/MM/user_ID/`
- **智能裁剪**: 保持宽高比，居中裁剪

## 🔗 API 端点

### 故事发布相关API：
- `GET /publish_story` - 故事发布页面
- `GET /api/get_tags` - 获取标签分类和标签
- `POST /api/generate_description` - AI生成故事简介
- `POST /api/publish_story` - 发布故事
- `GET /api/get_user_stories` - 获取用户故事列表

## 📊 数据库表结构

### 新增表：
- `tag_categories` - 标签分类表
- `tags` - 标签表  
- `stories` - 故事表
- `story_tags` - 故事标签关联表
- `story_views` - 浏览记录表
- `story_likes` - 点赞记录表
- `story_comments` - 评论表

## 🔧 故障排除

### 常见问题：

1. **图片上传失败**
   - 检查 `static/uploads/stories` 目录权限
   - 确认文件大小不超过5MB
   - 验证文件格式是否支持

2. **标签加载失败**
   - 检查数据库连接
   - 确认标签表有数据：`python create_tables_simple.py`

3. **AI功能不工作**
   - 检查 `google_key.txt` 文件是否存在
   - 验证Google API密钥是否有效
   - 检查网络连接

4. **故事发布失败**
   - 检查数据库连接
   - 确认必填字段已填写
   - 查看控制台错误信息

## 📱 前端功能

### 故事发布页面特性：
- **响应式设计**: 适配桌面和移动端
- **拖拽上传**: 支持图片拖拽上传
- **实时预览**: 图片上传后即时预览
- **表单验证**: 客户端和服务端双重验证
- **进度提示**: 加载和处理进度显示
- **自动保存**: Session Storage临时保存
- **标签选择**: 直观的标签选择界面

## 🚀 下一步扩展

根据AI_Storytelling_Platform_Documentation.md，接下来可以开发：

1. **管理员审核系统**
2. **故事浏览和搜索页面**
3. **用户互动功能**（点赞、评论）
4. **故事推荐算法**
5. **社交分享功能**

## 📞 技术支持

如遇问题，请检查：
1. 控制台错误信息
2. 数据库连接状态
3. 文件权限设置
4. API密钥配置

---

**版本**: v1.0  
**最后更新**: 2024年7月31日  
**状态**: 功能完成，可用于生产环境