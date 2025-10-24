# 🎙️ 音频保存与播放功能实施总结

## ✅ 已完成的修改

### 1. 数据库修改
- **文件**: `database_migration_add_audio.sql`
- **状态**: ✅ 已创建
- **说明**: 为 stories 表添加 4 个音频字段
  - `audio_path` - 音频文件相对路径
  - `audio_original_name` - 原始文件名
  - `audio_duration` - 时长(秒)
  - `audio_format` - 格式(webm/mp3等)
- **执行方法**: 在 MySQL 中运行此 SQL 文件

### 2. 后端代码修改

#### audio_service.py ✅
- 完全参照 image_service.py 实现
- 保存路径: `/video/stories/年份/月份/user_用户ID/文件名`
- 支持格式: webm, mp3, wav, m4a, ogg, mp4
- 最大文件大小: 25MB

#### config.py ✅
- 添加音频配置参数
  ```python
  AUDIO_UPLOAD_FOLDER = '/video/stories'
  MAX_AUDIO_SIZE = 25 * 1024 * 1024
  ALLOWED_AUDIO_FORMATS = ['webm', 'mp3', 'wav', 'm4a', 'ogg', 'mp4']
  ```

#### app.py 修改 ✅
1. **导入 audio_service** (Line 14)
   ```python
   from audio_service import audio_service
   ```

2. **新增音频访问路由** (Line 224-232)
   ```python
   @app.route('/video/stories/<path:filename>')
   def serve_audio(filename):
       return send_from_directory('/video/stories', filename)
   ```

3. **修改 /api/transcribe** (Line 933-986)
   - 转录成功后保存音频文件
   - 返回音频信息: audio_path, audio_original_name, audio_duration, audio_format

4. **修改 /api/publish_story** (Line 1467-1522)
   - 接收表单中的音频信息
   - 插入数据库时包含音频字段

5. **修改 story_detail** (Line 1123-1143)
   - SELECT 查询包含音频字段
   - 返回给模板用于显示播放器

### 3. 前端代码修改

#### record_story.html ✅
1. **showTranscriptionResult函数** (Line 3624-3636)
   - 保存音频信息到 recorder.audioData
   ```javascript
   if (result.audio_path) {
       this.audioData = {
           audio_path: result.audio_path,
           audio_original_name: result.audio_original_name,
           audio_duration: result.audio_duration,
           audio_format: result.audio_format
       };
   }
   ```

2. **publishStoryToPublishPage函数** (Line 4018-4026)
   - 保存音频信息到 sessionStorage
   ```javascript
   if (recorder.audioData) {
       sessionStorage.setItem('storyAudio', JSON.stringify(recorder.audioData));
   }
   ```

## 🔧 待完成的前端修改

### 4. publish_story.html 修改步骤

#### 步骤 A: 页面加载时读取音频数据并显示预览
在 DOMContentLoaded 事件监听器中添加:

```javascript
// 在页面加载时读取音频数据
window.addEventListener('DOMContentLoaded', () => {
    // 读取音频信息
    const audioDataStr = sessionStorage.getItem('storyAudio');
    if (audioDataStr) {
        try {
            const audioData = JSON.parse(audioDataStr);

            // 显示音频预览区域
            const audioPreview = document.getElementById('audioPreview');
            if (audioPreview && audioData.audio_path) {
                audioPreview.style.display = 'block';

                // 设置音频源
                const audioPlayer = document.getElementById('audioPreviewPlayer');
                const audioSource = document.getElementById('audioPreviewSource');
                if (audioPlayer && audioSource) {
                    audioSource.src = `/video/stories/${audioData.audio_path}`;
                    audioSource.type = `audio/${audioData.audio_format || 'webm'}`;
                    audioPlayer.load();
                }

                // 显示文件信息
                document.getElementById('audioFileName').textContent = audioData.audio_original_name || 'recording';
                document.getElementById('audioDuration').textContent = audioData.audio_duration || '未知';
            }
        } catch (e) {
            console.error('Error loading audio data:', e);
        }
    }
});
```

#### 步骤 B: 在表单中添加音频预览 HTML (找到合适位置插入)
在故事内容卡片后添加:

```html
<!-- 音频预览区域 -->
<div class="modern-card" id="audioPreview" style="display:none;">
    <div class="card-header-modern card-header-info">
        <i class="fas fa-headphones me-2"></i>录音预览
    </div>
    <div class="p-4">
        <audio id="audioPreviewPlayer" controls style="width:100%; border-radius: 12px;">
            <source id="audioPreviewSource" type="audio/webm">
            您的浏览器不支持音频播放。
        </audio>
        <div class="mt-3 text-muted" style="font-size: 0.9rem;">
            <i class="fas fa-info-circle me-2"></i>
            <span id="audioFileName">recording.webm</span> •
            时长: <span id="audioDuration">0</span>秒
        </div>
    </div>
</div>
```

#### 步骤 C: 修改发布函数,提交音频信息
在 publishStory 函数中,FormData 添加音频字段:

