"""
使用arxiv库搜索论文并下载
"""
import os
import arxiv
import requests
from tqdm import tqdm

# 数据保存路径
DATA_FOLDER = "data/download"
# 如果数据保存路径不存在，则创建
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


def search_papers(query, max_results):
    # 定义搜索参数
    print(f"Searching for papers with query: {query}")
    search = arxiv.Search(
        query=query,  # 搜索关键词
        max_results=max_results,  # 最大返回结果数
        sort_by=arxiv.SortCriterion.SubmittedDate  # 按提交日期排序
    )

    # 使用 Client().results() 替代 search.results()
    results = list(arxiv.Client().results(search))  # 转换为列表以便多次使用

    # 输出搜索结果
    for result in results:
        print(result.entry_id, '->', result.title)
    return results


def download_paper(paper_url, save_path):
    try:
        response = requests.get(paper_url, timeout=30)  # 添加超时设置
        response.raise_for_status()  # 检查HTTP错误
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f'下载成功: {save_path}')
    except requests.exceptions.Timeout:
        print(f'下载超时: {paper_url}')
    except requests.exceptions.HTTPError as e:
        print(f'HTTP错误: {response.status_code} - {paper_url}')
    except requests.exceptions.RequestException as e:
        print(f'下载出错: {str(e)} - {paper_url}')
    except IOError as e:
        print(f'文件保存错误: {str(e)} - {save_path}')


def main(query, max_results):
    # 示例：下载第一篇论文
    results = search_papers(query, max_results)
    print(f"Found {len(results)} papers")
    for result in tqdm(results, desc="Downloading papers", total=len(results)):
        pdf_url = result.pdf_url  # 获取PDF链接
        download_paper(pdf_url, f"{DATA_FOLDER}/{result.title}.pdf")
        # 保存为论文标题命名的文件


if __name__ == "__main__":
    main("Reinforcement Learning", 10)
