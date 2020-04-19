# First Exercise - Word Tokenizer

Word tokenization is the process of splitting a large sample of text into words. This is a requirement in natural language processing tasks where each word needs to be captured and subjected to further analysis like classifying and counting them for a particular sentiment etc.
To achieve this goal we have implemented a class named `Token` and we will assign each token to one instance of this class.

## Overall Approach

If we use space character to separate words we may face many problems, as a solid example, punctuation marks which has no space with words, or numbers may have no space with dots(in IP addresses for-example).
To avoid this problems we have defined some *regex* in `tokens.tokensMap` in which each token name has mapped to its specific regex. And `wordTokenizer.wordTokenizer` function will search the text in `sampleText` file for longest occurrence of this regex.
several major programming problems which we have faced are listed below:

- we couldn't use recursive approach because recursion depth causes number of limitations, this problem paves the way for using a simple *loop*
- As searching the whole text for all of the regexes in each step(using *backTracking* method) waste plenty of time, the program searches for each tokens between two spaces.

Below you can see the regexes for which we are searching:
```python
persianLetters="ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیأإآيئؤكٓه"+"\u200c\u200d\u200e"+"ة"
# ZERO WIDTH NON-JOINER=(U+200C) ZERO WIDTH JOINER=(U+200D) LEFT-TO-RIGHT MARK=(U+200E)
persionSounds="".join(chr(i) for i in range(1611,1632))+"ء"
extensions=open("extensions").read().split("\n")[:-1]
dummyPunctuations="\u22c5\u2032\u2212\u2013\u061b\u061f\u2061"
dummyPunctuations+="؛؟" # these are persian pronunciations
dummyPunctuations+="{}…"
tokensMap={"PUNCTUATION"        :rf'[!"#$%&\'()*+,\-./:;≈❗️,«»<=>?@\[\\\]\^_`|~،”“.×{dummyPunctuations}]',
           "EMOJI"              :"["+open("emojies").read().replace("\n","")+"]",
           "IP"                 :r"\d\.\d\.\d\.\d",
           "NUMBER"             :r"(?:\d+(?:٫\d+)?)|(?:\d+(?:\.\d+)?)",
           "UNSTRUCTURED_NUMBER":r"[\d٫]+|[\d\.]+",
           "PERSIAN_WORD"       :f"[{persianLetters}][{persianLetters}{persionSounds}]*[{persianLetters}]?",
           "ENGLISH_WORD"       :r"[A-Za-z]+",
           "ENGLISH_HUMAN_NAME" :r"(?:(?i)mr|mis|miss)\.[A-Za-z][a-z]+",
           "FILE_NAME"          :rf"(?i)[a-z0-9\._\-()!@#$%^&]+\.(?:{'|'.join(extensions)})",
           "LINK"               :r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z][a-zA-Z0-9()]{0,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=,]*)",
           "EMAIL"              :r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]+[a-zA-Z0-9])?\.[a-zA-Z0-9](?:[a-zA-Z0-9-]+[a-zA-Z0-9])?",
           "GREEL_LETTERS"      :"[ΑαΒβΓγŋΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσΤτΥυΦφΧχΨψΩω∑∈]",
           "DEGREE"             :r"(\d+°C)|(\d+°F)",
           "NEW_LINE"           :r"\n",
           "SPACE"              :" ",
           "TAB"                :r"\t"
        }
```
Also there is some tips, we should concern about:

- Sounds between words should not break the letter and should not make new letter either.For instance the word
"سلام"
and
"سَلام"
are same word and both are single word.\
to solve these problems, first of all `PERSIAN_WORD` regex accepts Persian sounds only in the middle of word, Also we omit all persianSounds before saving each token.
- There is a letter 'ء' in Persian (I'm not sure if it is a letter) that was common in old texts, but nowadays this letter is omitted. This letter is added into `persianSounds`.
- There is two kind of **ZERO WIDTH SPACE**(standard and non-standard keyboard)
- There is a **LEFT-TO-RIGHT MARK** which is frequently used in persian texts.
- Vast types of tokens are supported(approximately vast!!!)

## Execution

The `wordTokenizer.wordTokenizer` function will return a list containing all of the tokens in same order as the text.This part of code will calculate this  exercise goal:
```Python
text=open("sampleText").read()
tokensFile=open("foundedTokens","w")
errorsFile=open("errorChars","w")
wordCounterFile=open("wordCounterFile.md","w")
print("Searching for tokens...")
startTime=time()
foundedTokens,errorChars=wordTokenizer(text)
print(f"Totally {len(foundedTokens)} tokens found in {time()-startTime:.4f}seconds\nwriting the results to files...")
errorsFile.write("\n".join(str(i)+"\n\tcode: "+str(ord(i.text)) for i in set(errorChars)))
for i in foundedTokens:
    tokensFile.write(str(i)+"\n")
