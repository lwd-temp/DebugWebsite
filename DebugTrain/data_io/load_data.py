from settings import *
import json
import os


class Article:
    """文章内容"""

    def __init__(self):
        self.title = ""
        self.text = ""


class MarkData:
    """标注好的数据"""

    def __init__(self):
        self.err_msg = ""
        self.scenes = []
        self.scene_lines = []
        self.scene_weight = []
        self.solves = []
        self.solve_lines = []
        self.solve_weight = []


def load_articles():
    """读取文章的标题和正文"""
    articles = dict()
    for site in ['cnblogs', 'jianshu', 'oschina']:
        input_path = '../SpiderData/%s/Clean' % site
        f = open(os.path.join(input_path, 'titles.txt'), 'r', encoding='utf8')
        for line in f.readlines():
            aid_tmp = int(line[:line.find('  ')])
            aid = aid_tmp + AID_BASE[site]
            article_title = line[line.find('  ') + 2:]
            articles[aid] = Article()
            articles[aid].title = article_title
            text_filename = os.path.join(os.path.join(input_path, '%05d.txt' % aid_tmp))
            f2 = open(text_filename, 'r', encoding='utf8')
            text = f2.read()
            f2.close()
            articles[aid].text = text
        f.close()
    return articles


def load_mark_data():
    """读取标注好的信息"""

    def split_by_n(str2):
        return str2.replace('\n\n\n', '\n').replace('\n\n', '\n').split('\n')

    all_marked_data = dict()
    for site in ['cnblogs']:  # , 'jianshu', 'oschina']:
        input_path = '../TrainInput/%s' % site
        for filename in os.listdir(input_path):
            aid = int(filename[:filename.find('.json')]) + AID_BASE[site]
            f = open(os.path.join(input_path, filename), 'r', encoding='utf8')
            doc = json.load(f)
            f.close()
            # 获取标注好的文章中的错误信息。
            all_marked_data[aid] = MarkData()
            if 'err_msg' in doc and 'text' in doc['err_msg']:
                all_marked_data[aid].err_msg = doc['err_msg']['text']
                # 获取标注好的场景信息
                if 'scene' in doc and doc['scene']:
                    # 只在有报错信息的情况下，场景信息和解决方案的信息才会有意义
                    if type(doc['scene']) is dict:
                        all_marked_data[aid].scenes = split_by_n(doc['scene']['text'])
                        all_marked_data[aid].scene_lines = doc['scene']['lines']
                        all_marked_data[aid].scene_weight = doc['scene']['weight']
                    elif type(doc['scene']) is list:
                        for t in doc['scene']:
                            all_marked_data[aid].scenes.extend(split_by_n(t['text']))
                            all_marked_data[aid].scene_lines.extend(t['lines'])
                            all_marked_data[aid].scene_weight.extend(t['weight'])
                    else:
                        raise ValueError
            # 获取标注好的解决方案信息
            if 'solve' in doc and doc['solve']:
                if type(doc['solve']) is dict:
                    all_marked_data[aid].solves = split_by_n(doc['solve']['text'])
                    all_marked_data[aid].solve_lines = doc['solve']['lines']
                    all_marked_data[aid].solve_weight = doc['solve']['weight']
                elif type(doc['solve']) is list:
                    for t in doc['solve']:
                        all_marked_data[aid].solves.extend(split_by_n(t['text']))
                        all_marked_data[aid].solve_lines.extend(t['lines'])
                        all_marked_data[aid].solve_weight.extend(t['weight'])
                else:
                    raise ValueError
    return all_marked_data