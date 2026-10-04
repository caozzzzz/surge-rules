# Personal Surge Rules

这是一个可直接托管到 GitHub 的 Surge 外部规则集仓库。

## 目录

- `rules/ai.list`：AI 合集，包含 ChatGPT、Gemini 等（自动同步）
- `rules/openai.list`：旧 OpenAI 兼容文件，不再由主配置引用
- `rules/apple.list`：普通 Apple 服务（自动同步）
- `rules/apple-ai.list`：Apple Intelligence / Private Relay（自动同步）
- `rules/spotify.list`：Spotify（自动同步）
- `rules/youtube.list`：YouTube（自动同步）
- `rules/youtube-music.list`：YouTube Music（自动同步）
- `rules/netflix.list`：Netflix（自动同步）
- `rules/telegram.list`：Telegram（自动同步）
- `rules/twitter.list`：Twitter / X（自动同步）
- `rules/tiktok.list`：TikTok（自动同步）
- `rules/china.list`：中国大陆 IPv4 规则（自动同步）
- `icons/`：Essential 系列策略组图标（256×256、透明背景 PNG）
- `icons/source/`：18 枚独立图标的设计源图片
- `scripts/generate-icons.py`：统一尺寸、留白并生成图标，保留旧版 URL 兼容文件

## 自有图标

策略组图标由本仓库自行托管，不依赖第三方图标仓库。配置使用以下格式引用：

```ini
icon-url=https://raw.githubusercontent.com/caozzzzz/surge-rules/main/icons/ai.png?v=essential-20261002
```

Essential 系列采用无底板的独立符号，保留品牌和地区辨识度。Airport 使用客机剪影，Proxy 使用蓝紫交错流线表达流量转发。图标设计由 ImageGen 制作，再从透明图集中拆分为独立源图片。

在本地运行 `python -m pip install -r requirements-icons.txt` 安装固定版本依赖后运行 `python scripts/generate-icons.py`，可以从 `icons/source/` 重新生成整套图标。所有图标统一输出为 256×256 RGBA PNG，符号置于 208×208 的内容区域，保留透明留白。图标源图片、生成脚本或依赖发生变化时自动生成，也可手动运行 Generate policy icons；每日规则同步不再重新生成图标。旧版带版本号的图标文件仍保留并同步生成，以兼容已下载的配置。

## 首次导入

`surge.conf` 预置了本仓库的可下载示例订阅 `examples/subscription.list`，四个地区组均有名称匹配的示例节点，示例节点不能实际连接。使用时只需将 Airport 行 `policy-path=` 后面的 URL 替换为你的 Surge 格式完整订阅 URL，再把订阅域名规则中的 `example.com` 改成真实订阅域名。Airport 的 `hidden=1` 可改为 `hidden=0` 以显示入口。Zus、Zjp 是独立示例节点，可修改或删除；删除时也要从 Proxy🪁 策略组移除引用。本地控制 API 默认注释关闭。不要将真实订阅 Token 提交到公开仓库。

## Surge 引用

仓库所有者为 `caozzzzz`：

```ini
[Rule]
DOMAIN-SUFFIX,raw.githubusercontent.com,Proxy

RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/apple-ai.list,Apple-AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/ai.list,AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/apple.list,Apple
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/netflix.list,Netflix
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/telegram.list,Telegram,no-resolve
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/twitter.list,Twitter
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/tiktok.list,TikTok
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/spotify.list,Spotify
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/youtube-music.list,YouTube-Music
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/youtube.list,YouTube
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/china.list,DIRECT
GEOIP,CN,DIRECT
FINAL,Final,dns-failed
```

规则集文件内部不包含策略名称。策略由主配置中的 `RULE-SET` 行统一指定。

## 自动更新

GitHub Actions 每天北京时间 06:20 同步上游规则，并在提交前执行格式检查。也可以在仓库的 Actions 页面手动运行 `Sync Surge rules`。

香港策略组使用 fallback，按节点列表优先级选择可用节点，故障时自动切换；Apple-AI 优先于 AI 和普通 Apple 规则匹配。

LAN 检查分为两层：开头使用 `RULE-SET,LAN,DIRECT,no-resolve`，避免为判断是否内网而提前解析所有域名；应用规则之后、国内规则之前保留 `RULE-SET,LAN,DIRECT`，继续识别域名解析出的内网地址。应用规则优先于后面的 LAN 检查；如果自定义内网域名可能命中应用规则，应在开头显式添加其直连规则。此调整不影响应用规则自身可能触发的 DNS 查询。