wordFrequency=wordCounter(foundedTokens)
# print(wordFrequency)
wordCounterFile.write("|index|token|frequency|\n|:-:|:-|:-:|\n")
wordCounterFile.write("\n".join(f"|{index}|\\{i}|{j}|" for index,(i,j) in enumerate(sorted(wordFrequency.items(),key=lambda x:x[1]))))
```
`sampleText` file contains **153449** characters

## Output
```bash
$ python3 wordTokenizer.py
Searching for tokens...
Totally 68564 tokens found in 9.1284 seconds
writing the results to files...
```

result table is available below:

|index|token|frequency|
|:-:|:-|:-:|
|5010|\<TOKEN type:PUNCTUATION pos:(12569, 12570)>,[=]|103|
|5011|\<TOKEN type:PERSIAN_WORD pos:(253, 255)>,[بر]|104|
|5012|\<TOKEN type:PERSIAN_WORD pos:(1330, 1333)>,[های]|106|
|5013|\<TOKEN type:PERSIAN_WORD pos:(9991, 9993)>,[یا]|109|
|5014|\<TOKEN type:ENGLISH_WORD pos:(11901, 11913)>,[displaystyle]|111|
|5015|\<TOKEN type:PERSIAN_WORD pos:(707, 709)>,[ها]|114|
|5016|\<TOKEN type:PUNCTUATION pos:(12247, 12248)>,[_]|119|
|5017|\<TOKEN type:PERSIAN_WORD pos:(4564, 4567)>,[شده]|123|
|5018|\<TOKEN type:PERSIAN_WORD pos:(4509, 4511)>,[آن]|130|
|5019|\<TOKEN type:PUNCTUATION pos:(62, 63)>,[:]|169|
|5020|\<TOKEN type:ENGLISH_WORD pos:(11942, 11943)>,[d]|173|
|5021|\<TOKEN type:PUNCTUATION pos:(24933, 24934)>,[*]|186|
|5022|\<TOKEN type:PERSIAN_WORD pos:(1032, 1034)>,[یک]|193|
|5023|\<TOKEN type:PUNCTUATION pos:(4322, 4323)>,[(]|194|
|5024|\<TOKEN type:PUNCTUATION pos:(4341, 4342)>,[)]|196|
|5025|\<TOKEN type:ENGLISH_WORD pos:(11897, 11898)>,[t]|210|
|5026|\<TOKEN type:PERSIAN_WORD pos:(4926, 4930)>,[برای]|219|
|5027|\<TOKEN type:PERSIAN_WORD pos:(431, 434)>,[است]|281|
|5028|\<TOKEN type:PERSIAN_WORD pos:(147, 149)>,[با]|293|
|5029|\<TOKEN type:PUNCTUATION pos:(6233, 6234)>,[,]|296|
|5030|\<TOKEN type:PERSIAN_WORD pos:(722, 724)>,[را]|347|
|5031|\<TOKEN type:PERSIAN_WORD pos:(104, 106)>,[که]|371|
|5032|\<TOKEN type:PERSIAN_WORD pos:(49, 52)>,[این]|423|
|5033|\<TOKEN type:PUNCTUATION pos:(11900, 11901)>,[\]|447|
|5034|\<TOKEN type:ENGLISH_WORD pos:(24943, 24947)>,[link]|477|
|5035|\<TOKEN type:PUNCTUATION pos:(11899, 11900)>,[{]|495|
|5036|\<TOKEN type:PUNCTUATION pos:(11915, 11916)>,[}]|495|
|5037|\<TOKEN type:PERSIAN_WORD pos:(0, 2)>,[به]|559|
|5038|\<TOKEN type:PERSIAN_WORD pos:(107, 109)>,[از]|624|
|5039|\<TOKEN type:PERSIAN_WORD pos:(36, 38)>,[در]|735|
|5040|\<TOKEN type:PUNCTUATION pos:(18, 19)>,[،]|742|
|5041|\<TOKEN type:PERSIAN_WORD pos:(354, 355)>,[و]|859|
|5042|\<TOKEN type:PUNCTUATION pos:(198, 199)>,[.]|915|
|5043|\<TOKEN type:PUNCTUATION pos:(213, 214)>,[-]|2370|
|5044|\<TOKEN type:NEW_LINE pos:(199, 200)>,[]|2390|
|5045|\<TOKEN type:SPACE pos:(2, 3)>,[ ]|32047|

**NAME:** Kasra Eskandari<br>
**STD ID:** 955361005
