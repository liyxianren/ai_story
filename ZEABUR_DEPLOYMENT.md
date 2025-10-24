# 🚀 Zeabur 云端部署指南

## 📋 部署前准备

### 1. 确认所有文件已提交

确保以下文件在您的代码仓库中：

✅ 核心文件：
- `app.py` - 主应用
- `config.py` - 配置文件
- `requirements.txt` - Python 依赖
- `audio_service.py` - 音频服务
- `image_service.py` - 图片服务
- `speech_service.py` - 语音服务
- `gemini_service.py` - Gemini AI 服务

✅ 模板文件：
- `templates/` 目录下所有 HTML 文件
- 特别确认：`story_detail.html` (包含音频播放器)

✅ 静态文件：
- `static/` 目录

✅ 数据库迁移：
- `database_migration_add_audio.sql`

❌ 不要提交：
- `.env` (包含敏感信息)
- `.env.local`
- `__pycache__/`
- `*.pyc`

---

## 🔧 Zeabur 环境变量配置

### 步骤 1: 登录 Zeabur 控制台

访问: https://zeabur.com/dashboard

### 步骤 2: 选择你的项目

找到 `echoverse` 项目 → 点击进入

### 步骤 3: 配置环境变量

在项目设置中，添加以下环境变量：

#### 必需的环境变量

```bash
# Google API Key (必需)
GOOGLE_API_KEY=AIzaSyBf2A23x1m5tJ_SOUVVmJV2YzsPedi4qQc

# 数据库配置 (必需)
DB_HOST=tpe1.clusters.zeabur.com
DB_PORT=32149
DB_USER=root
DB_PASSWORD=69uc42U0oG7Js5Cm831ylixRqHODwXLI
DB_NAME=zeabur

# Flask 配置 (必需)
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key-here

# 上传目录 (可选，使用默认值)
UPLOAD_FOLDER=/image
AUDIO_UPLOAD_FOLDER=/video/stories
```

**⚠️ 重要提示**:
- 生成新的 SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
- 不要在代码中硬编码敏感信息

---

## 📦 依赖确认

确保 `requirements.txt` 包含以下内容：

```txt
# Core Flask dependencies
Flask==3.0.0
Flask-Login==0.6.3
Werkzeug==3.1.3

# Environment variables
python-dotenv>=1.0.0

# Database
PyMySQL>=1.0.0

# Authentication & Security
bcrypt>=4.0.0

# Image processing
Pillow>=10.0.0

# Audio processing
mutagen>=1.47.0

# External APIs
requests>=2.28.0
google-generativeai>=0.8.0
google-cloud-speech>=2.22.0

# Production server
gunicorn>=21.2.0
```

---

## 🗄️ 数据库迁移

### 执行音频字段迁移

在部署前或部署后，需要执行数据库迁移：

```bash
# 方式 1: 使用 MySQL 客户端
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur < database_migration_add_audio.sql

# 方式 2: 直接执行 SQL
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur
```

然后复制并执行 SQL：
```sql
ALTER TABLE stories
ADD COLUMN audio_path VARCHAR(255) DEFAULT NULL COMMENT '音频文件相对路径',
ADD COLUMN audio_original_name VARCHAR(255) DEFAULT NULL COMMENT '原始音频文件名',
ADD COLUMN audio_duration INT DEFAULT NULL COMMENT '音频时长(秒)',
ADD COLUMN audio_format VARCHAR(10) DEFAULT NULL COMMENT '音频格式';
```

验证：
```sql
DESCRIBE stories;
-- 应该看到 audio_path, audio_original_name, audio_duration, audio_format 字段
```

---

## 📁 创建必要的目录

Zeabur 上需要创建存储目录：

### 方式 1: 使用 Zeabur SSH (推荐)

```bash
# 连接到 Zeabur 容器
# (Zeabur Dashboard → Service → Terminal)

mkdir -p /image/stories
mkdir -p /video/stories

chmod -R 755 /image
chmod -R 755 /video
```

