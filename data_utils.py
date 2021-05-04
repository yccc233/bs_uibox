import re


def split_text_to_sentences(text):
    # 文本数据清洗，文本转句子
    text.replace('\t', '')
    text.replace('\n', '')
    return text.split('。')


def classify_kind_to_list(predict):
    # 分类json格式的返回值，按照covid，gene，phen，protein顺序返回列表
    covid = gene = phen = protein = []
    if 'COVID' in predict:
        covid = predict['COVID']
    if 'GENE' in predict:
        gene = predict['GENE']
    if 'PHEN' in predict:
        phen = predict['PHEN']
    if 'DISEASE' in predict:
        phen = phen + predict['DISEASE']   # 目前将疾病和表型合并
    if 'PROTEIN' in predict:
        protein = predict['PROTEIN']
    return covid, gene, phen, protein


def handle_list_to_highlight(covid, gene, phen, protein):
    hl = []
    for c in covid:
        hl.append(['COVID', c])
    for g in gene:
        hl.append(['GENE', g])
    for p in phen:
        hl.append(['PHEN', p])
    for p in protein:
        hl.append(['PROTEIN', p])
    return hl


def getDouble_by_sentence(predict):
    # 通过一句话的分析获取两元组的关系，返回一个二维列表，具体index包括种类1，name1，种类2，name2
    # 第一层是covid，第二层是gene，第三层是phen
    # protein也属于第二层，disease属于第三层
    dou = []
    GENE = []
    PHEN = []
    # 获取基因型，gene和protein重复的即忽略
    if 'GENE' in predict:
        GENE+=predict['GENE']
    elif 'PROTEIN' in predict:
        GENE+=predict['PROTEIN']

    if 'PHEN' in predict:
        PHEN+=predict['PHEN']
    if 'DISEASE' in predict:
        PHEN+=predict['DISEASE']

    if 'COVID' in predict:  # 有新冠关键字
        if GENE:
            for gene in GENE:
                dou.append(['covid','COVID-19','gene',gene])
        if PHEN:
            for phen in PHEN:
                dou.append(['covid', 'COVID-19', 'phen', phen])
        if GENE and PHEN:
            for gene in GENE:
                for phen in PHEN:
                    dou.append(['gene',gene,'phen',phen])
    else:  # 无新冠关键字
        if GENE and PHEN:
            for gene in GENE:
                for phen in PHEN:
                    dou.append(['gene',gene,'phen',phen])
    return dou


# 清洗文本数据
def clean_sentences(sentences):
    for sen in sentences:  # 删除空元素
        if not sen:
            sentences.remove(sen)
    return sentences


# 清洗实体识别数据，这是个二维数组
def clean_entities_from_predict(entitis):
    tar_entitis = []
    for entity in entitis:
        if entity not in tar_entitis and not re.search(r"[()（）%@&*$¥#!]", entity[1]):
            entity[1] = entity[1].replace('_','-')
            tar_entitis.append(entity)
    return tar_entitis


if __name__ == '__main__':
    entities = [['COVID', '新型冠状病毒2019_nCOV'], ['PROTEIN', '受体基因血管紧张素转化酶2'], ['PROTEIN', 'Angi'], ['GENE', 'ACE2'], ['GENE', 'ACE2'], ['GENE', '能(Gene '], ['GENE', '%的AC'], ['PROTEIN', 'Caveolin蛋白'], ['PHEN', '阻断病毒感染'], ['COVID', '新冠'], ['GENE', '过与AC'], ['PHEN', '引起细胞'], ['PHEN', '性和肾功能'], ['COVID', '当对新冠'], ['PHEN', '发现肾功能']]
    print(entities)
    entities = clean_entities_from_predict(entities)
    print(entities)

    print(re.search(r"[()（）\%@&*$¥#!]", '%的AC'))