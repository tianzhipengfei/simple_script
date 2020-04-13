---
layout:     post
title:      "Mastering the Game of Go without Human Knowledge 论文学习"
subtitle:   "机器的重生竟然是放弃人类"
date:       2020-04-13 00:00:00
author:     "Eric"
header-img: "img/alpha_go_zero_bg.jpg"
catalog: true
tags:
  - Inforcement Learning
  - Alpha Go
  - 论文笔记
---

# Mastering the Game of Go without Human Knowledge

[论文地址](https://www.nature.com/articles/nature24270.epdf)

众所周知，Alpha Go Zero是一个围棋的AI产品，经历了几次更新迭代之后，它是目前最强大的围棋AI，能力超过战胜了李世石的Alpha  Go Lee和战胜了柯洁的Alpha Go Master。最近要做一个桌游类的AI机器，所以读了这篇论文，今天我来记录一下这篇论文的总结。

# 1. 核心算法

Alpha Go Zero的核心思想是用MCTS去记录棋盘，同时统计出获胜的概率，用残差网络去学习这个概率分布，同时在MCTS中还用到了UCT算法(我看网上说真的用到UCT的很少，但是Alpha Go Zero用了)。

## 1.1 Monte Carlo Tree Search (MCTS)

MC是蒙特卡洛方法，是一种基于统计的模拟方法。例如在古代不知道圆周率的情况下，如何计算圆的面积，我们可以在一个正方形内画一个内切圆，经过多次的随机向正方形内扔石头，计算圆内的石子个数和正方形内的石子个数求得圆与正方形的面积比，从而计算出圆的面积。这种方法的步骤是，把原问题转化为概率问题，之后通过概率计算求得原问题的估计解。随着试验次数的不断增加，解的准确性也不断提升。

TS是树搜索，可以看做记录了不同状态及其先后次序的一棵树。通过树状结构，我们可以把一盘围棋的棋盘进行复盘，即从空棋盘状态->先手放第一个棋子后的状态1>后手放第一个棋子的状态2-> ... ->最终的棋盘状态。

## 1.2 Neural Networks (NN)

NN就是神经网络，比较流行的有Convolutional Neural Networks，Recurrent Neural Networks等，Alpha Go前期使用的是CNN，在后期逐渐使用[Residual Neural Network](https://arxiv.org/abs/1512.03385)(之后总结这个论文)，在这篇文章中也对两种网络结构的性能做了对比。

## 1.3 Upper Confidence Bound (UCB)算法

UCB算法是强化学习中的一个算法，在强化学习中，一般分为两个步骤，一个是Estimate(估计)，一个是Exploitation(实施)。为了方便理解，我们在这里统一举一个例子，假如我们是餐厅老板，来了一位顾客，我们要给他推荐菜品，应该如何推荐呢？估计就是基于历史推荐和顾客的喜欢与否，我们对每个菜品的欢迎程度进行估算，实施就是通过一定的规则，我们根据估算结果对顾客推荐一道菜。下面我从简单到难地介绍几种算法。

### 1.3.1 Greedy

贪心算法，最直观容易理解。我们只要记录之前每个客人点过的订单，统计出每个菜的欢迎程度(该菜被顾客喜欢的次数/该菜的被推荐次数)，之后我们选择最受欢迎的即可。当然，为了让每个菜在起初都有被点的可能，我们为没有被点的菜品赋一个较大值 
<img src="https://www.zhihu.com/equation?tex= Q_{0} " alt=" Q_{0} " class="ee_img tr_noresize" eeimg="1">
，使得优先推荐从未被点过的菜。


![](https://tva1.sinaimg.cn/large/007S8ZIlly1gdrgblwmpsj30hw09sdgv.jpg)

### 1.3.2 ε-Greedy

 ε-Greedy算法和Greedy算法类似，区别在于Exploitation阶段中，我们并不是一直都要使用估算得到的最受欢迎的菜品，我们要保留一定的概率ε用来进行新的探索，随机从所有菜品中选择一道推荐给顾客。
 
 这样的好处在于，可以探索到更多的顾客可能喜欢的菜品，但缺点是趋于稳定的时间变长。这个很好理解，因为要找到好吃的菜是需要很多人进行试吃试错的，如果探索过少，则很难找到好吃的菜。
 
 ![](https://tva1.sinaimg.cn/large/007S8ZIlly1gdrgimpupsj30im0aedh4.jpg)
 
### 1.3.3 UCB
 
在 ε-Greedy算法中，虽然我们有ε的概率进行探索，但是还是有一定的问题，例如两道菜，他们受欢迎的程度一致，例如菜A(2/4)，菜B(3/6)，如果我们现在要给顾客进行推荐，我们应该优先推荐哪一个呢？当然是A，因为我们希望有更多的顾客去试吃，从而得到更多的数据，进而得到更准确的欢迎程度。但是 ε-Greedy算法并没有解决这个问题。UCB算法便很好地解决了它，它充分利用了历史信息进行推荐。

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gdrgvx971vj30ii0abgn0.jpg)

上图中Q<sub>t-1</sub>(i)由两项组成，左边为之前说的受欢迎程度，右边则与该菜被推荐的频率有关，t表示推荐的总次数，N<sub>t-1</sub>(i)表示第i道菜被推荐的次数，显然菜A和菜B在受欢迎程度相同时，因为菜A只被推荐过四次，A的总分数大于B，所以优先被选择推荐。

那么为什么右边这项是这样一个式子呢？其实这就联系到了Upper Confidence Bound，统计得到的第i道菜受欢迎程度虽然和真实的受欢迎程度有误差，但这个误差是由上界的。根据Chernoff-Hoeffding Bound，假设样本的Reward是在[0, 1]区间的独立同分布随机变量，用 
<img src="https://www.zhihu.com/equation?tex= \bar p" alt=" \bar p" class="ee_img tr_noresize" eeimg="1">
 表示样本的均值，用p表示分布的均值，（这里
<img src="https://www.zhihu.com/equation?tex= \bar p" alt=" \bar p" class="ee_img tr_noresize" eeimg="1">
 表示菜根据历史信息得到的受欢迎结果，p表示这道菜真的受欢迎的结果）有不等式成立, 
<img src="https://www.zhihu.com/equation?tex= P\left \{ \left | \overline{p} - p \right | \leq \delta \right \} \geq 1 - 2e^{2n\delta ^{2}}" alt=" P\left \{ \left | \overline{p} - p \right | \leq \delta \right \} \geq 1 - 2e^{2n\delta ^{2}}" class="ee_img tr_noresize" eeimg="1">
,当 
<img src="https://www.zhihu.com/equation?tex= \delta = \sqrt{\frac{2 ln(t)}{n}} " alt=" \delta = \sqrt{\frac{2 ln(t)}{n}} " class="ee_img tr_noresize" eeimg="1">
时，
<img src="https://www.zhihu.com/equation?tex= \overline{p} - \sqrt{\frac{2  ln(t)}{n}}\leq p\leq \overline{p} + \sqrt{\frac{2  ln(t)}{n}} " alt=" \overline{p} - \sqrt{\frac{2  ln(t)}{n}}\leq p\leq \overline{p} + \sqrt{\frac{2  ln(t)}{n}} " class="ee_img tr_noresize" eeimg="1">
是以 
<img src="https://www.zhihu.com/equation?tex= 1 - \frac{2}{t^{4}} " alt=" 1 - \frac{2}{t^{4}} " class="ee_img tr_noresize" eeimg="1">
的概率成立的。

# 2. 论文内容

# 2.1 Summary

人工智能的一个长期目标就是在一个具有挑战的领域拥有超越人类的实力，最近，Alpha Go成为了第一个击败围棋世界冠军的程序。Alpha Go的Tree Search在下棋中会评估每一个状态，并通过神经网络进行下一步的指导。之前的Alpha Go神经网络是通过人类专家数据和自我对弈数据训练得到的。这篇文章里，我们提出了一种新的算法，它仅仅依赖于自我对弈的数据，而不需要人类专家数据、指导或者除了围棋规则外的其他专业领域知识。Alpha Go可以通过不断地自我对弈，指导自己下棋。这个神经网络模型增强了Tree Search的能力，并拥有了更厉害的下棋水平。Alpha Go Zero成功实现了超越人类的水平，以100:0的战绩赢了之前打败了众多世界冠军的前任Alpha Go模型。

# 2.2 Methods

两大部分，一部分是深度神经网络 
<img src="https://www.zhihu.com/equation?tex=f_{θ}" alt="f_{θ}" class="ee_img tr_noresize" eeimg="1">
，另一部分是蒙特卡洛树搜索MCTS。



## 2.2.1 Deep Neural Network

神经网络是整个项目最终要训练的一个模型，它的作用是，每当我把当前棋盘的一些状态信息输入后，它可以输出下一步选择在哪里下棋。输入的信息s包括棋盘的状态和下这步及前七步历史状态信息(raw board representation of the position and its history)，是一个19\*19\*17的一个矩阵 [link](https://ai.stackexchange.com/questions/11933/alphago-neural-network-inputs)，19\*19是棋盘的大小，17包括8个黑方8个白方的棋盘历史信息，和1个下一步是黑方下还是白方下。网络输出的是两个值(p, v)，p表示的是下一步在每一个可能位置落子的概率，v表示当前选手在当前局面下获胜的概率。网络结构是基于ResNet，包含许多residual block的卷积层，同时还有批量归一化和非线性整流器模块。

## 2.2.2 MCTS

MCTS的作用是记录棋盘的状态，和不同状态间的关系。为什么要这么做呢？之前已经说过了MCTS是把一个原问题转化为概率问题，在这里，下每一步棋容易获胜与否就是原问题，作为人类，我们在下每一步棋子的时候都是希望自己选择胜率较高的位置下棋，但是Alpha Go zero无法直接通过计算得到每一个位置的获胜率较高还是较低，就把原问题转换为概率问题，通过历史统计信息，可以得到经过该位置的棋盘情况最终赢了多少把，输了多少把来获得这个概率。

相对于神经网络，MCTS也会在每一个局面下输出两个值，π和z，π就是与NN的p对应的接下来在每一个可能位置落子的概率，z与v相对应，表示当前选手在当前局面下获胜的概率。由于无法直接通过数学公式计算π和z，这里用MCTS通过统计数据计算得到它们，并让神经网落去学习，当训练数据足够足够多的时候，π和p的分布就足够接近，z和v也足够接近，这点在损失函数中也可以看出来，MSE和CE加一个正则项。

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds57tuqnxj30o703raab.jpg)


![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds3he6jzsj30pl0pv43a.jpg)


MCTS其实很简单，当MCTS全部建立起来后，机器便可以通过遍历MCTS得到下一步怎么下，因为MCTS对每一步的信息都进行了统计，这些信息包括一个先验概率P(s, a)，一个被访问次数N(s,a)，和一个action-value Q(s,a)，P与当前的棋盘状态和选择下一步有关；N是统计在s局面下，选择a这个位置的次数，和之前推荐顾客某个菜品的次数类似；Q是选择这个位置最终导致胜利了多少次，类似于之前推荐给顾客后，顾客最终喜欢了多少次。MCTS每次都使用UCB算法进行选择，从所有可选的位置中，选择Q+U最高的位置下，Q其实就是统计了经过S,a这个状态和move最终导致的胜率是多少，
<img src="https://www.zhihu.com/equation?tex= {s}' " alt=" {s}' " class="ee_img tr_noresize" eeimg="1">
 是指最终的一个状态 
<img src="https://www.zhihu.com/equation?tex= V({s}')" alt=" V({s}')" class="ee_img tr_noresize" eeimg="1">
 取得胜利的指示函数，而U就是计算的统计概率和真实概率的误差上界，是上述UCB中的加号右边那项。

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds4jxgpqwj30ox0g2tcy.jpg)

但是如何从一个根节点建立起整个MCTS，并将MCTS的信息交给NN去更新呢。具体训练细节如下：

a. Select: 每次模拟从当前棋面对应的根节点s开始，不断迭代的选择Q(s,a)+U(s,a)最大的动作a进行搜索，一直搜索到遇到叶子节点或棋盘结束。

b. Expand and Evaluate: 当MCTS遇到叶子节点时，说明之前探索到这里就再也没有继续去考虑在当前状况下该往哪里下棋了，那么没有历史数据MCTS如何扩展这个叶子节点呢，NN就提供了帮助，把当前的s输入至NN，NN便可以得到一个p和v，通过NN指导MCTS不断延伸。

c. Backup: 当一盘棋结束后，就要对整盘棋经历过的所有move进行更新。还记得么，每个move存储了这一步move导致最终获胜的胜率是多少，所以当棋盘结束后要对其进行更新。

d. play: 当多次模拟过程后，便可以通过概率得到π，
<img src="https://www.zhihu.com/equation?tex= \pi_{a} \propto N(s, a)^{1/\pi } " alt=" \pi_{a} \propto N(s, a)^{1/\pi } " class="ee_img tr_noresize" eeimg="1">
, τ 是温度参数（temperature parameter），它可以控制π的分布更均匀还是更陡峭，通过调节它可以让NN更好的进行学习。

经过多次的模拟对弈后，便得到了众多的训练数据(s, π, z)，之后更新NN即可。通过不断地迭代，不断地训练，NN输出的结果与统计的结果越来越相似，最终导致通过自我博弈，获得了高超的围棋水平。

# 3. Experiment

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds5lnnbk5j30q10jf0xx.jpg)

上图展示了三个数据，第一个是Elo，是一个评价选手水平的指标，王者荣耀也用这个进行玩家匹配；第二个是与人类专家下棋的相似程度，第三个是损失函数。综合来看，Alpha Go Zero的水平高于了使用人类数据训练的监督学习模型的水平，同时它下棋的方法与人类专家也没有那么相似，可是它的损失函数缺更低，说明它预测输赢的水平更强。

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds5r272u8j30nx0jm77g.jpg)

