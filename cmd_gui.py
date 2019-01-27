import adnmb
            
import curses

from time import sleep



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


def gui_display_thread(t_list, pos):
    t_str = ""

    m_l = curses.LINES - 4
    m_c = curses.COLS - 4

    pad = curses.newpad(m_l, m_c)

    t_title = t_list[pos].disp_info()
    t_content = t_list[pos].disp_content()

    pad.addstr(0, 0, t_title, curses.A_DIM + curses.color_pair(2))
    pad.addstr(1, 0, t_content, curses.A_NORMAL)


    pad.refresh(0,0, 2,0, curses.LINES-1, curses.COLS)


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
            Chn = 1
        elif Chn >= len(m_list):
            Chn = len(m_list)

    t_list = adnmb.get_thread(m_list[int(Chn-1)].get('href'))
    
    stdscr.clear()
    stdscr.addstr(0, 0, m_list[int(Chn-1)].get('title'), curses.A_BOLD + curses.color_pair(2))
    stdscr.refresh()

    Chn = 1
    while True:
        gui_display_thread(t_list, Chn)

        i_key = stdscr.getkey()
        if i_key == 'KEY_UP':
            Chn = Chn - 1
        elif i_key == 'KEY_DOWN':
            Chn = Chn + 1
        else:
            break

        if Chn <= 0:
            Chn = 1
        elif Chn >= len(t_list):
            Chn = len(t_list)


    sleep(10)

    # input nav number
    #stdscr.addstr(curses.LINES-1, 0, "请选择板块：", curses.A_DIM + curses.color_pair(2))
    #Chn = int(stdscr.getch())-1
    #stdscr.addstr(curses.LINES-1, 16, m_list[int(Chn)].get('title'), curses.A_NORMAL + curses.color_pair(2))
    #stdscr.refresh()

    #t_list = adnmb.get_thread(m_list[int(Chn)].get('href'))
    sleep(10)

if __name__ == "__main__":
    #main()
    curses.wrapper(main)