### 方式 2: 代码中自动创建

`app.py` 已包含自动创建目录的代码：
```python
if __name__ == '__main__':
    # Create upload folder for profile pictures
    os.makedirs('/image', exist_ok=True)
    # Audio service 会自动创建 /video/stories
```

---

## 🚀 部署步骤

### 1. Push 代码到 Git

```bash
# 确保所有更改已提交
git status

# 添加新文件
git add .

# 提交
git commit -m "feat: Add audio recording save and playback feature

- Add audio_service.py for audio file management
- Add mutagen for accurate duration calculation
- Update story_detail.html with English audio player
- Add database migration for audio fields
- Add file deletion on story removal"

# 推送到远程仓库
git push origin main
```

### 2. Zeabur 自动部署

Zeabur 会自动检测到代码更新并开始部署：

1. **监控部署**:
   - 进入 Zeabur Dashboard
   - 查看 "Deployments" 标签
   - 查看构建日志

2. **检查日志**:
   ```
   Building Python application...
   Installing dependencies from requirements.txt...
   Starting gunicorn server...
   ```

3. **等待部署完成**:
   - 通常需要 2-5 分钟
   - 部署成功后状态变为 "Running"

---

## ✅ 部署后验证

### 1. 检查应用状态

访问: https://echoverse.zeabur.app

应该能正常访问主页

### 2. 测试音频功能

#### 测试录音

1. 访问: https://echoverse.zeabur.app/record
2. 登录
3. 录制一段音频
4. 点击转录
5. **检查**:
   - 转录成功
   - 浏览器控制台没有错误
   - sessionStorage 中有音频信息

#### 测试发布

1. 从录音页面跳转到发布页面
2. **检查**:
   - 显示音频预览播放器
   - 可以播放音频
3. 填写标题、描述
4. 点击发布
5. **检查**:
   - 发布成功
   - 跳转到"我的故事"页面

#### 测试详情页

1. 从"我的故事"点击查看详情
2. **检查**:
   - 显示英文音频播放器: "Listen to Original Recording"
   - 显示准确的时长: "Duration: X seconds"
   - 可以正常播放音频
   - 音频时长准确（误差不超过1秒）

### 3. 检查日志

在 Zeabur Dashboard → Service → Logs 中查看：

```
INFO:__main__:Accurate audio duration: X seconds
INFO:audio_service:Saved audio file: /video/stories/...
INFO:__main__:Story inserted with ID: XX
```

### 4. 验证数据库

```sql
-- 连接到数据库
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur

-- 查询最新故事
SELECT id, title, audio_path, audio_duration, audio_format
FROM stories
ORDER BY created_at DESC
LIMIT 5;

-- 应该看到音频信息已保存
```

### 5. 验证文件存储

在 Zeabur Terminal 中：
```bash
# 检查音频文件
ls -lh /video/stories/2025/10/user_*/
# 应该看到 .webm 文件

# 检查文件权限
ls -ld /video/stories
# 应该是 drwxr-xr-x
```

---

## 🐛 故障排查

### 问题 1: 应用无法启动

**症状**: Zeabur 显示 "Failed" 或 "Crashed"

**检查**:
1. 查看 Zeabur 构建日志
2. 检查 `requirements.txt` 是否正确
3. 验证环境变量是否设置

**常见原因**:
- Python 版本不兼容
- 依赖安装失败
- 缺少环境变量

**解决**:
```bash
# 本地测试
pip install -r requirements.txt
python app.py
```

### 问题 2: 数据库连接失败

**症状**: 日志显示 "Can't connect to MySQL server"

**检查**:
1. 环境变量是否正确
2. 数据库服务是否运行
3. 防火墙规则

**解决**:
```python
# 在 Zeabur Terminal 测试
python -c "
import pymysql
conn = pymysql.connect(
    host='tpe1.clusters.zeabur.com',
    port=32149,
    user='root',
    password='your_password',
    database='zeabur'
)
print('Connected!')
"
```