同时Alpha Go团队也对神经网络架构的改变与训练算法的改进对最终结果的影响进行了试验，架构包括把policy和value网络合并还是分离，训练算法包括使用conv还是res，两两组合控制变量得到了上图的结果。可以发现，无论是哪种改进都对最终的结果有较大的影响。结果表明，使用残差网络会更加准确，error会更低，它提高了Alpha GO的Elo水平超过600分；同时，将policy和value合并的架构稍稍降低了预测的准确性，但是它降低了error，并也提高了约600分Elo，研究人员分析这一提升，是因为dual-res提升了计算效率，但更重要的是因为优化目标能够使得网络更加规范化，能够学习到一个共同的表示来支持多种场景。

![](https://tva1.sinaimg.cn/large/007S8ZIlly1gds61bgfl3j30qh0k9td0.jpg)

最后，Alpha Go团队拿Zero用了40个residual block持续训练了约40天，最终效果见上图，简单来说就是牛逼吧。

# 4. Conclusion

其实读的时候有一句话还是蛮震撼的，"AlphaGo Zero may be learning a strategy that is qualitatively different to human play"，这是否说明了人类这么长时间的对围棋的研究可能从方向上是有一定偏差的，这样的结果令人震撼也令人担心，希望人类少走一些弯路，希望AI也能更好地指导人类学习。

----

#### 参考链接

* http://xtf615.com/2018/02/12/AlphaGo-Zero/
* https://zhuanlan.zhihu.com/p/32952677
