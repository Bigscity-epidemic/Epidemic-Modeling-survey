这里面文件的作用是，把一个Model类编译为类似SUEIR_base.py那样的函数文件，从而在后一步进行参数拟合

compiler为编译器

fit需要接收的参数为：model，需要进行欧氏距离的仓室及其真值。这一部分将以dict：compartment_name->list[real value]的形式给出。
fit返回一组拟合好的参数