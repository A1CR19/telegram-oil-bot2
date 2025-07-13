# Telegram 销售机器人

这是一个用 Python 编写的 Telegram 销售机器人，支持：
- 自定义按钮
- 图文回复
- 多类型卡密处理
- Render.com 部署

## 快速开始

### 1. 安装依赖
```
pip install -r requirements.txt
```

### 2. 设置环境变量
在你的系统或部署平台设置 BOT_TOKEN：

```
BOT_TOKEN=你的 BotFather Token
```

### 3. 运行机器人
```
python bot.py
```

## 推荐部署平台
- [Render.com](https://render.com/)：支持长期免费运行
- 使用 `Web Service` 部署即可

## 示例按钮
- 🅜 油卡*1张
- 🅜 电信卡*10张
- 👩‍💻 在线客服 等

你可以在 `bot.py` 文件中自定义按钮和图片链接。
