# 音频语言信息功能实现文档
# Audio Language Information Feature Implementation

## 📋 功能概述

此功能允许系统保存和显示用户录音或上传音频时选择的语言信息。

### 主要特性
- ✅ 保存录音时选择的语言代码和名称
- ✅ 在故事详情页面显示音频录制语言
- ✅ 历史数据兼容（旧故事不显示语言信息）
- ✅ 支持所有现有的语言选项

---

## 🔧 实施的修改

### 1. 数据库层面
**文件**: `migrate_add_audio_language.py`

添加了两个新字段到 `stories` 表：
- `audio_language` VARCHAR(20) - 语言代码（如: 'cmn-Hans-CN', 'en-US'）
- `audio_language_name` VARCHAR(100) - 语言名称（如: 'Chinese (Mandarin)', 'English'）

**执行迁移**:
```bash
python migrate_add_audio_language.py
```

### 2. 前端 - 录音页面
**文件**: `templates/record_story.html` (第3777-3784行)

修改了 `audioData` 对象，添加语言信息：
```javascript
this.audioData = {
    audio_path: result.audio_path,
    audio_original_name: result.audio_original_name,
    audio_duration: result.audio_duration,
    audio_format: result.audio_format,
    audio_language: this.selectedLanguage,           // 新增
    audio_language_name: this.getLanguageName(this.selectedLanguage)  // 新增
};
```

### 3. 前端 - 发布页面
**文件**: `templates/publish_story.html` (第891-892行)

在表单提交时添加语言信息到 FormData：
```javascript
formData.append('audio_language', audioData.audio_language || '');
formData.append('audio_language_name', audioData.audio_language_name || '');
```

### 4. 后端 - 发布API
**文件**: `app.py`

#### 接收参数 (第1604-1605行)
```python
audio_language = request.form.get('audio_language')
audio_language_name = request.form.get('audio_language_name')
```

#### 保存到数据库 (第1642-1659行)
```python
INSERT INTO stories (user_id, title, content, language, language_name, description,
                   image_path, image_original_name,
                   audio_path, audio_original_name, audio_duration, audio_format,
                   audio_language, audio_language_name,  # 新增
                   reading_time, word_count, status, published_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
```

#### 查询故事详情 (第1251-1273行)
```python
SELECT
    s.id, s.title, s.content, s.description, s.language_name,
    s.image_path, s.image_original_name,
    s.audio_path, s.audio_original_name, s.audio_duration, s.audio_format,
    s.audio_language, s.audio_language_name,  # 新增
    ...
FROM stories s
```

### 5. 前端 - 故事详情页面
**文件**: `templates/story_detail.html` (第487-492行)

在音频播放器区域显示语言信息：
```html
{% if story.audio_language_name %}
<div style="display: flex; align-items: center; gap: 8px;">
    <i class="fas fa-globe" style="color: #22c55e;"></i>
    <span>Language: <strong>{{ story.audio_language_name }}</strong></span>
</div>
{% endif %}
```

---

## 🧪 测试流程

### 1. 数据库迁移测试
```bash
# 运行迁移脚本
python migrate_add_audio_language.py

# 预期输出：
# [SUCCESS] 数据库迁移完成！
# 显示新增的两个字段：audio_language, audio_language_name
```

### 2. 录音功能测试

**步骤**：
1. 访问 `/record` 页面
2. 选择一个语言（例如：中文、英语）
3. 录制或上传音频文件
4. 点击转录
5. 转录成功后，检查浏览器控制台

**验证点**：
```javascript
// 在控制台应该看到：
🎙️ Audio information saved: {
  audio_path: "2025/10/user_xxx/...",
  audio_duration: 120,
  audio_format: "webm",
  audio_language: "cmn-Hans-CN",      // ✓ 包含语言代码
  audio_language_name: "Chinese (Mandarin)"  // ✓ 包含语言名称
}
```

### 3. 发布功能测试

**步骤**：
1. 完成录音后，点击"Publish Story"
2. 填写标题、描述等信息
3. 提交故事

**验证点**：
```sql
-- 在数据库中检查新发布的故事
SELECT audio_language, audio_language_name
FROM stories
ORDER BY created_at DESC
LIMIT 1;

-- 预期结果：
-- audio_language: 'cmn-Hans-CN' (或用户选择的语言)
-- audio_language_name: 'Chinese (Mandarin)' (或相应的语言名称)
```

