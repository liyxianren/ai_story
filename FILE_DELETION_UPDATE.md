# 🗑️ 故事删除时文件清理功能更新

## ✅ 更新内容

### 问题
之前管理员永久删除故事时，只删除了数据库记录，但图片和音频文件仍然保留在服务器上，造成存储空间浪费。

### 解决方案
更新了以下两个函数，确保在永久删除故事时同时删除关联的图片和音频文件：

1. **单个永久删除**: `/admin/api/permanently_delete_story/<story_id>`
2. **批量永久删除**: `/admin/api/batch_recycling_action` (action='permanently_delete')

---

## 📝 修改详情

### 1. 单个永久删除故事 (app.py:2935-2990)

**修改前**:
- 只删除数据库记录
- 不删除文件

**修改后**:
```python
@app.route('/admin/api/permanently_delete_story/<int:story_id>', methods=['DELETE'])
@admin_required
def admin_permanently_delete_story(story_id):
    # 1. 查询故事时同时获取 image_path 和 audio_path
    cursor.execute("""
        SELECT id, image_path, audio_path
        FROM stories
        WHERE id = %s AND deleted_at IS NOT NULL
    """, (story_id,))
    story = cursor.fetchone()

    # 2. 删除图片文件（如果存在）
    if story.get('image_path'):
        image_full_path = os.path.join(Config.UPLOAD_FOLDER, story['image_path'])
        if os.path.exists(image_full_path):
            os.remove(image_full_path)

    # 3. 删除音频文件（如果存在）
    if story.get('audio_path'):
        audio_full_path = os.path.join(Config.AUDIO_UPLOAD_FOLDER, story['audio_path'])
        if os.path.exists(audio_full_path):
            os.remove(audio_full_path)

    # 4. 删除数据库记录
    cursor.execute("DELETE FROM stories WHERE id = %s", (story_id,))
```

### 2. 批量永久删除故事 (app.py:3019-3057)

**修改前**:
- 只删除数据库记录
- 循环中不删除文件

**修改后**:
```python
elif action == 'permanently_delete':
    cursor_dict = connection.cursor(pymysql.cursors.DictCursor)
    for story_id in story_ids:
        # 1. 查询每个故事的文件路径
        cursor_dict.execute("""
            SELECT id, image_path, audio_path
            FROM stories
            WHERE id = %s AND deleted_at IS NOT NULL
        """, (story_id,))
        story = cursor_dict.fetchone()

        if story:
            # 2. 删除图片文件
            if story.get('image_path'):
                image_full_path = os.path.join(Config.UPLOAD_FOLDER, story['image_path'])
                if os.path.exists(image_full_path):
                    os.remove(image_full_path)

            # 3. 删除音频文件
            if story.get('audio_path'):
                audio_full_path = os.path.join(Config.AUDIO_UPLOAD_FOLDER, story['audio_path'])
                if os.path.exists(audio_full_path):
                    os.remove(audio_full_path)

            # 4. 删除数据库记录
            cursor.execute("DELETE FROM stories WHERE id = %s", (story_id,))
```

---

## 🔍 技术细节

### 文件路径构造
- **图片路径**: `Config.UPLOAD_FOLDER + story['image_path']`
  - 例如: `/image/stories/2025/10/user_25/story_123_main.jpg`
- **音频路径**: `Config.AUDIO_UPLOAD_FOLDER + story['audio_path']`
  - 例如: `/video/stories/2025/10/user_25/temp_xxx.webm`

### 错误处理
- 使用 `try-except` 包裹文件删除操作
- 即使文件删除失败，也会继续删除数据库记录
- 所有文件操作都有日志记录：
  ```python
  logger.info(f"Deleted image file: {image_full_path}")
  logger.error(f"Failed to delete audio file: {e}")
  ```

### 安全性
- 只删除在回收站中的故事 (`deleted_at IS NOT NULL`)
- 使用 `os.path.exists()` 检查文件是否存在再删除
- 使用 `os.path.join()` 安全构造路径，避免路径注入

---

## 🧪 测试步骤

### 测试 1: 单个永久删除

1. **创建测试故事**
   - 录制音频并上传图片
   - 发布故事
   - 记录 story_id

2. **软删除故事**
   - 管理员后台点击 "删除" 按钮
   - 故事移入回收站

3. **验证文件存在**
   ```bash
   # 检查文件是否存在
   ls -la /image/stories/2025/10/user_*/story_*
   ls -la /video/stories/2025/10/user_*/temp_*
   ```

4. **永久删除故事**
   - 管理员后台进入回收站
   - 点击 "永久删除" 按钮

5. **验证文件已删除**
   ```bash
   # 文件应该不存在
   ls -la /image/stories/2025/10/user_*/story_*  # 应该找不到
   ls -la /video/stories/2025/10/user_*/temp_*   # 应该找不到
   ```

6. **检查日志**
   ```
   INFO:__main__:Deleted image file: /image/stories/...
   INFO:__main__:Deleted audio file: /video/stories/...
   ```

