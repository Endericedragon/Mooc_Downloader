import re
import os
import pickle

def namer(num):
    if num<10:
        return '000'+str(num)
    elif num<100:
        return '00'+str(num)
    elif num<1000:
        return '0'+str(num)
    else:
        return str(num)

def m3u8Process(courseName, courseDict):
    rawPat = re.compile('^https?://.+/\d{4}/\d{2}/\d{2}/')
    for week, sections in courseDict.items():
        for section, vidInfo in sections.items():
            path = courseName+'\\'+week+'\\'+section
            #文件路径
            for vidName, detail in vidInfo.items(): #vidName没有后缀名
                if detail['format']!='m3u8':
                    continue
                elif os.path.exists(path+'\\'+vidName+'.mp4'):
                    continue
                for vid in os.listdir(path): #vid带有后缀名
                    if re.search(vidName, vid) and 'mp4' not in vid:
                        origin_path = os.getcwd()
                        fg = origin_path+'\\ffmpeg\\bin\\ffmpeg'
                        os.chdir(path)
                        cc = 0
                        rawUrl = vidInfo[vidName]['url']
                        url = rawPat.match(rawUrl).group()
                        # ~ print(vid)
                        with open(vid, 'r') as f:
                            tsInfo = f.readlines()
                        for each in tsInfo:
                            each = each.strip()
                            if each[0]!='#':
                                print('{2} -n -i \"{0}\" \"{1}.mp4\"'.format(url+each, namer(cc), fg))
                                os.system('{2} -n -i \"{0}\" \"{1}.mp4\"'.format(url+each, namer(cc), fg))
                                cc+=1
                        with open('temp.txt', 'w') as f:
                            for i in range(cc):
                                f.write('file \'{0}.mp4\'\n'.format(namer(i)))
                        print('{1} -n -f concat -i \"temp.txt\" \"{0}.mp4\"'.format(vidName, fg))
                        os.system('{1} -n -f concat -i \"temp.txt\" \"{0}.mp4\"'.format(vidName, fg))
                        os.system('del temp.txt')
                        os.remove(vid)
                        for ck in range(cc):
                            os.system('del \"{0}.mp4\"'.format(namer(ck)))
                        os.chdir(origin_path)

def test():
    with open('tempDict.pck', 'rb') as f:
        d = pickle.load(f)
    m3u8Process('音乐奥秘解码——轻松学乐理_中国大学MOOC(慕课)', d)
if __name__=='__main__':
    test()