### 4. 展示功能测试

**步骤**：
1. 访问已发布的故事详情页面
2. 滚动到音频播放器区域

**验证点**：
- ✅ 应该看到音频播放器
- ✅ 显示录音时长
- ✅ 显示音频格式
- ✅ **显示语言信息**（例如：🌍 Language: **Chinese (Mandarin)**）

### 5. 历史数据兼容性测试

**步骤**：
1. 访问迁移前创建的旧故事

**验证点**：
- ✅ 旧故事正常显示
- ✅ 音频播放器正常工作
- ✅ **不显示语言信息行**（因为 audio_language_name 为 NULL）

---

## 📊 数据流程图

```
用户选择语言 (录音页面)
    ↓
保存到 audioData.audio_language
保存到 audioData.audio_language_name
    ↓
转录/上传音频
    ↓
存储到 sessionStorage
    ↓
发布页面读取 sessionStorage
    ↓
提交到后端 /api/publish_story
    ↓
保存到数据库 stories 表
    ↓
故事详情页面查询显示
```

---

## 🎯 支持的语言列表

系统支持以下语言的完整映射：

| 语言代码 | 语言名称 | 显示示例 |
|---------|---------|---------|
| en-US | English (US) | 🌍 Language: **English (US)** |
| cmn-Hans-CN | Chinese (Mandarin) | 🌍 Language: **Chinese (Mandarin)** |
| es-ES | Español (Spanish) | 🌍 Language: **Español (Spanish)** |
| ja-JP | 日本語 (Japanese) | 🌍 Language: **日本語 (Japanese)** |
| ko-KR | 한국어 (Korean) | 🌍 Language: **한국어 (Korean)** |
| ar-SA | العربية (Arabic) | 🌍 Language: **العربية (Arabic)** |
| hi-IN | हिन्दी (Hindi) | 🌍 Language: **हिन्दी (Hindi)** |
| fr-FR | Français (French) | 🌍 Language: **Français (French)** |
| de-DE | Deutsch (German) | 🌍 Language: **Deutsch (German)** |
| ... | ... | ... |

---

## 🔍 故障排查

### 问题1：语言信息未显示

**检查清单**：
1. 数据库是否成功添加字段？
   ```sql
   SHOW COLUMNS FROM stories LIKE 'audio_language%';
   ```
2. 故事是否是新创建的？（旧故事不会显示语言信息）
3. 浏览器控制台是否有错误？

### 问题2：数据库迁移失败

**解决方案**：
1. 检查数据库连接配置 (`config.py`)
2. 确认有足够的数据库权限
3. 手动执行 SQL：
   ```sql
   ALTER TABLE stories
   ADD COLUMN audio_language VARCHAR(20) DEFAULT NULL,
   ADD COLUMN audio_language_name VARCHAR(100) DEFAULT NULL;
   ```

### 问题3：语言信息保存为空

**检查**：
1. 录音时是否选择了语言？
2. 浏览器控制台检查 `audioData` 对象
3. 网络请求中是否包含语言参数？

---

## 📝 注意事项

1. **历史数据**：迁移前的故事 `audio_language` 和 `audio_language_name` 为 NULL，不会显示语言信息
2. **必填性**：语言字段不是必填的，如果用户没有录音/上传音频，这些字段将为空
3. **性能**：新增字段对查询性能影响微小（已在 GROUP BY 中包含）
4. **扩展性**：可以轻松添加更多语言，只需更新 `record_story.html` 中的语言列表

---

## ✅ 验证完成清单

- [x] 数据库迁移成功
- [x] 录音页面保存语言信息
- [x] 发布页面传递语言信息
- [x] 后端API接收和保存语言信息
- [x] 故事详情页面显示语言信息
- [x] 历史数据兼容性测试通过

---

## 🚀 部署步骤

1. **备份数据库**（重要！）
2. **运行数据库迁移**：
   ```bash
   python migrate_add_audio_language.py
   ```
3. **重启应用**（如果需要）
4. **测试新功能**：创建一个新故事并验证

---

## 📞 技术支持

如有问题，请检查：
- 数据库迁移日志
- 浏览器控制台
- 应用服务器日志

---

**实施日期**: 2025-10-24
**版本**: 1.0
**状态**: ✅ 已完成并测试