### 测试 2: 批量永久删除

1. **创建多个测试故事** (至少 3 个)
   - 每个都有图片和音频
   - 软删除所有故事

2. **批量永久删除**
   - 管理员后台勾选多个故事
   - 点击 "批量永久删除"

3. **验证所有文件已删除**
   ```bash
   find /image/stories -name "story_*" -mmin -5
   find /video/stories -name "temp_*" -mmin -5
   # 应该没有输出
   ```

4. **检查批量删除日志**
   ```
   INFO:__main__:Batch delete: Removed image file: ...
   INFO:__main__:Batch delete: Removed audio file: ...
   ```

### 测试 3: 边缘情况

**情况 1: 故事只有图片，没有音频**
- ✅ 应该只删除图片文件
- ✅ 不应该报错

**情况 2: 故事只有音频，没有图片**
- ✅ 应该只删除音频文件
- ✅ 不应该报错

**情况 3: 故事既没有图片也没有音频**
- ✅ 应该只删除数据库记录
- ✅ 不应该报错

**情况 4: 文件已经被手动删除**
- ✅ `os.path.exists()` 返回 False，跳过删除
- ✅ 继续删除数据库记录
- ✅ 不应该报错

---

## 📊 日志示例

### 成功删除
```
INFO:__main__:Deleted image file: /image/stories/2025/10/user_25/story_123_main.jpg
INFO:__main__:Deleted audio file: /video/stories/2025/10/user_25/temp_0f447886-34dd-4a2a-ad0a-30a73d080bd7_original.webm
```

### 文件不存在（正常情况）
```
# 不会输出任何日志，因为 os.path.exists() 返回 False
```

### 删除失败（权限问题等）
```
ERROR:__main__:Failed to delete image file: [Errno 13] Permission denied: '/image/stories/...'
ERROR:__main__:Failed to delete audio file: [Errno 13] Permission denied: '/video/stories/...'
```

---

## 🔒 注意事项

1. **确保应用有文件删除权限**
   ```bash
   # 检查目录权限
   ls -ld /image/stories
   ls -ld /video/stories

   # 应该是 drwxr-xr-x 或更宽松
   ```

2. **软删除不会删除文件**
   - 只有永久删除才会删除文件
   - 软删除 (`deleted_at` 设置时间戳) 文件仍然保留
   - 这样可以支持从回收站恢复故事

3. **备份建议**
   - 定期备份 `/image/stories` 和 `/video/stories` 目录
   - 永久删除是不可逆的操作

4. **存储空间监控**
   - 定期检查回收站，清理长时间未恢复的故事
   - 考虑添加自动清理策略（如 30 天后自动永久删除）

---

## 🚀 部署清单

- [x] 修改 `admin_permanently_delete_story` 函数
- [x] 修改 `admin_batch_recycling_action` 函数
- [x] 添加文件删除逻辑（图片和音频）
- [x] 添加错误处理和日志记录
- [x] 重启应用使更改生效
- [ ] 在生产环境测试文件删除功能
- [ ] 监控日志确认文件正常删除
- [ ] 验证存储空间释放

---

## 💡 未来优化建议

1. **添加软删除定时清理**
   ```python
   # 每天自动清理 30 天前软删除的故事
   @app.route('/admin/api/cleanup_old_deleted_stories', methods=['POST'])
   def cleanup_old_deleted_stories():
       cutoff_date = datetime.now() - timedelta(days=30)
       # 查询并永久删除旧的软删除故事
   ```

2. **添加删除确认和撤销功能**
   - 永久删除前二次确认
   - 短时间内支持撤销操作

3. **批量清理孤立文件**
   ```python
   # 查找数据库中不存在的文件并清理
   @app.route('/admin/api/cleanup_orphan_files', methods=['POST'])
   def cleanup_orphan_files():
       # 扫描文件系统，删除没有对应数据库记录的文件
   ```

4. **存储统计报表**
   - 显示各用户占用的存储空间
   - 显示回收站占用的空间
   - 提供存储清理建议

---

## 📞 故障排查

### 问题: 文件删除失败

**检查日志**:
```bash
grep "Failed to delete" /var/log/your-app/error.log
```

**可能原因**:
1. **权限不足**: 应用没有删除文件的权限
2. **文件被占用**: 文件正在被其他进程使用
3. **磁盘错误**: 文件系统错误

**解决方案**:
```bash
# 修复权限
sudo chown -R www-data:www-data /image/stories /video/stories
sudo chmod -R 755 /image/stories /video/stories

# 检查文件系统
df -h
fsck /dev/sda1  # 根据实际情况调整
```

### 问题: 数据库删除成功但文件未删除

**检查**:
1. 查看日志是否有错误信息
2. 手动检查文件是否存在
3. 验证路径拼接是否正确

**临时手动清理**:
```bash
# 查找数据库中不存在的文件
mysql -e "SELECT image_path FROM stories WHERE deleted_at IS NOT NULL"
# 手动删除这些文件
```
