from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/caozzzzz/surge-rules/main/rules/'


def build():
    text = (ROOT / 'surge.conf').read_text(encoding='utf-8')
    samples = '\n'.join(line for line in (ROOT / 'examples/subscription.list').read_text(encoding='utf-8').splitlines() if line and not line.startswith('#'))
    text = text.replace('[Proxy]\n', '[Proxy]\n' + samples + '\n')
    output = ['# 离线通用版：规则内置，默认直连；不包含真实代理服务。']
    expanded = 0
    for line in text.splitlines():
        if line.startswith('Airport ='):
            output.extend([
                '# 填写订阅：删除下面生效的 Airport 行，再取消下一行注释并替换 policy-path 后的 URL。',
                '# ' + line.replace('https://raw.githubusercontent.com/caozzzzz/surge-rules/main/examples/subscription.list', 'https://example.com/your-surge-subscription'),
                'Airport = select,DIRECT,include-all-proxies=true,hidden=1',
            ])
            continue
        if line.startswith('geoip-maxmind-url ='):
            output.append('# 离线版使用 Surge 内置 GeoIP 数据库。')
            continue
        if line.startswith('RULE-SET,' + BASE):
            _, url, policy, *flags = line.split(',')
            path = ROOT / 'rules' / url.removeprefix(BASE)
            output.append('# 内置规则：' + path.name)
            for rule in path.read_text(encoding='utf-8-sig').splitlines():
                if not rule.strip() or rule.startswith(('#', ';', '//')):
                    continue
                fields = rule.split(',')
                options = []
                while fields[-1] in ('no-resolve', 'extended-matching'):
                    options.insert(0, fields.pop())
                for flag in flags:
                    if flag == 'extended-matching' and fields[0] not in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-WILDCARD', 'URL-REGEX'):
                        continue
                    if flag == 'no-resolve' and fields[0] not in ('IP-CIDR', 'IP-CIDR6', 'IP-ASN', 'GEOIP'):
                        continue
                    if flag not in options:
                        options.append(flag)
                output.append(','.join([*fields, policy, *options]))
                expanded += 1
            continue
        if not line.startswith('#'):
            line = re.sub(r',icon-url=[^,\s]+', '', line)
        output.append(line)
    result = '\n'.join(output) + '\n'
    active = [l for l in result.splitlines() if l and not l.startswith('#')]
    assert not any('policy-path=' in l or 'icon-url=' in l or l.startswith('RULE-SET,' + BASE) for l in active)
    (ROOT / 'surge-offline.conf').write_text(result, encoding='utf-8')
    print(f'Built offline profile with {expanded} embedded rules')


if __name__ == '__main__':
    build()
