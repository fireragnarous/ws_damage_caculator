from queue import Queue
import random



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

def damage_can_be_cancelled(damage_number):
    global deck,climax_deck,deal,climax_deal,queue_deal,drop,climax_drop
    tmp_queue=Queue()
    whether_cancelled=0        #0代表未取消，1代表轻松取消
    for i in range (0,damage_number):
        ratio=climax_deck/deck
        # print(deck,climax_deck,ratio)
        climax_or_not=random.random()
        # print(climax_or_not)
        if climax_or_not>ratio:   #判定翻出来的是否是潮，随机数大于潮的浓度时认为翻出来的是血
            tmp_queue.put(0)
            deck=deck-1
            if deck==0:
                new_deck()
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
###main
# 斩杀成功率计算
s=0
for i in range (0,10000):
#参数设置
    deck=16
    climax_deck=4
    drop=12
    climax_drop=3
    level=2
    clock=2
    climax_clock=0
    # stock=0
    # hand=0
    # memory=0
    deal=0
    climax_deal=0

    # climax_stock=0

    # climax_level=0
    # climax_hand=0
    # climax_memory=0

    lifepoint = level * 7 + clock
    #以下逐行输入造成的伤害
    #两路零龙加一路平A打4
    damage_can_be_cancelled(4)
    card_back_to_deck(3)
    damage_can_be_cancelled(4)
    damage_can_be_cancelled(4)

    damage_can_be_cancelled(4)
    card_back_to_deck(3)
    damage_can_be_cancelled(4)
    damage_can_be_cancelled(4)

    damage_can_be_cancelled(4)
    print("等级:",level,"时计区:",clock,"控室:",drop,"卡组:",deck,"卡组剩余高潮卡:",climax_deck)
    lifepoint = level * 7 + clock
    if lifepoint>=28:
        s+=1
print(s)
