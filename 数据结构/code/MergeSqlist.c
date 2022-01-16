#include <stdio.h>
#include <stdlib.h>

/* 宏定义 */
#define LIST_INIT_SIZE  100
#define LISTINCREMENT   10

/* 状态码 */
#define TRUE        1
#define FALSE       0
#define OK          1
#define ERROR       0
#define INFEASIBLE  -1
#define OVERFLOW    -2

typedef int Status;

typedef int ElemType;

/* 结构描述 */
typedef struct
{
    ElemType *elem;     // 存储空间基地址
    int length;         // 当前长度
    int listsize;       // 分配长度
}SqList;

/* 初始化顺序表 */
Status InitList_Sq(SqList *L){
    // 构造一个空的顺序表L
    (*L).elem = (ElemType * )malloc(LIST_INIT_SIZE * sizeof(ElemType));
    if (!(*L).elem) exit(OVERFLOW);     // 存储失败
    (*L).length = 0;                    // 空表长度0
    (*L).listsize = LIST_INIT_SIZE;     // 初始化存储容量
    return OK;
}

/* 顺序表的合并 */
Status MergeList_Sq(SqList La, SqList Lb, SqList *Lc){
    // 已知顺序线性表La和Lb的元素按值非递减排列
    // 归并La和Lb得到新的顺序线性表Lc，Lc的元素按非递增排列
    int *pa = La.elem;
    int *pb = Lb.elem;
    (*Lc).listsize = (*Lc).length = La.length + Lb.length;
    (*Lc).elem = (ElemType * )malloc((*Lc).listsize * sizeof(ElemType));
    
    int *pc; pc = (*Lc).elem + (*Lc).length - 1;
    
    if (!(*Lc).elem) exit(OVERFLOW);    // 存储分配失败

    int *pa_last = La.elem + La.length - 1;
    int *pb_last = Lb.elem + Lb.length - 1;
    
    while (pa <= pa_last && pb <= pb_last){     // 归并
        if (*pa <= *pb) *pc-- = *pa++;
        else *pc-- = *pb++;
    } 
    while (pa <= pa_last) *pc-- = *pa++;        // 插入La的剩余元素
    while (pb <= pb_last) *pc-- = *pb++;        // 插入Lb的剩余元素
    
    return OK;
}   // MergeList_Sq

/* 打印顺序线性表 */
Status ShowList_Sq(SqList L){
    for (int i=0; i<L.length; ++i){
        printf("%d ",L.elem[i]);
    }
    return OK;
}

/* 判断顺序表格式是否正确 */ 
int JudgeList_Sq(SqList L){
    for (int i=1; i<L.length; ++i){
        if (L.elem[i] < L.elem[i-1]) {printf("输入错误.\n"); return ERROR;}
    }
    printf("No Problem!\n");
    return OK;
}

/* 实现顺序线性表的合并 */
int main()
{
    // 初始化三个顺序线性表
    SqList La, Lb, Lc;
    InitList_Sq(&La);
    InitList_Sq(&Lb);
    InitList_Sq(&Lc);

    // 输入La和Lb
    int n_a, n_b;		// n_a, n_b分别是表La与Lb的长度 
    int e_a, e_b;       // e_a, e_b分别是表La与Lb中的数据元素值
    printf("请输入La的长度:\n");
    scanf("%d",&n_a);
    printf("请按照从小到大顺序输入列表La:\n");
    for(int i=0; i<n_a; ++i){     // 数据元素填入表中
        scanf("%d",&e_a);
        La.elem[i] = e_a;
        ++La.length;
    }
    
    printf("请输入Lb的长度:\n");
    scanf("%d",&n_b);
    printf("请按照从小到大顺序输入列表Lb:\n");
    for(int i=0; i<n_b; ++i){     // 数据元素填入表中
        scanf("%d",&e_b);
        Lb.elem[i] = e_b;
        ++Lb.length;
    }

    // 判读线性顺序表是否是从小到大顺序
    printf("\n下面对输入顺序表格式检查.\n");
    JudgeList_Sq(La);
    JudgeList_Sq(Lb);
    printf("检查无误.\n");

    // 合并
    printf("\n现在对两个线性表进行合并.\n");
    MergeList_Sq(La, Lb, &Lc);
    printf("合并后顺序表如下:\n");
    ShowList_Sq(Lc);

	return 0;
}