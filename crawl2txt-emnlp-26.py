import re
import requests
from bs4 import BeautifulSoup

urls = [
    "https://aclanthology.org/volumes/2026.emnlp-main/",
    "https://aclanthology.org/volumes/2026.findings-emnlp/",
    "https://aclanthology.org/volumes/2026.emnlp-demos/",
]

output_paths = [
    "./data/EMNLP-2026-main.txt",
    "./data/EMNLP-2026-findings.txt",
    "./data/EMNLP-2026-demos.txt",
]


def extract_titles(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = []

    for link in soup.select("span.d-block a.align-middle"):
        href = link.get("href", "")
        paper_id = re.fullmatch(
            r"/2026\.(?:emnlp-main|findings-emnlp|emnlp-demos)\.(\d+)/?", href
        )
        # 排除论文集封面（编号为0），只保留论文条目。
        if not paper_id or int(paper_id.group(1)) == 0:
            continue

        # 保留标题内的原始文本连接，避免将格式化的缩写拆成多个单词。
        title = " ".join(link.get_text().split())
        if title:
            titles.append(title)

    return titles


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    for url, output_path in zip(urls, output_paths):
        print("正在爬取网页数据...")
        response = requests.get(url, headers=headers, timeout=90)
        response.raise_for_status()
        response.encoding = 'utf-8'

        titles = extract_titles(response.text)
        if not titles:
            raise ValueError(f"未提取到论文题目，请检查页面结构：{url}")

        with open(output_path, 'w', encoding='utf-8') as f:
            for title in titles:
                f.write(title + "\n")

        print(f"成功爬取并提取了 {len(titles)} 篇论文题目，已保存至 '{output_path}'。")
