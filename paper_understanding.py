from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="sk-********",
    # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

DATA_FOLDER = "data/download"

# moonshot.pdf 是一个示例文件, 我们支持文本文件和图片文件，对于图片文件，我们提供了 OCR 的能力
# 上传文件时，我们可以直接使用 openai 库的文件上传 API，使用标准库 pathlib 中的 Path 构造文件
# 对象，并将其传入 file 参数即可，同时将 purpose 参数设置为 file-extract；注意，目前文件上传
# 接口仅支持 file-extract 一种 purpose 值。
for file_path in Path(DATA_FOLDER).glob("*.pdf"):
    print(f"上传文件: {file_path}")
    file_object = client.files.create(file=file_path, purpose="file-extract")
    print(f"文件上传成功: {file_object.id}")

    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，某些旧版本示例中的 retrieve_content API 在最新版本标记了 warning, 可以用下面这行代替
    # （如果使用旧版本的 SDK，可以继续延用 retrieve_content API）
    print(f"获取文件内容: {file_object.id}")
    file_content = client.files.content(file_id=file_object.id).text
    print(file_content)

    # 计算文件的 token 数量
    token_count = len(file_content)
    print(f"文件 token 数量: {token_count}")

    # 把文件内容通过系统提示词 system prompt 放进请求中
    messages = [
        {
            "role":
            "system",
            "content": ("你是 Kimi，由 Moonshot AI 提供的人工智能助手，"
                        "你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。"
                        "同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"
                        "Moonshot AI 为专有名词，不可翻译成其他语言。"),
        },
        {
            "role": "system",
            # 这里，我们将抽取后的文件内容（注意是文件内容，而不是文件 ID）放置在请求中
            "content": file_content,
        },
        {
            "role": "user",
            "content": f"请简单介绍 {file_path} 的具体内容"
        },
    ]

    # 然后调用 chat-completion, 获取 Kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
        temperature=0.3,
    )

    print(completion.choices[0].message)
    break
