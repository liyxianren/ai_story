# Zeabur 部署配置说明

## 大文件上传配置

本应用支持最大30MB的音频文件上传。为确保正常工作，需要在Zeabur中配置以下环境变量：

### 必需的环境变量

在Zeabur项目的"环境变量"(Environment Variables)页面添加：

```
# Gunicorn超时设置（必需！）
GUNICORN_TIMEOUT=600
GUNICORN_GRACEFUL_TIMEOUT=120

# 如果Zeabur有Nginx反向代理，可能需要以下设置
NGINX_CLIENT_MAX_BODY_SIZE=40M
NGINX_PROXY_READ_TIMEOUT=600s
NGINX_PROXY_CONNECT_TIMEOUT=600s
NGINX_PROXY_SEND_TIMEOUT=600s
```

### 为什么需要这些配置？

1. **GUNICORN_TIMEOUT=600**
   - Worker处理请求的最大时间（10分钟）
   - 上传和处理30MB音频文件需要较长时间

2. **NGINX反向代理超时设置**
   - Zeabur通常使用Nginx作为反向代理
   - 默认超时可能只有60秒
   - 需要增加到至少600秒以匹配Gunicorn超时

### 检查部署状态

部署后，查看日志应该能看到：

```
=== TRANSCRIBE API CALLED ===
Request content length: 9123068
Request content type: multipart/form-data
Attempting to access request.files...
Audio file found in request
Audio filename: recording.wav
Language code: en-US
File extension: wav
Starting to read audio data...
Audio data read complete: 8.70 MB
```

如果在"Attempting to access request.files..."之后就超时，说明：
- Gunicorn超时设置未生效
- 或者Zeabur/Nginx层有额外的超时限制

### 故障排查

如果仍然超时：

1. 确认环境变量已添加并重新部署
2. 检查Zeabur控制台的服务日志
3. 联系Zeabur支持确认是否有平台级别的请求大小或超时限制
4. 考虑使用Zeabur的对象存储(Object Storage)服务来处理大文件上传

### 当前配置摘要

- Flask `MAX_CONTENT_LENGTH`: 35MB
- Flask `MAX_FORM_MEMORY_SIZE`: 50MB
- Gunicorn `timeout`: 600秒 (10分钟)
- Gunicorn `graceful_timeout`: 120秒 (2分钟)
- 应用层验证: 30MB音频文件
