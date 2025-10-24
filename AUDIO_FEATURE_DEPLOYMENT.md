# 🎙️ 音频功能部署与测试指南

## ✅ 代码实现完成状态

### 后端实现 (100% 完成)
- ✅ 数据库迁移文件: `database_migration_add_audio.sql`
- ✅ 音频服务模块: `audio_service.py` (完全参照 image_service.py)
- ✅ 配置文件: `config.py` (添加音频配置)
- ✅ Flask路由: `app.py` (所有必要的修改已完成)
  - 导入 audio_service
  - /video/stories 路由
  - /api/transcribe 保存音频
  - /api/publish_story 接收音频信息
  - story_detail 查询音频字段

### 前端实现 (100% 完成)
- ✅ `record_story.html` - 保存音频信息到 sessionStorage
- ✅ `publish_story.html` - 显示音频预览和提交音频信息
- ✅ `story_detail.html` - 显示音频播放器

---

## 📋 部署前检查清单

### 1. 服务器环境准备

#### 创建音频存储目录
```bash
# 创建音频存储目录
sudo mkdir -p /video/stories

# 设置正确的权限 (根据你的 Web 服务器用户调整)
sudo chown -R www-data:www-data /video/stories  # For Apache/Nginx
# 或者
sudo chown -R your_user:your_group /video/stories

# 设置目录权限
sudo chmod -R 755 /video/stories
```

#### 验证目录权限
```bash
# 验证目录存在且可写
ls -la /video/stories
touch /video/stories/test.txt && rm /video/stories/test.txt && echo "✅ 目录可写"
```

### 2. 数据库迁移

#### 连接到数据库
```bash
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur
```

#### 执行迁移 SQL
```sql
-- 方式 1: 直接复制粘贴
ALTER TABLE stories
ADD COLUMN audio_path VARCHAR(255) DEFAULT NULL COMMENT '音频文件相对路径',
ADD COLUMN audio_original_name VARCHAR(255) DEFAULT NULL COMMENT '原始音频文件名',
ADD COLUMN audio_duration INT DEFAULT NULL COMMENT '音频时长(秒)',
ADD COLUMN audio_format VARCHAR(10) DEFAULT NULL COMMENT '音频格式';

-- 验证字段已添加
DESCRIBE stories;
```

#### 或使用文件导入
```bash
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p zeabur < database_migration_add_audio.sql
```

#### 验证迁移成功
```sql
-- 检查新字段
SELECT COLUMN_NAME, DATA_TYPE, COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'stories'
AND COLUMN_NAME LIKE 'audio_%';

-- 应该看到 4 个字段:
-- audio_path
-- audio_original_name
-- audio_duration
-- audio_format
```

### 3. 部署代码文件

#### 上传新文件到服务器
```bash
# audio_service.py
scp audio_service.py user@your-server:/path/to/your/app/

# 或者如果使用 git
git add audio_service.py database_migration_add_audio.sql
git add config.py app.py
git add templates/record_story.html templates/publish_story.html templates/story_detail.html
git commit -m "Add audio recording save and playback feature"
git push
```

#### 确认所有文件已部署
```bash
# 在服务器上验证
ls -la audio_service.py
ls -la templates/record_story.html
ls -la templates/publish_story.html
ls -la templates/story_detail.html
```

### 4. 重启服务

```bash
# Zeabur 平台
# 在 Zeabur Dashboard 中点击重新部署

# 或者本地测试
python app.py
```

---

## 🧪 测试步骤

### 测试 1: 音频录制与保存

1. **访问录音页面**
   ```
   https://echoverse.zeabur.app/record
   ```

2. **录制测试音频**
   - 点击录音按钮
   - 说话 10-15 秒
   - 点击停止录音

3. **触发转录**
   - 点击 "转录" 按钮
   - 等待转录完成

