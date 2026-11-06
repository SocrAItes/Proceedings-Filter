import requests
from bs4 import BeautifulSoup


urls = [
    "https://proceedings.mlr.press/v202/",
    "https://proceedings.mlr.press/v235/",
    "https://proceedings.mlr.press/v267/",
    "https://proceedings.mlr.press/v306/",
]

output_paths = [
    "./data/ICML-2023.txt",
    "./data/ICML-2024.txt",
    "./data/ICML-2025.txt",
    "./data/ICML-2026.txt",
]

if __name__ == '__main__':

    for url, output_path in zip(urls, output_paths):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # 发送 GET 请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 解析 HTML 网页
        soup = BeautifulSoup(response.text, "html.parser")

        paper_divs = soup.find_all("div", class_="paper")

        titles = []
        for paper in paper_divs:
            title_p = paper.find("p", class_="title")
            if title_p:
                title_text = " ".join(title_p.get_text().split())
                if title_text:
                    titles.append(title_text)

        # 保存到 txt
        with open(output_path, "w", encoding="utf-8") as f:
            for title in titles:
                f.write(title + "\n")

        print(f"爬取完成，共提取 {len(titles)} 条论文标题，已保存至 {output_path}")
