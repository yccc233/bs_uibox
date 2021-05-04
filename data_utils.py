

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