4. **检查音频信息**
   - 打开浏览器控制台 (F12)
   - 查看 Network 标签中的 `/api/transcribe` 响应
   - 应该包含:
     ```json
     {
       "success": true,
       "text": "转录文本...",
       "audio_path": "2024/10/user_1/temp_xxx.webm",
       "audio_original_name": "recording.webm",
       "audio_duration": 12,
       "audio_format": "webm"
     }
     ```

5. **验证文件已保存**
   ```bash
   # 在服务器上检查
   ls -lh /video/stories/2024/10/user_*/temp_*.webm
   ```

### 测试 2: 发布页面音频预览

1. **点击 "发布故事" 按钮**
   - 从录音页面跳转到发布页面

2. **检查 sessionStorage**
   - 在浏览器控制台执行:
     ```javascript
     console.log(JSON.parse(sessionStorage.getItem('storyAudio')))
     ```
   - 应该输出音频信息对象

3. **验证音频预览播放器**
   - 页面应显示绿色的 "录音预览" 卡片
   - 音频播放器应可见
   - 点击播放按钮，应能听到刚才的录音
   - 检查显示的文件名和时长

4. **检查表单数据**
   - 打开控制台，在 publishStory 函数中添加断点
   - 或者查看 Network 标签
   - 提交表单时应包含:
     ```
     FormData:
       audio_path: "2024/10/user_1/temp_xxx.webm"
       audio_original_name: "recording.webm"
       audio_duration: "12"
       audio_format: "webm"
     ```

### 测试 3: 发布故事

1. **填写故事信息**
   - 标题、描述、内容
   - (可选) 上传封面图片

2. **提交故事**
   - 点击 "发布故事" 按钮
   - 应该成功发布

3. **验证数据库记录**
   ```sql
   SELECT id, title, audio_path, audio_original_name, audio_duration, audio_format
   FROM stories
   ORDER BY created_at DESC
   LIMIT 1;
   ```
   - 应该看到刚发布的故事，包含音频信息

### 测试 4: 故事详情页播放

1. **访问刚发布的故事**
   ```
   https://echoverse.zeabur.app/story/<story_id>
   ```

2. **检查音频播放器**
   - 页面顶部应显示绿色的 "🎧 收听故事原声" 卡片
   - HTML5 音频播放器应可见
   - 显示作者名、时长、格式信息

3. **播放音频**
   - 点击播放按钮
   - 应该能听到之前录制的音频
   - 检查音频URL:
     ```
     /video/stories/2024/10/user_1/temp_xxx.webm
     ```

4. **验证音频文件访问**
   - 在浏览器控制台查看 Network 标签
   - 音频请求应返回 200 状态码
   - Content-Type 应为 `audio/webm` 或相应格式

### 测试 5: 持久化测试

1. **重启服务器**
   ```bash
   # 重启应用
   systemctl restart your-app-service
   # 或在 Zeabur 上重新部署
   ```

2. **重新访问故事详情页**
   - 音频播放器应仍然显示
   - 音频应仍然可以播放

3. **验证文件未丢失**
   ```bash
   ls -lh /video/stories/2024/10/user_*/
   ```

---

## 🐛 故障排查

### 问题 1: 音频文件保存失败

**症状**: `/api/transcribe` 返回成功，但没有 audio_path

**检查**:
```bash
# 1. 检查目录是否存在
ls -la /video/stories

# 2. 检查权限
ls -ld /video/stories
# 应该显示 drwxr-xr-x 或类似权限

# 3. 检查磁盘空间
df -h /video

# 4. 查看应用日志
tail -f /var/log/your-app/error.log
# 或 Zeabur 平台日志
```

**解决**:
```bash
# 修复权限
sudo chown -R www-data:www-data /video/stories
sudo chmod -R 755 /video/stories
```

### 问题 2: 音频无法播放

**症状**: 播放器显示但点击播放无反应

**检查**:
1. 打开浏览器控制台
2. 查看 Network 标签
3. 找到音频请求 `/video/stories/...`
4. 检查状态码

**可能原因**:
- **404 Not Found**: 文件不存在或路径错误
  ```bash
  # 验证文件路径
  ls -la /video/stories/2024/10/user_1/
  ```

