import re
import data_utils

if __name__ == '__main__':
    with open('/users/yucheng/Downloads/test.txt','r') as f:
        text = f.read()
        print(text,'\n\n')
    print(data_utils.clean_text_character(text))