### 问题 3: 音频保存失败

**症状**: 转录成功但没有音频信息返回

**检查**:
1. 目录权限
2. 磁盘空间
3. mutagen 是否安装

**解决**:
```bash
# 检查目录
ls -ld /video/stories
# 修复权限
chmod -R 755 /video/stories

# 检查磁盘空间
df -h

# 验证 mutagen
python -c "from mutagen import File; print('OK')"
```

### 问题 4: 音频无法播放

**症状**: 播放器显示但无法播放

**检查**:
1. 浏览器控制台错误
2. Network 标签中音频请求状态
3. 音频文件路径

**解决**:
- 检查 `/video/stories` 路由是否正确
- 验证文件确实存在
- 检查文件权限 (应该是 644)

### 问题 5: GOOGLE_API_KEY 未设置

**症状**: "GOOGLE_API_KEY environment variable not found"

**解决**:
1. 进入 Zeabur Dashboard
2. Service → Environment Variables
3. 添加 `GOOGLE_API_KEY`
4. 重新部署

---

## 📊 性能监控

### 推荐监控指标

1. **应用健康**:
   - CPU使用率
   - 内存使用
   - 响应时间

2. **数据库**:
   - 连接数
   - 查询时间
   - 慢查询

3. **存储**:
   - 磁盘使用率
   - 文件数量
   - 上传/下载速度

### Zeabur 内置监控

访问: Zeabur Dashboard → Service → Metrics

---

## 🔄 更新部署

### 常规更新

```bash
# 1. 修改代码
# 2. 提交更改
git add .
git commit -m "Update: ..."
git push

# Zeabur 会自动重新部署
```

### 回滚部署

```bash
# 在 Zeabur Dashboard
Deployments → 选择之前的版本 → Redeploy
```

### 数据库迁移

```bash
# 如果有新的数据库更改
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur < new_migration.sql
```

---

## 📝 环境变量完整列表

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `GOOGLE_API_KEY` | ✅ | 无 | Google API 密钥 |
| `DB_HOST` | ✅ | 无 | 数据库主机 |
| `DB_PORT` | ✅ | 无 | 数据库端口 |
| `DB_USER` | ✅ | 无 | 数据库用户 |
| `DB_PASSWORD` | ✅ | 无 | 数据库密码 |
| `DB_NAME` | ✅ | 无 | 数据库名称 |
| `FLASK_ENV` | ⚠️ | development | 环境模式 |
| `SECRET_KEY` | ⚠️ | 随机生成 | Flask 密钥 |
| `UPLOAD_FOLDER` | ❌ | /image | 图片目录 |
| `AUDIO_UPLOAD_FOLDER` | ❌ | /video/stories | 音频目录 |

---

## 🎯 部署检查清单

- [ ] 代码已推送到 Git
- [ ] requirements.txt 完整
- [ ] 环境变量已配置
- [ ] 数据库迁移已执行
- [ ] 目录权限正确
- [ ] Zeabur 部署成功
- [ ] 主页可访问
- [ ] 录音功能正常
- [ ] 转录功能正常
- [ ] 音频保存成功
- [ ] 发布页面预览正常
- [ ] 故事发布成功
- [ ] 详情页音频播放正常
- [ ] 时长显示准确
- [ ] 界面为英文

---

## 📞 支持

如遇问题：

1. **查看日志**: Zeabur Dashboard → Logs
2. **检查文档**: 本文档 + AUDIO_FEATURE_IMPLEMENTATION.md
3. **数据库检查**: 直接连接数据库验证
4. **文件检查**: 使用 Zeabur Terminal 检查文件

---

## 🎉 部署成功！

完成所有检查清单后，你的音频功能就成功部署到云端了！

用户现在可以：
- 🎙️ 录制故事音频
- 📝 转录为文字
- 💾 保存音频文件
- 🎧 在详情页听原声
- ⏱️ 看到准确的时长
- 🌍 使用英文界面

Enjoy your deployed application! 🚀
