# Personal Surge Rules

这是一个可直接托管到 GitHub 的 Surge 外部规则集仓库。

## 目录

- `rules/openai.list`：OpenAI / ChatGPT
- `rules/apple-ai.list`：Apple Intelligence / Private Relay
- `rules/netflix.list`：Netflix（自动同步）
- `rules/telegram.list`：Telegram（自动同步）
- `rules/twitter.list`：Twitter / X（自动同步）
- `rules/tiktok.list`：TikTok（自动同步）
- `rules/china.list`：中国大陆 IPv4 规则（自动同步）

## Surge 引用

仓库所有者为 `caozzzzz`：

```ini
[Rule]
DOMAIN-SUFFIX,raw.githubusercontent.com,Proxy

RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/openai.list,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/apple-ai.list,Apple-AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/netflix.list,Netflix
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/telegram.list,Telegram,no-resolve
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/twitter.list,Twitter
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/tiktok.list,TikTok
RULE-SET,https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/china.list,DIRECT
GEOIP,CN,DIRECT
FINAL,Final,dns-failed
```

规则集文件内部不包含策略名称。策略由主配置中的 `RULE-SET` 行统一指定。

## 自动更新

GitHub Actions 每天北京时间 06:20 同步上游规则，并在提交前执行格式检查。也可以在仓库的 Actions 页面手动运行 `Sync Surge rules`。
