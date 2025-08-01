# 故事传承 - AI 故事记录平台

一个基于 Flask 的 AI 驱动故事记录和分享平台，让用户可以录制、整理和分享他们的珍贵故事。

## 项目特色

🎙️ **多语言录音** - 支持多种语言的语音识别和转录  
🤖 **AI 智能处理** - 使用 Google Gemini AI 优化故事内容和生成描述  
🖼️ **智能配图** - 自动为故事生成合适的封面图片  
📖 **故事管理** - 完整的故事分类、发布和管理系统  
🎨 **现代设计** - 温暖怀旧的用户界面设计  

## 技术栈

- **后端**: Flask + Python 3.8+
- **数据库**: MySQL (Zeabur 云数据库)
- **前端**: Bootstrap 5 + JavaScript
- **AI 服务**: Google Gemini API
- **语音识别**: Google Speech-to-Text API
- **图像处理**: Pillow

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境配置

创建 `google_key.txt` 文件并添加您的 Google API 密钥。

### 3. 数据库初始化

运行数据库表创建脚本：

```bash
python create_tables_simple.py
```

插入初始标签数据：

```bash
python update_simple_tags.py
```

### 4. 启动应用

```bash
python app.py
```

访问 http://localhost:8080 查看应用。

## 项目结构

```
├── app.py                 # 主应用文件
├── templates/             # HTML 模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── login.html        # 登录页
│   ├── register.html     # 注册页
│   ├── record_story.html # 录制故事页
│   └── publish_story.html# 发布故事页
├── static/               # 静态文件
│   └── uploads/          # 上传文件存储
├── gemini_service.py     # AI 服务
├── speech_service.py     # 语音识别服务
├── image_service.py      # 图像处理服务
├── create_tables_simple.py  # 数据库表创建
└── update_simple_tags.py    # 标签数据初始化
```

## 主要功能

### 用户管理
- 用户注册和登录
- 个人资料管理
- 安全的会话管理

### 故事录制
- 多语言语音录制
- 实时语音转文字
- AI 智能内容优化

### 故事发布
- 简化的故事类型分类系统（8种类型）
- 自动生成故事描述
- 图片上传和处理
- 故事状态管理（草稿/待审核/已发布）

### 故事展示
- 精美的故事卡片展示
- 响应式设计
- 现代化的用户界面

## 数据库设计

项目使用 MySQL 数据库，包含以下主要表：

- `users` - 用户信息
- `stories` - 故事内容
- `tags` - 故事标签
- `tag_categories` - 标签分类
- `story_tags` - 故事标签关联
- `story_views` - 故事浏览记录
- `story_likes` - 故事点赞记录
- `story_comments` - 故事评论

## API 接口

- `GET /` - 首页
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /record_story` - 录制故事页面
- `GET /publish_story` - 发布故事页面
- `POST /api/publish_story` - 发布故事 API
- `GET /api/get_story_types` - 获取故事类型
- `POST /api/generate_description` - 生成故事描述

## 部署说明

1. 确保服务器环境支持 Python 3.8+
2. 安装所有依赖包
3. 配置 Google API 密钥
4. 设置数据库连接信息
5. 运行应用程序

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

## 许可证

MIT License

## 更新日志

### v1.0.0 (当前版本)
- ✅ 完成基础用户管理系统
- ✅ 实现多语言语音录制功能
- ✅ 集成 Google Gemini AI 服务
- ✅ 完成故事发布和管理系统
- ✅ 设计现代化用户界面
- ✅ 简化故事标签分类系统
- ✅ 实现图片上传和处理功能