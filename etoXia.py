import xiami
import music163

def trans_collect(se,collect_id):
    collect = music163.get_music_list_from_collect(collect_id)
    collect_info = collect[0]
    music_list = collect[1]
    write(collect_info['title'] + '--' + collect_id + '\n')
    x_collect_id = xiami.create_collect(se, collect_info['title'])
    write("虾米歌单id" + x_collect_id)
    for music in music_list:
        try:
            x_music = xiami.search_music(music)
            xiami.add_music_to_collect(se, x_music['id'], x_collect_id)
            write(str(music) + '--->' + str(x_music) + '\n')
        except Exception as e:
            write('add failed' + str(music) + '\n')
            if x_music == None:
                write('can not find it in xiami.com')

def write(content):
    with open('EtoXia.log' , 'a') as f:
        f.write(content)

if __name__ == '__main__':
    se = xiami.login()
    trans_collect(se, '519140070')   
    # collectid_list = music163.get_collect_list()
    # for collect in collectid_list:
        # try:
            # trans_collect(se, collect)
        # except:
            # print('error when collect' + collect)
