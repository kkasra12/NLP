from string import  punctuation
from re import findall,sub
from os import chdir
from os.path import dirname,join
DIRNAME=dirname(__file__)

persianLetters="ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیأإآيئؤكٓه"
persianLetters+="ة"
# ZERO WIDTH NON-JOINER (U+200C)
# ZERO WIDTH JOINER (U+200D)
# LEFT-TO-RIGHT MARK (U+200E)
persianSounds="["+"".join(chr(i) for i in range(1611,1632))+"ء"+"]"
extensions=open(join(DIRNAME,"extensions")).read().split("\n")[:-1]
dummyPunctuations="\u22c5\u2032\u2212\u2013\u061b"#+"\u061f\u2061"
dummyPunctuations+="؛؟" # these are persian pronunciations
dummyPunctuations+="{}…"
# DOT OPERATOR' (U+22C5) ==> ⋅
# PRIME (U+2032) ==> ′
# MINUS SIGN (U+2212) ==> −
# EN DASH (U+2013) ==> –
# ARABIC SEMICOLON' (U+061B)
# arabic question mark (U+061F)
# FUNCTION APPLICATION (U+2061)
tokensMap={"PUNCTUATION"        :rf'[!"#$%&\'()*+,\-./:;≈❗️,«»<=>?@\[\\\]\^_`|~،”“.×{dummyPunctuations}]',
           "EMOJI"              :"["+open(join(DIRNAME,"./emojies")).read().replace("\n","")+"]",
           "IP"                 :r"\d\.\d\.\d\.\d",
           "NUMBER"             :r"(?:\d+(?:(?:\.\d+)|\.)?)|(?:\.\d+)",
           # "PERSIAN_WORD"       :f"[{persianLetters}][{persianLetters}{persianSounds}]*[{persianLetters}]?",
           "PERSIAN_WORD"       :f"[{persianLetters}]+[{persianLetters}\u200c\u200d]*[{persianLetters}]+",
           "ENGLISH_WORD"       :r"[A-Za-z]+(?:\'[a-z]+)?",
           "SENTENCE_DELIMITERS":r"[.?!؟]",
           "ENGLISH_HUMAN_NAME" :r"(?:(?i)mr|mis|miss)\.[A-Za-z][a-z]+",
           "FILE_NAME"          :rf"(?i)[a-z0-9\._\-()!@#$%^&]+\.(?:{'|'.join(extensions)})",
           "LINK"               :r"(?:https?:\/\/)?(?:www\.)?[-a-zA-Z0-9%._\+~#=]{1,256}\.[a-zA-Z][a-zA-Z0-9]{0,6}(?:[A-Za-z\-\/0-9_$%]*)(?:#(?:[a-zA-Z0-9]+=[a-zA-Z0-9]*,)*(?:[a-zA-Z0-9]+=[a-zA-Z0-9]*))?",
           "EMAIL"              :r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]+[a-zA-Z0-9])?\.[a-zA-Z0-9](?:[a-zA-Z0-9-]+[a-zA-Z0-9])?",
           "GREEL_LETTERS"      :"[ΑαΒβΓγŋΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσΤτΥυΦφΧχΨψΩω∑∈]",
           "DEGREE"             :r"(\d+°C)|(\d+°F)",
           " LEFT_TO_RIGHT_MARK":"\u200e",
           "NEW_LINE"           :r"\n",
           "SPACE"              :" ",
           "TAB"                :r"\t"
        }


class Token:
    def __init__(self,type,text,regex,pos=(-1,-1)):
        self.type=type
        self.regex=regex
        self.pos=pos
        if type=="NUMBER":
            self.text=str(float(text))
        else:
            self.text=text

    def __eq__(self,other):
        if self.text==other.text and self.type==other.type:
            return True
        return False

    def __str__(self):
        if self.pos!=(-1,-1):
            if self.text=="\n" or self.type=="NEW_LINE":
                return f"<TOKEN type:{self.type} pos:{self.pos}>,['\\n']"
            else:
                return f"<TOKEN type:{self.type} pos:{self.pos}>,[{self.text}]"
        else:
            if self.text=="\n" or self.type=="NEW_LINE":
                return f"<TOKEN type:{self.type}>,['\\n']"
            else:
                return f"<TOKEN type:{self.type}>,[{self.text}]"
            # return f"<TOKEN type:{self.type} regex:{self.regex}>,[{self.text}]"
    def __hash__(self):
        return hash(self.text)
    def __repr__(self):
        return self.__str__()
    def __lt__(self,other):
        if type(other)!=Token:
            raise TypeError(f"'>' not supported between instances of 'Token' and '{type(other)}'")
        return self.text<other.text



if __name__ == '__main__':
    testText="""
hello, this a word /*-+\\,&^%$#@!*()__+=4353 54353 onrb4 c5335
این کلمات فارسی هستنمد و *،٪!٬،
"""
    text="""
سلام، من یک متن هستم که علاوه بر یک  متن معمولی برا
ی تست کردن هم استفاده می‌شوم
"""
    for tokName,tokRegex in tokensMap.items():
        print(f"{tokName},{tokRegex}")
        print(f"{tokName}\t{findall(tokRegex,text)}")
        print("-"*20)
