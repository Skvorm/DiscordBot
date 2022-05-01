import os
import filetype
from itertools import chain
class TestingClass:
    def create_music_list(self,path):
        music_list=[]
        dir_list=[]
        c=os.scandir(path)
        for f in c:
            print(f"{f.name}-{f.is_file()}")
            if f.is_dir():
               tmplist=self.create_music_list(f.path)
               #ensures flat list is returned
               for tf in tmplist:
                   music_list.append(tf)
            elif f.is_file():
                if filetype.is_audio(f.path):
                    music_list.append(f.name)
        c.close()
        return music_list
if __name__ == '__main__':
    tc= TestingClass()
    song_list=tc.create_music_list("music")
    print(len(song_list))