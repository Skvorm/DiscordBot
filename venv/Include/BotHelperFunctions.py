import os
import random
import filetype


def get_random_song():
    songs = create_music_list("music")
    song_path = songs[random.randrange(0, len(songs))]
    return song_path


def get_song_choice(user_input):
    songs = create_music_list("music")
    song_path = songs[user_input - 1]
    # print(song_path)
    return song_path


def get_song_list_length():
    return len(create_music_list("music"))


def song_format(song):
    song_name = song.rsplit("\\")[-1]
    songtmp = song_name[:song_name.rindex(".")]
    return songtmp


def get_song_list():
    songs = create_music_list("music")
    ch_ct = 0
    ct = 1
    out = ""
    outtmp = ''
    songtmp = ''
    bl = 2000
    msg_ct = 1
    for song in songs:
        songtmp = song_format(song)
        outtmp = f'{ct}: {songtmp}\n'
        if (len(outtmp) + ch_ct) <= bl:
            out += outtmp
        else:
            # ensures proper output spacing
            # if songlist longer than max Discord message length
            diff = (msg_ct * bl) - len(out) - 1
            out += (diff * " ") + "\n"
            out += outtmp
            # print(f"{ct}:{diff}:{outtmp}")
            ch_ct = 0
            msg_ct += 1

        ct += 1
        ch_ct += len(outtmp)
    return out


def get_roll_range(input_string, max_val=10000, max_die=1000):
    # parses input from !roll command
    # outputs list of[min,max,# of die]
    end = 100
    out = []
    num_die = 1
    param = input_string.replace('!roll', '')
    param = param.strip()
    if param.find('d') != -1:
        param = param.split('d')
        print(param)
        start = 1
        # if parameters greater than limits, uses max values
        # if less, uses default parameters
        if len(param) > 1:
            if param[0] == '':
                param[0] = 1
            if param[1] == '':
                param[1] = 6
        try:
            end = int(param[1])
            num_die = int(param[0])
            # print(f'start{start}:End{end}:NumberDice{num_die}')
        except ValueError:
            # print("Value ERROR")
            end = 6
            num_die = 1
        if end <= 0:
            end = 6
        elif num_die > max_die:
            num_die = max_die
        elif num_die <= 0:
            num_die = 1
        else:
            end = int(param[1])
        if end >= max_val:
            end = max_val
        elif end <= (max_val * -1):
            end = (-1 * max_val)
        out = [start, end, num_die]
        # print(f'{out}:A')
    elif param.find('-') != -1:
        param = param.replace(' ', '')
        ct = param.count('-')
        # print(f'{ct}:{param}')
        if ct == 1:
            if param.startswith('-'):
                param = param[1:]
                param = param.split('-')
                start = -1 * int(param[0])
                end = 0
                # print(f'A{start},{end},{param}')
            else:
                param = param.split('-')
                start = int(param[0])
                end = int(param[1])
                # print(f'B{start},{end},{param}')
        elif ct == 2:
            if param.startswith('-'):
                param = param[1:]
                param = param.split('-')
                start = -1 * (int(param[0]))
                end = int(param[1])
                # print(f'C{start},{end},{param}')
            else:
                param = param.split('-')
                start = int(param[0])
                end = -1 * int(param[1])
                # print(f'D{start},{end},{param}')
        elif ct == 3:
            param = param.split('-')
            # print(param)
            param = list(filter(None, param))
            # print(param)

            start = -1 * int(param[0])
            end = -1 * int(param[1])
            # print(f'E{start},{end},{param}')

        else:
            param = param.split('-')
            start = int(param[0])
            end = int(param[1])
            # print(f'F{start},{end},{param}')
        if end < start:
            tmp = start
            start = end
            end = tmp
        out = [start, end, 1]
    else:
        # print(f'Default {1},{end},{param}')
        try:
            end = int(param)
            if end >= max_val:
                end = max_val
            elif end <= (max_val * -1):
                end = (-1 * max_val)
            if end == 0:
                out = [0, 1, 1]
            elif end == 1:
                out = [0, end, 1]
            elif end > 1:
                out = [1, end, 1]
            elif end < 0:
                out = [end, -1, 1]
        except ValueError:
            out = [1, 100, 1]
        # min,max,times rolled
        # out = [1, 100, 1]
    # print(out)
    return out


def parse_poll(input_string, delimiter="!~"):
    quest = ""
    ans = []
    parse_list = []
    param = input_string.replace('!poll', '')
    param = param.strip()
    if param.find(delimiter) != -1:
        param = param.split(delimiter)
        if len(param) > 1:
            quest = param[0]
            ans = param[1:len(param)]
    else:
        quest = param
        ans = ["Yes", "No"]
    parse_list = [quest, ans]
    return parse_list


def parse_song(input_string):
    param = input_string.replace('!music', '')
    param = param.strip()
    param = param.split(" ")[0]
    try:
        param = int(param)
        if param <= 0:
            param = -1
    except ValueError:
        param = -1
    return param


# returns flat list of all playable media files
def create_music_list(path):
    music_list = []
    dir_list = []
    c = os.scandir(path)
    for f in c:
        # print(f"{f.name}-{f.is_file()}")
        if f.is_dir():
            tmp_list = create_music_list(f.path)
            # ensures flat list is returned
            for tf in tmp_list:
                music_list.append(tf)
        elif f.is_file():
            if filetype.is_audio(f.path):
                music_list.append(f.path)
    c.close()
    return music_list


# returns dictionary of media files
# folder:[list of playable files in folder]
def create_music_list_dir(path):
    music_list = []
    dir_list = {}
    c = os.scandir(path)
    for f in c:
        if f.is_dir():
            tmp_list = create_music_list(f.path)
            for tf in tmp_list:
                dir_list[f.path] = tmp_list
        elif f.is_file():
            if filetype.is_audio(f.path):
                music_list.append(f.path)
    dir_list[path] = music_list
    c.close()
    return dir_list


class BotHelperFunctions:
    pass


if __name__ == '__main__':
    d = BotHelperFunctions()
    #  tmp = parse_song("!music 9")
    #  tmp = parse_song("!music")
    #   print(str(tmp) + ":" + str(parse_song("!music")))
    # tmp=create_music_list_dir("music")
    ####       print(f'{song_format(song)}')
    print(get_roll_range("3d20"))
