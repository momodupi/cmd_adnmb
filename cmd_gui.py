import adnmb
            
import curses

from time import sleep


'''
def gui_disp_menu(m_list, pos):
    m_l = curses.LINES - 4
    m_c = curses.COLS - 4

    total_page = int(len(m_list)/m_l)
    m_page = int((pos-1)/m_l)

    pad = curses.newpad(m_l, m_c)
    editwin = curses.newwin(5, 30, 2, 1)

    l_page = []
    for i in range(0, total_page+1):
        l_page.append([])

    cnt = 0
    for l in m_list:
        l_page[int(cnt/m_l)].append(l)
        cnt = cnt+1

    cnt = 0
    for l in l_page[m_page]:
        l_str = "{}. {}".format(m_page*m_l+cnt+1, l.get('title'))
        if (m_page*m_l+cnt+1) == pos:
            pad.addstr(cnt, 0, l_str, curses.A_BOLD + curses.color_pair(3))
        else:
            pad.addstr(cnt, 0, l_str, curses.A_NORMAL)

        cnt = cnt+1

    pad.refresh(0,0, 2,0, curses.LINES-1, curses.COLS)
'''
def gui_disp_menu(m_list, pos):
    m_l = curses.LINES - 4
    m_c = curses.COLS - 4

    total_page = int(len(m_list)/(m_l-2))+1

    pad = curses.newpad(m_l, m_c)
    #editwin = curses.newwin(m_l, int(m_c/total_page), 2, 1)

    cnt = 0
    for l in m_list:
        l_str = "{}. {}".format(cnt+1, l.get('title'))
        if (cnt+1) == pos:
            pad.addstr(int(cnt%m_l), int(cnt/m_l)*int(m_c/total_page), l_str, curses.A_BOLD + curses.color_pair(3))
        else:
            pad.addstr(int(cnt%m_l), int(cnt/m_l)*int(m_c/total_page), l_str, curses.A_NORMAL)

        cnt = cnt+1

    pad.refresh(0,0, 2,0, curses.LINES, m_c)


def gui_menu_interface(stdscr, m_list):
    Chn = 1
    while True:
        gui_disp_menu(m_list, Chn)

        i_key = stdscr.getkey()
        if i_key == 'KEY_UP':
            Chn = Chn - 1
        elif i_key == 'KEY_DOWN':
            Chn = Chn + 1
        elif i_key == 'KEY_RIGHT':
            break

        if Chn <= 0:
            Chn = len(m_list)
        elif Chn >= len(m_list):
            Chn = 1
    
    t_list = adnmb.get_thread(m_list[Chn-1].get('href'), 1)
    stdscr.clear()

    return Chn, t_list


def gui_display_thread(stdscr, title, t_list, pos, page):
    stdscr.addstr(0, 0, title, curses.A_BOLD + curses.color_pair(2))
    stdscr.addstr(0, 12, "{:03}/{:03}".format(int(pos),int(page)), curses.A_BOLD + curses.color_pair(2))
    stdscr.refresh()

    m_l = curses.LINES - 4
    m_c = int((curses.COLS - 4)/2)

    #pad = curses.newpad(m_l, m_c)
    pad_m = curses.newpad(1000, m_c)

    t_title = t_list[pos].disp_info()
    t_content = t_list[pos].disp_content()

    pad_m.addstr(0, 0, t_title, curses.A_DIM + curses.color_pair(2))
    pad_m.addstr(1, 0, t_content, curses.A_NORMAL)

    pad_m.refresh(0, 0, 2, 0, curses.LINES-1, m_c)

    if t_list[pos].get_reply_num :
        pad_r = curses.newpad(1000, m_c-4)

        str_pos = 0
        for r in t_list[pos].rpy_list:
            rpy_info = "{} {} {} {} {}\n".format(r.get("id"), r.get("title"), r.get("email"), r.get("createdat"), r.get("uid"))
            rpy_content = "{}\n".format(r.get("content").strip())
            str_len = int(len(rpy_content)/m_l)+2

            pad_r.addstr(str_pos, 0, rpy_info, curses.A_DIM + curses.color_pair(2))
            pad_r.addstr(str_pos+1, 0, rpy_content, curses.A_NORMAL)
            str_pos = str_pos + str_len + 2

        pad_r.refresh(0, 0, 2, m_c+2, curses.LINES-1, curses.COLS - 4)

