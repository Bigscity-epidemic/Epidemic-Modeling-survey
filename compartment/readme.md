这里包含3类文件和他们之间的转化工具
1. 用于构建仓室的顶层可视化表述
2. 用于构建舱室的graph，以节点表示仓室，以有向边表示转移路径
3. 表述这一仓室结构的实际类，这个类可以直接放入executor，配合参数文件进行预测

执行器将首先调用一个graph，随后调用descriptor里面的命令完成图的创建

graph会用到node建模。graph会维护一个dict，保存仓室名（node名）-> 仓室类。

graph创建好后，执行器将调用transfer里面的函数，根据graph建立model。
同时，Node改为Compartment，带有仓室值属性；
将边改为Path类，带有是否使用embedding的动态参数，静态参数值，四则运算表达式（表达式中包含自然数、四则运算符、括号、前述参数、仓室名称这5种字符）等属性。


