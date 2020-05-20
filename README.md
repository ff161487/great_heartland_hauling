# 货运卡车

## 游戏简介
《货运卡车》(The Great Heartland Hauling Co.)是一款益智类的卡牌桌游，适合玩家数目2~4人进行游戏，十分适合在情侣之间或合租屋、同宿舍的室友之间进行。玩家将会操作自己的卡车，将不同种货物从其产地运送至相应的可出售对应货物的地点，从而赚取收益。先达到“临界金额”的玩家宣布游戏进入最后一轮，在本轮结束后进行结算，并判断哪位或哪几位玩家最终获得胜利。具体游戏规则请参考下面的“游戏规则”部分。

据悉，《货运卡车》的原作为

## 项目简介
本项目是作者在同室友玩过《货运卡车》后被成功安利入坑的。经过讨论，大家一致认为线下玩耍过程中，洗牌问题对结果影响甚大。如果弃牌堆洗牌不匀，会导致同类型卡牌在摸牌时集中出现，很大程度上影响了游戏体验，破坏了游戏平衡性。因此，我们萌生了将这款有趣的线下桌游搬到线上的想法。由此诞生了本项目。

另一方面，作者的室友在同步开发《货运卡车》的界面及跨平台客户端和服务器端的程序。然而，由于一些涉及人类的本质方面的原因，其项目进度惨不忍睹。因此，本项目原计划是实现《货运卡车》的逻辑内核，同时留下供所有爱好者开发AI的接口，以期能形成一个AI开发社群供大家进行AI之间的对战等等，现在也被迫加入了界面部分的开发。而由于作者能力所限，目前的界面部分仅由matplotlib绘图实现，但是已经可以做到人机交互，方便开发者通过和自己设计的AI进行对局来直观感受AI的强度。在此感谢Elliot Gao同学对界面的改进，同时FHC同学的建议也帮助改善了试玩游戏体验。关于未来进一步开发更加动态、直观地交互界面，作者的父亲也给予了作者十分宝贵的指导和建议，让作者深刻认识到自己能力之所限，不应该妄图设想以一己之力完成如此庞大的工程。后面会更加专注于AI开发方面。

说到AI开发，作者在项目中设计了接口支持广大开发者发挥自己的创造力进行AI策略开发。通过对场上公开信息的有效提炼以及对游戏每回合所允许的操作的理解，作者将《货运卡车》的AI/策略通用形式转化为了一个函数/方法，即输入可行操作集合与场上公开信息，返回本回合AI/策略所选择的操作。为了方便AI开发，作者还提供了能够“列出给定公开信息下，一个玩家理论上可执行的所有操作的集合”以及“给定某玩家所采取的操作和当前场上的公开信息，返回操作完成后新的公开信息”的函数。因此后续开发者可以不必花费时间纠结于游戏的具体机制以及行动逻辑，而直接进行AI开发。相关函数以及接口的具体介绍请参见[]()

前面提到，《货运卡车》支持2~4人游戏，而项目中给出的示例AI都是基于4人游戏的情形下开发的。作者鼓励大家开发不同类型、风格、强度以及适合不同人数的AI。在线下体验《货运卡车》的过程中，作者发现不同人数时的策略、行动的侧重点以及游戏节奏均有不同，可以相信通过AI/策略的开发，我们也可以看到这一点。一个很有趣的问题是：在线下进行时，有两类思路颇受玩家青睐。一类是“远离众人，闷头发育”；另一类则是“积极卡位，强势压制”。可以说这两类思路都有道理且都有效。那么究竟哪种思路更胜一筹？还是说应当因时制宜？或者有其它更绝妙的想法？这些问题的回答可能都需要等到一个“神”级的AI开发出来后，我们才能回答。



## 游戏规则

## 协议与免责声明
 
