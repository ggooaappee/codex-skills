# 顺序表参考实现（教材口径）

教材：李云清《数据结构（C 语言版）》第 4 版，人民邮电出版社。教师模板把教材的 `elem/length` 改成了 `a/n`，接口以模板为准。

## 数据类型

```c
#define N 100
typedef int ElemType;
typedef struct{
  ElemType a[N];     // 存放元素的数组
  int n;             // 当前表长
}SeqList;
```

## exp1.h：基本操作

```c
void init(SeqList *slt)
{
	slt->n = 0;
}

int empty(SeqList *slt)
{
	return (slt->n == 0) ? (1) : (0);
}

int full(SeqList *slt)
{
	return (slt->n == N) ? (1) : (0);
}

int find(SeqList *slt, ElemType x)
{
	int i = 0;
	while((i < slt->n) && (slt->a[i] != x))  i++;
	return (i < slt->n) ? (i) : (-1);
}

int get(SeqList *slt , int i, ElemType *e)
{
	if((i >= 0) && (i < slt->n))
	{   *e = slt->a[i];
		return 1;
	}
	return 0;
}

int insert(SeqList *slt, int i, ElemType x)
{
	int j;
	if((slt->n == N) || (i < 0) || (i > slt->n))  return 0;
	for(j = slt->n; j >= i + 1; j--)  slt->a[j] = slt->a[j - 1];
	slt->a[i] = x;
	++slt->n;
	return 1;
}

//测试程序按 del(&L,i,&e) 调用，故与教材 delete 一致，带回送参数
int del(SeqList *slt, int i, ElemType *e)
{
	int j;
	if((slt->n == 0) || (i < 0) || (i >= slt->n))  return 0;
	*e = slt->a[i];
	for(j = i; j < slt->n - 1; j++)  slt->a[j] = slt->a[j + 1];
	--slt->n;
	return 1;
}
```

模板原型 `int insert(SeqList *slt, int i, ElemType x,)` 末尾的逗号是语法错误，必须删掉。

## exp2.1.1 倒置存储（reverse）

```c
void reverse(SeqList *L)
{   int i=0, j=length(L)-1;
    ElemType tmpi, tmpj;
    while(i<j)
    {   get(L,i,&tmpi);
        get(L,j,&tmpj);
        replace(L,i,tmpj);
        replace(L,j,tmpi);
        i++; j--;
	}
}
```

时间 O(n)，空间 O(1)。输入 0…9，输出 9…0。

## exp2.1.2 按奇偶性拆分（sprit）

```c
void sprit(SeqList *L, SeqList *L1, SeqList *L2)
{   int i=0, len=length(L);
    int p1=0, p2=0;
    ElemType ei;
    while(i<len)
    {   ei = L->a[i];
        if(ei%2)
		{   insert(L1,p1,ei);  p1++;
		}
        else
		{   insert(L2,p2,ei);  p2++;
        }
        i++;
	}
}
```

时间 O(n)。输入 0…9，L1=1 3 5 7 9，L2=0 2 4 6 8，两表均保持原相对次序。

## exp2.1.3 奇偶分类存储（partition）

```c
void partition(SeqList *L)
{   int i=0, j=length(L)-1;
    ElemType ei, ej;
    while(i<j)
    {   while(i<j)
	    {   get(L,i,&ei);
		    if(ei%2) i++;      // 奇数继续后移
		    else break;        // 偶数停住
		}
	    while(i<j)
	    {   get(L,j,&ej);
		    if(ej%2==0) j--;
		    else break;
		}
        if(i<j)
		{   replace(L,i,ej);
		    replace(L,j,ei);
        }
        i++; j--;
	}
}
```

时间 O(n)，空间 O(1)；就地交换会打乱同类元素的相对次序，若需稳定分区要另开数组。

`if(ei%2) i++;` 后多写一个分号会让 `else` 失去配对，编译报 `'else' without a previous 'if'`。

测试数据 `11 20 23 4 55 6 7 82 9 10 3 5 28 40 41 87 24 30 45 60`
预期输出 `11 45 23 87 55 41 7 5 9 3 10 82 28 40 6 4 24 30 20 60`（前 10 奇、后 10 偶）。

## exp2.1.4 有序表归并（merge）

```c
void merge(SeqList *L, SeqList *L1, SeqList *L2)
{   int i=0, j=0, k=0;
    int len1=length(L1), len2=length(L2);
    ElemType ei, ej;
    while(i<len1&&j<len2)
    {   get(L1,i,&ei);
	    get(L2,j,&ej);
	    while(ei<=ej)
	    {   insert(L,k,ei);
		    i++; k++;
			if(!get(L1,i,&ei)) break;
		}
		while(ei>ej)
	    {   insert(L,k,ej);
		    j++; k++;
			if(!get(L2,j,&ej)) break;
		}
	}
	while(i<len1)
	{   get(L1,i,&ei);
	    insert(L,k,ei);
	    i++; k++;
	}
	while(j<len2)
	{   get(L2,j,&ej);
	    insert(L,k,ej);
	    j++; k++;
	}
}
```

时间 O(n1+n2)，空间 O(1)。1 3 5 7 9 与 2 4 6 8 10 归并为 1…10。

## exp1.c 的预期运行结果

```text
empty: 1

full: 1, L.n=100

0    1    2    ...    99    find 10: 10
find 101: -1
empty: 1
```

说明：循环插入 N+1=101 次，第 101 次因表满失败；find 10 返回下标 10，find 101 返回 -1；从表尾逐个删除后 empty 回到 1。

## 复杂度速查

| 操作 | 时间 | 说明 |
| --- | --- | --- |
| init / empty / full | O(1) | 只看表长 |
| get / replace | O(1) | 下标直接定位 |
| find | O(n) | 顺序比较 |
| insert | O(n) | 平均后移一半元素 |
| del | O(n) | 平均前移一半元素 |
| reverse / partition | O(n) | 双指针就地交换，空间 O(1) |
| sprit | O(n) | 另设两个表，空间 O(n) |
| merge | O(n1+n2) | 结果直接存 L，空间 O(1) |