'''
def gui_display_reply(stdscr, r_list, pos, page):
    stdscr.addstr(0, 0, title, curses.A_BOLD + curses.color_pair(2))
    stdscr.addstr(0, 12, "{:03}/{:03}".format(int(pos),int(page)), curses.A_BOLD + curses.color_pair(2))
    stdscr.refresh()

    m_l = curses.LINES - 4
    m_c = int((curses.COLS - 4)/2)

    #pad = curses.newpad(m_l, m_c)
    pad = curses.newpad(1000, m_c)

    t_title = t_list[pos].disp_info()
    t_content = t_list[pos].disp_content()

    pad.addstr(0, 0, t_title, curses.A_DIM + curses.color_pair(2))
    pad.addstr(1, 0, t_content, curses.A_NORMAL)

    pad.refresh(0,0, 2,0, curses.LINES-1, m_c)
'''

def main(stdscr):
    
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # set title
    stdscr.addstr(0, 0, "A岛匿名版", curses.A_BOLD + curses.color_pair(2))
    stdscr.refresh()

    # request borad nav
    m_list = adnmb.get_menu()
    
    # display nav
    '''
    Chn = 1
    while True:
        gui_disp_menu(m_list, Chn)

        i_key = stdscr.getkey()
        if i_key == 'KEY_UP':
            Chn = Chn - 1
        elif i_key == 'KEY_DOWN':
            Chn = Chn + 1
        elif i_key == 'KEY_RIGHT':
            break

        if Chn <= 0:
            Chn = len(m_list)
        elif Chn >= len(m_list):
            Chn = 1
    '''
    Chn, t_list = gui_menu_interface(stdscr, m_list)
    #t_list = adnmb.get_thread(m_list[Chn-1].get('href'))
    
    stdscr.clear()
    #stdscr.addstr(0, 0, m_list[int(Chn-1)].get('title'), curses.A_BOLD + curses.color_pair(2))
    #stdscr.refresh()

    Thd_pos = 1
    Thd_page = 1

    '''
    #stdscr.addstr(0, 0, title, curses.A_BOLD + curses.color_pair(2))
    #stdscr.addstr(0, 12, "{:03}/{:03}".format(int(pos),int(page)), curses.A_BOLD + curses.color_pair(2))
    #stdscr.refresh()

    m_l = curses.LINES - 4
    m_c = int((curses.COLS - 4)/2)

    #pad = curses.newpad(m_l, m_c)
    pad = curses.newpad(1000, m_c)
    
    t_title = t_list[pos].disp_info()
    t_content = t_list[pos].disp_content()
    
    str_pos = 0
    for t in t_list:
        t_title = t.disp_info()
        t_content = t.disp_content()
        str_len = int(len(t_content)/m_l)+2
        pad.addstr(str_pos, 0, t_title, curses.A_DIM + curses.color_pair(2))
        pad.addstr(str_pos+1, 0, t_content, curses.A_NORMAL)
        #str_pos, curs_x = curses.getsyx()
        str_pos = str_pos + str_len + 2

    pad.refresh(0,0, 2,0, curses.LINES-1, m_c)
    '''


    while True:
        gui_display_thread(stdscr, m_list[Chn-1].get('title'), t_list, Thd_pos, Thd_page)
        #pad.refresh(Thd_pos,0, 2,0, curses.LINES-1, m_c)

        i_key = stdscr.getkey()
        if i_key == 'KEY_UP':
            Thd_pos = Thd_pos - 1
        elif i_key == 'KEY_DOWN':
            Thd_pos = Thd_pos + 1
        elif i_key == 'KEY_LEFT':
            Chn, t_list = gui_menu_interface(stdscr, m_list)
        elif i_key == 'KEY_RIGHT':
            a=1
        else:
            break

        
        if Thd_pos <= 0:
            Thd_page = Thd_page-1
            if Thd_page < 1:
                Thd_page = 1
                Thd_pos = 1
                t_list = adnmb.get_thread(m_list[Chn-1].get('href'), Thd_page)
                if Thd_page == 1:
                    Thd_pos = 1
            else:
                t_list = adnmb.get_thread(m_list[Chn-1].get('href'), Thd_page)
                Thd_pos = len(t_list)-1

        elif Thd_pos >= len(t_list):
            Thd_page = Thd_page+1
            t_list = adnmb.get_thread(m_list[Chn-1].get('href'), Thd_page)
            Thd_pos = 1
        '''
        if Thd_pos >= str_pos:
            Thd_pos = str_pos
        elif Thd_pos <= 0:
            Thd_pos = 0
        '''
            

        


if __name__ == "__main__":
    #main()
    curses.wrapper(main)