```javascript
async function publishStory() {
    // ... 现有代码 ...

    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('description', description);
    formData.append('story_type', storyType);

    // 添加封面图片
    if (coverImageFile) {
        formData.append('cover_image', coverImageFile);
    }

    // 【新增】添加音频信息
    const audioDataStr = sessionStorage.getItem('storyAudio');
    if (audioDataStr) {
        try {
            const audioData = JSON.parse(audioDataStr);
            if (audioData.audio_path) {
                formData.append('audio_path', audioData.audio_path);
                formData.append('audio_original_name', audioData.audio_original_name);
                formData.append('audio_duration', audioData.audio_duration);
                formData.append('audio_format', audioData.audio_format);
                console.log('🎙️ Audio info added to form submission');
            }
        } catch (e) {
            console.error('Error adding audio data:', e);
        }
    }

    // 提交表单
    const response = await fetch('/api/publish_story', {
        method: 'POST',
        body: formData
    });

    // ... 处理响应 ...
}
```

### 5. story_detail.html 修改步骤

#### 在故事内容显示区域上方添加音频播放器 HTML:

找到故事内容的主要显示区域 (通常在 `<div class="story-content">` 之前),插入:

```html
{% if story.audio_path %}
<!-- 音频播放器区域 -->
<div class="modern-card mb-4" style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.05) 0%, rgba(255, 255, 255, 0.95) 100%);">
    <div class="card-header-modern" style="background: linear-gradient(135deg, #22c55e 0%, #10a34a 100%);">
        <i class="fas fa-headphones me-2"></i>🎧 收听故事原声
    </div>
    <div class="p-4">
        <div class="audio-player-container">
            <audio id="storyAudioPlayer" controls style="width:100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <source src="/video/stories/{{ story.audio_path }}" type="audio/{{ story.audio_format or 'webm' }}">
                您的浏览器不支持音频播放。
            </audio>
        </div>

        <div class="audio-info mt-3" style="display: flex; align-items: center; gap: 20px; color: #6b7280; font-size: 0.9rem;">
            <div style="display: flex; align-items: center;">
                <i class="fas fa-microphone me-2" style="color: #22c55e;"></i>
                由 <strong style="color: var(--warm-primary); margin: 0 4px;">{{ story.author }}</strong> 亲自录制
            </div>
            {% if story.audio_duration %}
            <div style="display: flex; align-items: center;">
                <i class="fas fa-clock me-2" style="color: #22c55e;"></i>
                时长: {{ (story.audio_duration // 60)|int }}分{{ story.audio_duration % 60 }}秒
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endif %}
```

## 📊 数据流程图

```
用户录音
  ↓
前端: MediaRecorder 录制 → Blob
  ↓
POST /api/transcribe (转录API)
  ↓
后端: audio_service.upload_story_audio()
  ↓
保存到: /video/stories/2024/10/user_1/temp_xxx.webm
  ↓
返回: { audio_path, audio_original_name, audio_duration, audio_format }
  ↓
前端: 保存到 recorder.audioData
  ↓
跳转发布页面: 存入 sessionStorage['storyAudio']
  ↓
发布页面: 读取 sessionStorage,显示预览
  ↓
提交表单: FormData 包含音频信息
  ↓
POST /api/publish_story
  ↓
后端: INSERT INTO stories 包含音频字段
  ↓
数据库: 永久保存音频路径等信息
  ↓
故事详情页: 读取数据库,显示音频播放器
  ↓
用户点击播放: GET /video/stories/{audio_path}
  ↓
Flask: send_from_directory() 提供文件
  ↓
浏览器: HTML5 audio 标签播放
```

## ✅ 验证清单

### 后端验证
- [x] SQL 迁移文件已创建
- [x] audio_service.py 已创建
- [x] config.py 已添加配置
- [x] app.py 已导入 audio_service
- [x] /video/stories 路由已添加
- [x] /api/transcribe 保存音频并返回信息
- [x] /api/publish_story 接收并保存音频信息
- [x] story_detail 查询包含音频字段

### 前端验证
- [x] record_story.html 保存音频信息到 recorder.audioData
- [x] record_story.html 跳转时存入 sessionStorage
- [ ] publish_story.html 显示音频预览播放器
- [ ] publish_story.html 提交时包含音频信息
- [ ] story_detail.html 显示音频播放器

### 功能验证
- [ ] 录音 → 转录 → 音频文件已保存
- [ ] 发布页面显示音频预览
- [ ] 故事发布成功,数据库包含音频信息
- [ ] 故事详情页显示播放器
- [ ] 点击播放按钮,音频正常播放
- [ ] 重启服务后,音频仍然可以播放

## 🎯 下一步操作

1. **执行数据库迁移**
   ```bash
   mysql -u root -p zeabur < database_migration_add_audio.sql
   ```

2. **完成剩余前端修改**
   - 修改 publish_story.html (参考上面步骤 A、B、C)
   - 修改 story_detail.html (参考上面步骤 5)

3. **测试完整流程**
   - 录制一个测试故事
   - 检查转录后是否有音频信息
   - 在发布页面查看预览
   - 发布故事
   - 在详情页播放音频

4. **验证数据持久化**
   - 检查 `/video/stories/` 目录中的文件
   - 检查数据库 stories 表的 audio_* 字段
   - 重启服务后再次访问,验证音频仍可播放

## 💡 技术要点

- 音频保存完全参照图片保存机制,成熟可靠
- 使用相对路径存储,跨环境兼容
- 前后端分离,数据通过 sessionStorage 传递
- 支持多种音频格式
- HTML5 audio 标签原生支持流式播放

## 📝 注意事项

1. 确保服务器 `/video/stories` 目录存在并有写入权限
2. 数据库迁移需要在所有环境 (开发/生产) 执行
3. 音频文件较大,注意服务器存储空间
4. 考虑添加音频文件清理策略(删除未发布故事的音频)