- **403 Forbidden**: 权限问题
  ```bash
  # 修复权限
  sudo chmod 644 /video/stories/2024/10/user_1/*.webm
  ```

- **500 Internal Server Error**: Flask 路由错误
  - 检查 app.py 中 serve_audio 路由
  - 查看应用日志

### 问题 3: 数据库字段不存在

**症状**: 发布故事时报错 "Unknown column 'audio_path'"

**检查**:
```sql
DESCRIBE stories;
```

**解决**:
```sql
-- 重新执行迁移
ALTER TABLE stories
ADD COLUMN audio_path VARCHAR(255) DEFAULT NULL,
ADD COLUMN audio_original_name VARCHAR(255) DEFAULT NULL,
ADD COLUMN audio_duration INT DEFAULT NULL,
ADD COLUMN audio_format VARCHAR(10) DEFAULT NULL;
```

### 问题 4: sessionStorage 数据丢失

**症状**: 发布页面没有显示音频预览

**检查**:
1. 打开控制台
2. 执行: `console.log(sessionStorage.getItem('storyAudio'))`

**可能原因**:
- 跨域问题 (不太可能，同域名)
- sessionStorage 被清除
- record_story.html 没有正确保存

**解决**:
- 确认 record_story.html 中 publishStoryToPublishPage 函数有保存代码
- 在录音页面控制台验证:
  ```javascript
  console.log(recorder.audioData)
  ```

---

## 📊 成功指标

测试通过标准:
- ✅ 录音后转录返回包含音频信息
- ✅ 音频文件保存到 /video/stories 目录
- ✅ 发布页面显示音频预览播放器
- ✅ 音频可以在预览中播放
- ✅ 故事发布成功，数据库包含音频字段
- ✅ 故事详情页显示音频播放器
- ✅ 音频可以在详情页播放
- ✅ 重启服务后音频仍可播放

---

## 🎯 快速测试命令集

```bash
# === 服务器端快速验证 ===

# 1. 检查音频目录
ls -la /video/stories

# 2. 检查数据库
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p -e "DESCRIBE zeabur.stories" | grep audio

# 3. 检查最新音频文件
find /video/stories -type f -name "*.webm" -mmin -10

# 4. 检查最新故事的音频信息
mysql -h tpe1.clusters.zeabur.com -P 32149 -u root -p -e "
  SELECT id, title, audio_path, audio_duration, audio_format
  FROM zeabur.stories
  WHERE audio_path IS NOT NULL
  ORDER BY created_at DESC
  LIMIT 5"

# 5. 测试音频文件访问
# (替换为实际路径)
curl -I http://localhost:5000/video/stories/2024/10/user_1/temp_xxx.webm
```

---

## 📝 回滚计划

如果测试失败需要回滚:

### 1. 回滚数据库
```sql
ALTER TABLE stories
DROP COLUMN audio_path,
DROP COLUMN audio_original_name,
DROP COLUMN audio_duration,
DROP COLUMN audio_format;
```

### 2. 回滚代码
```bash
git revert <commit-hash>
git push
```

### 3. 清理音频文件 (可选)
```bash
# 仅在确认不需要时执行
sudo rm -rf /video/stories/2024/10/
```

---

## 🚀 下一步优化建议

1. **音频压缩**: 考虑在服务器端压缩大音频文件
2. **格式转换**: 统一转换为 MP3 或其他通用格式
3. **存储清理**: 定期清理未发布故事的临时音频
4. **CDN 加速**: 将音频文件迁移到 CDN
5. **进度条**: 添加音频上传进度条
6. **波形可视化**: 显示音频波形图
7. **下载功能**: 允许用户下载音频文件

---

## 📞 支持信息

如有问题，请检查:
1. 应用日志
2. Zeabur 平台日志
3. 浏览器控制台错误
4. Network 请求详情

记录以下信息便于调试:
- 用户 ID
- 故事 ID
- 音频文件路径
- 错误信息截图
- Network 请求响应
