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

本项目提供分流配置，不提供代理节点。每个人需填写自己的 Surge 格式订阅。

1. 导入 `surge.conf`。首次使用默认直连；示例订阅中的地区项也是直连演示，不会访问虚假节点。
2. 在文本编辑中，将 Airport 行 `policy-path=` 后的示例 URL 替换为自己的完整订阅 URL，并将规则中的 `example.com` 换成订阅域名。
3. 更新 Airport 订阅，在 Proxy🪁 中选择真实地区组或 Airport。若选择 Airport，需要在其中选择真实节点；可临时把 `hidden=1` 改为 `hidden=0` 显示入口。地区筛选依赖节点名称中的香港/HK、美国/US、新加坡/SG、台湾/TW 等关键词。
4. 应用组默认跟随 Proxy🪁；已有配置可能保留旧选择，需要手动确认。Apple 默认直连。
5. 资源下载默认直连。已有可用代理后，若 GitHub 或订阅直连失败，可把资源下载组切换为 Proxy🪁。

如果 GitHub Raw 下载发生 TLS 错误，可以获取 `surge-offline.conf` 文件，通过 Surge 的 Import from Other Apps 导入。此版本内置规则和直连地区演示项，没有生效的远程订阅或图标依赖；按 Airport 附近的注释启用自己的订阅。离线规则是生成时的快照，更新需重新获取文件。

配置尚未下载时，其中的策略不会生效。不能保证 GitHub URL 在所有网络都可访问，可通过聊天、文件共享等方式分发离线配置。不要把个人订阅 Token 提交到公开仓库。

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

QUIC 使用 Surge 原生 `block-quic = all-proxy`：经代理转发的 QUIC 被阻止，让 YouTube 等客户端回退到 HTTPS/TCP；DIRECT 流量可使用 QUIC。不再使用按国家判断的 UDP/443 拦截规则，因此也不再一概拒绝其他相应 UDP/443 流量。该开关影响所有代理 QUIC，不仅限于 YouTube。
