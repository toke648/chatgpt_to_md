# ChatGPT to Markdown

一个简单的工具，将ChatGPT导出的zip文件转换为漂亮的Markdown文件。

## 安装

```bash
pip install chatgpt-to-md
```

## 使用方法

### 命令行使用

```bash
# 基本用法
chatgpt-to-md conversation.zip

# 指定输出目录
chatgpt-to-md conversation.zip -o ./my_chats
```

### Python中使用

```python
from chatgpt_to_md import convert

convert("conversation.zip", "./output")
```

## 功能特点

- ✅ 自动解压zip文件
- ✅ 转换所有对话为独立的Markdown文件
- ✅ 包含YAML front matter元数据
- ✅ 按时间排序对话消息
- ✅ 自动处理文件名中的非法字符

## 许可证

MIT
```

## 5. 许可证文件 (`LICENSE`)

```text
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted...
```

## 发布流程

### 1. 本地开发和测试

```bash
# 进入项目目录
cd chatgpt-to-md

# 安装为开发模式
pip install -e .

# 测试功能
chatgpt-to-md test_conversation.zip -o ./test_output
```

### 2. 构建包

```bash
# 安装构建工具
pip install build

# 构建包
python -m build
```

这会生成 `dist/` 目录，包含 `.whl` 和 `.tar.gz` 文件。

### 3. 发布到 PyPI

```bash
# 安装上传工具
pip install twine

# 上传到 PyPI
twine upload dist/*
```

## 使用方式

### 作为用户安装使用

```bash
# 从PyPI安装
pip install chatgpt-to-md

# 使用
chatgpt-to-md my_chatgpt_data.zip -o ./conversations
```

### 作为开发者使用

```python
from chatgpt_to_md import convert

# 在代码中使用
convert("path/to/chatgpt.zip", "./output_directory")
```

## 项目特点

1. **最简依赖**: 只使用Python标准库，无外部依赖
2. **单一功能**: 专注完成一个核心任务
3. **易于理解**: 代码结构清晰，便于学习和修改
4. **即装即用**: 安装后直接通过命令行使用
5. **标准化**: 符合Python包发布标准

这个架构让你能够：
- ✅ 快速理解整个发布流程
- ✅ 轻松维护和扩展
- ✅ 让其他用户方便安装使用
- ✅ 符合Python生态系统标准