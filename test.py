import re
import data_utils

if __name__ == '__main__':
    with open('/users/yucheng/Downloads/test.txt','r') as f:
        text = f.read()
        print(text,'\n\n')

    text = 'ACE2受体的表达主要集中在肺内一小群II型肺泡上皮细胞(AT2)上，这群对病毒易感的AT2细胞占所有AT2细胞数量的1%左右。'
    print(data_utils.clean_text_character(text))
