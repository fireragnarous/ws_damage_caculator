from queue import Queue
import random
import matplotlib.pyplot as plt


##输入残局参数
queue_deal=Queue()   #队列中0代表角色或事件，1代表高潮卡



def deal_to_clock():      #从处理去将卡片放置到时计区
    global clock,climax_clock,drop,climax_drop,queue_deal
    while not queue_deal.empty():
        next_clock=queue_deal.get()
        if next_clock==0:
            clock+=1
        else:
            clock+=1
            climax_clock+=1
        level_up_check()

def level_up_check():          #插入升级操作
    global clock, level,climax_clock,drop,climax_drop
    if clock==7:
        clock=0
        drop=drop+6
        climax_drop=climax_drop+climax_clock
        climax_clock=0
        level+=1

def draw(draw_number):                          #抽卡
    global deck,climax_deck
    for i in range (0,draw_number):
        ratio=climax_deck/deck
        # print(deck,climax_deck,ratio)
        if top_not_climax>0:
            climax_or_not =1
            top_not_climax=top_not_climax-1
        else:
            climax_or_not = random.random()
        # print(climax_or_not)
        if climax_or_not>=ratio:   #判定抽到的是否是潮
            deck = deck - 1
            if deck==0:
                new_deck()
        else:
            deck = deck - 1
            climax_deck=climax_deck -1
            if deck==0:
                new_deck()

def new_deck():                          #卡更
    global deck,climax_deck,drop,climax_drop
    deck=drop
    climax_deck=climax_drop
    drop=0
    climax_drop=0
    rule_clock_add(1)

def rule_clock_add(addnumber):                    #规则罚血，包含卡更或者卡组直接烫血，不包括将场上或者控室的角色射血
    global deck, climax_deck,clock,climax_clock
    for i in range (0,addnumber):
        ratio=climax_deck/deck
        # print(deck,climax_deck,ratio)
        climax_or_not=random.random()
        if climax_or_not > ratio:        #射血不是潮
            # print("没罚潮")
            clock+=1
            deck=deck-1
            level_up_check()
        else:                            #射血是潮
            # print("罚潮")
            clock+=1
            climax_clock+=1
            deck=deck-1
            climax_deck=climax_deck-1
            level_up_check()

def damage_can_be_cancelled(damage_number):
    global deck,climax_deck,deal,climax_deal,queue_deal,drop,climax_drop,top_not_climax
    tmp_queue=Queue()
    whether_cancelled=0        #0代表未取消，1代表轻松取消
    for i in range (0,damage_number):
        ratio=climax_deck/deck
        # print(deck,climax_deck,ratio)
        if top_not_climax>0:
            climax_or_not =1
            top_not_climax=top_not_climax-1
        else:
            climax_or_not = random.random()
        # print(climax_or_not)
        if climax_or_not>=ratio:   #判定翻出来的是否是潮，随机数大于潮的浓度时认为翻出来的是血
            tmp_queue.put(0)
            deck=deck-1
            if deck==0:
                new_deck()
            # print("肉！")
        else:
            whether_cancelled=1           #标记取消成功，卡组数量减少翻血次数，卡组潮-1，控室卡片数量增加翻血次数，控室高潮卡数量加1
            deck=deck-1
            climax_deck=climax_deck-1
            if deck == 0:
                new_deck()
            drop=drop+i+1
            climax_drop+=1
            break
    if whether_cancelled==0:        #未取消则翻出的血量进入处理区
        while not tmp_queue.empty():
            queue_deal.put(tmp_queue.get())
        deal_to_clock()            #处理区卡片进血
        return 0          #未取消
    else:
        return 1          #取消

def put_card_on_top(reshuffle_number): #向卡组顶放血
    global deck,drop, climax_drop,top_not_climax
    for i in range (0,reshuffle_number):
        if (drop-climax_drop)!=0:
            drop=drop-1
            top_not_climax=top_not_climax+1
            deck=deck+1
        else:
            break

def card_back_to_deck(reshuffle_number): #向卡组反洗肉
    global deck,drop, climax_drop
    # print(drop, deck)
    drop_not_climax=drop-climax_drop
    if drop_not_climax>=reshuffle_number:
        drop=drop-reshuffle_number
        deck=deck+reshuffle_number
        # print(drop,deck)
    else:
        drop=drop-reshuffle_number
        deck=deck+reshuffle_number
        # print(drop, deck)


def moka(moka_number):
    global deck, drop,climax_deck,climax_drop, top_not_climax
    effective_moka=moka_number-top_not_climax       #考虑做顶和摩卡同时存在的情况
    watched_climax=0
    tmp_climax_deck=climax_deck
    tmp_deck=deck-top_not_climax
    if effective_moka>0:
        if effective_moka>deck:
            effective_moka=deck

        for im in range(0,effective_moka):
            # print(tmp_climax_deck,tmp_deck)
            ratio = tmp_climax_deck / tmp_deck
            climax_or_not = random.random()
            if climax_or_not > ratio:  # 看到不是潮
                top_not_climax+=1
                tmp_deck=tmp_deck-1
            else:  # 看到是潮，推掉潮
                # print("潮！")
                watched_climax+=1
                tmp_deck=tmp_deck-1
                tmp_climax_deck=tmp_climax_deck-1
    if watched_climax!=0:
        deck=deck-watched_climax
        climax_deck=climax_deck-watched_climax
        drop=drop+watched_climax
        climax_drop=climax_drop+watched_climax
        if deck == 0:
            new_deck()

    # print(climax_deck,deck)
    # print(top_not_climax)




def damage_combo_spy():
    # damage_can_be_cancelled(1)
    # damage_can_be_cancelled(1)
    # moka(1)
    damage_can_be_cancelled(3)
    father1=damage_can_be_cancelled(3)
    if father1==1:
        damage_can_be_cancelled(1)
    damage_can_be_cancelled(4)
    father2=damage_can_be_cancelled(3)
    if father2==1:
        damage_can_be_cancelled(1)
    damage_can_be_cancelled(3)
###main
# 斩杀成功率计算

average_damage=0
s=0
for i in range (0,50000):
#参数设置
    deck=30
    climax_deck=6
    drop=0
    climax_drop=0
    level=2
    clock=4
    lifepoint_start = level * 7 + clock
    climax_clock=0
    # stock=0
    # hand=0
    # memory=0
    deal=0
    climax_deal=0
    top_not_climax=0
    # climax_stock=0
    # climax_level=0
    # climax_hand=0
    # climax_memory=0
    damage_combo_spy()


    # print("等级:",level,"时计区:",clock,"控室:",drop,"卡组:",deck,"卡组剩余高潮卡:",climax_deck)
    lifepoint_end = level * 7 + clock
    damage_created=lifepoint_end-lifepoint_start
    average_damage=average_damage+damage_created
    if lifepoint_end>=28:
        s+=1
print(s/50000,average_damage/50000)
