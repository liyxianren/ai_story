使用 API 将语音转录为文字

bookmark_border
本页面介绍了如何使用 REST 接口和 curl 命令向 Speech-to-Text 发送语音识别请求。

Speech-to-Text 能够将 Google 语音识别技术轻松集成到开发者应用中。您可以向 Speech-to-Text API 发送音频数据，然后该 API 会返回该音频文件的文字转录。如需详细了解该服务，请参阅 Speech-to-Text 基础知识。

准备工作
您必须先完成以下操作，然后才能向 Speech-to-Text API 发送请求。如需了解详情，请参阅准备工作页面。

在 GCP 项目上启用 Speech-to-Text。
确保已针对 Speech-to-Text 启用结算功能。
Install the Google Cloud CLI. After installation, initialize the Google Cloud CLI by running the following command:



gcloud init
If you're using an external identity provider (IdP), you must first sign in to the gcloud CLI with your federated identity.

（可选）创建新的 Google Cloud Storage 存储桶以存储您的音频数据。
发出音频转录请求
现在您可以使用 Speech-to-Text 将音频文件转录为文字。请使用以下代码示例向 Speech-to-Text API 发送 recognize REST 请求。

创建包含以下文本的 JSON 请求文件，然后将其另存为 sync-request.json 纯文本文件：


{
  "config": {
      "encoding":"FLAC",
      "sampleRateHertz": 16000,
      "languageCode": "en-US",
      "enableWordTimeOffsets": false
  },
  "audio": {
      "uri":"gs://cloud-samples-tests/speech/brooklyn.flac"
  }
}
  
此 JSON 片段表明，音频文件具有 FLAC 编码格式，采样率为 16000 Hz，以及音频文件存储在 Google Cloud Storage 中的给定 URI 处。该音频文件可公开访问，因此您不需要身份验证凭据即可访问该文件。

使用 curl 发出 speech:recognize 请求，并向其传递您在步骤 1 中设置的 JSON 请求的文件名：

示例 curl 命令使用 gcloud auth print-access-token 命令来获取身份验证令牌。


curl -s -H "Content-Type: application/json" \
    -H "Authorization: Bearer "$(gcloud auth print-access-token) \
    https://speech.googleapis.com/v1/speech:recognize \
    -d @sync-request.json
  
请注意，要将文件名传递给 curl，您可以使用 -d 选项（表示“数据”）并在文件名前面加上 @ 符号。此文件应该位于您执行 curl 命令所在的目录中。

您应该会看到如下所示的响应：


{
  "results": [
    {
      "alternatives": [
        {
          "transcript": "how old is the Brooklyn Bridge",
          "confidence": 0.98267895
        }
      ]
    }
  ]
}
  
恭喜！您已向 Speech-to-Text 发送了您的第一个请求！

如果您收到来自 Speech-to-Text 的错误或空响应，请查看问题排查和纠错步骤。

清理
为避免因本页中使用的资源导致您的 Google Cloud 账号产生费用，请按照以下步骤操作。

使用 Google Cloud console 删除不需要的项目。
后续步骤

练习转录短音频文件。
了解如何批量处理长音频文件以进行语音识别。
了解如何转录流式音频，例如来自麦克风的音频。
通过使用 Speech-to-Text 客户端库，以您选择的语言开始使用 Speech-to-Text。
上手体验示例应用。
如需了解关于最佳性能、准确度和其他方面的提示，请参阅最佳做法文档。