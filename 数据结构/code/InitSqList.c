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

/* 销毁顺序表 */
Status DestoryList(SqList *L){
    // 判断顺序表已存在
    if ((*L).elem) free((*L).elem);
    (*L).elem = NULL;
    (*L).length = 0;
    (*L).listsize = 0;
    return OK;
}

/* 将顺序表重置为空表 */
Status ClearList(SqList *L){
    if ((*L).elem) (*L).length = 0; // 重置为空表
    return OK;
}

/* 判断顺序表是否为空 */
Status ListEmpty(SqList L){
    if (L.length == 0) return TRUE;
    else return FALSE;
}

/* 返回顺序表的长度 */
int ListLength(SqList L){
    if (L.elem) return L.length;
}

/* 返回顺序表中的值 */
Status GetElem(SqList L, int i, ElemType *e){
    printf("请输入你想得到第几个数据.\n");
    scanf("%d",&i);

    // 判断线性表存在并且i是否合理
    if ((L.elem) && i>= 1 && i <= L.length) (*e) = L.elem[i-1];
    else return FALSE;
    
    printf("顺序表中第%d个值为%d.\n", i, *e);
    return OK;
}

/* 判断顺序表中元素位序 */
Status LocateElem(SqList L, ElemType e, Status(*compare)(int, int)){
    // 返回第一个与e满足得关系compare()的数据元素的位序
    int i = 1;
    int *p = L.elem;
    while (i <= L.length && !(*compare)(*p++, e)) ++i;
    if(i <= L.length) return i;
    else return FALSE;
}

/* 查找顺序表中元素位序 */
Status SearchElem(SqList L, ElemType e){
    for (int i=0; i<L.length; ++i){
        if (L.elem[i] == e) {return i+1;}
    }
}

/* 顺序表中插入一个元素 */
Status ListInsert_Sq(SqList *L, int i, ElemType e){
    // 在顺序线性表L中第i个位置之前插入新的元素e
    // i的合法值为1<=i<=ListLength_Sq(L)+1
    if (i < 1 || i > ((*L).length+1)) return ERROR;     // i值不合法
    
    if ((*L).length >= (*L).listsize){      // 当存储空间已满，增加分配
        int *newbase = (ElemType * )realloc((*L).elem, ((*L).listsize + LISTINCREMENT) * sizeof(ElemType));
        if (!newbase) exit(OVERFLOW);       // 存储分配失败
        (*L).elem = newbase;                // 新基址
        (*L).listsize += LISTINCREMENT;     // 增加存储容量
    }

    int *q = &((*L).elem[i-1]);             // q为插入位置，q为地址
    for (int *p = &((*L).elem[(*L).length-1]); p >= q; --p) *(p + 1) = *p;
                                            // 插入位置及之后元素后移
    *q = e;             // 插入e
    ++(*L).length;      // 表长增加1
    return OK; 
}

/* 顺序表中删除一个元素 */
Status ListDelete_Sq(SqList *L, int i, ElemType *e){
    // 在顺序线性表L中删除第i个元素，并用e返回其值
    // i的合法值为1<=i<=ListLength_Sq(L)
    if ((i < 1) || (i > (*L).length)) return ERROR;     // i值不合法
    int *p = &((*L).elem[i-1]);                         // p为被删除元素的位置
    *e = *p;                                             // 被删除元素的值赋给e
    int *q = (*L).elem + (*L).length-1;                 // 表尾元素的位置
    for (++p; p <= q; ++p) *(p - 1) = *p;               // 被删除元素之后的元素左移
    --(*L).length;                                      // 表长减1
    printf("被删除的元素是%d.\n",*e);
    return OK;
}

int main()
{
    SqList L;       // 创建顺序线性表L

    // 判断初始化
    if (InitList_Sq(&L) == OK) 
        printf("顺序线性表初始化完成.\n");
    else 
        printf("初始化失败, 请重试.\n");

    // 输入列表的值
    int n, e;       // n为列表的长度
    printf("请输入你的顺序表的长度.\n");
    scanf("%d",&n);
    printf("你将得到一个长度为%d的顺序表.\n",n);
    printf("请输入%d个数据元素, 以空格间隔.\n",n);
    for(int i=0; i<n; ++i){     // 数据元素填入表中
        scanf("%d",&e);
        L.elem[i] = e;
        ++L.length;
    }

    // 打印列表
    printf("\n");
    printf("你的数组为:\n");
    for (int i=0; i<L.length; ++i){
        printf("%d ",L.elem[i]);
    }

    // 数组中插入值
    printf("\n");
    printf("插入操作如下:\n");
    int a, b;           // a为插入位置，b为值
    printf("请输入插入的位置:\n");
    scanf("%d",&a);
    printf("请输入插入的值:\n");
    scanf("%d",&b);
    
    ListInsert_Sq(&L, a, b);        // 插入实现

    printf("插入完成, 新的数组为:\n");
    for (int i=0; i<L.length; ++i){     // 打印新列表
        printf("%d ",L.elem[i]);
    }

    // 数组中删除值
    printf("\n");
    printf("删除操作如下:\n");
    int m, Retain;      // m为删除元素序号, Retain用来保留删除的值
    printf("请输入你要删除的数据元素的序号:\n");
    scanf("%d",&m);

    ListDelete_Sq(&L, m, &Retain);   // 删除实现

    printf("删除完成, 新的数组为:\n");
    for (int i=0; i<L.length; ++i){     // 打印新列表
        printf("%d ",L.elem[i]);
    }

    // 查找数组中的值
    printf("\n");
    printf("查找操作如下:\n");
    int c;          // c为想要查找的值
    printf("请输入想要查找的元素的值:\n");
    scanf("%d",&c);

    int d = SearchElem(L, c);

    printf("该值序号为%d.\n",d);

    // 清空列表
    printf("\n");
    printf("操作完成, 清空列表.\n");
    if (ClearList(&L) == OK)
        printf("列表已清空.\n");
    else 
        printf("列表清空失败.\n");
    printf("此时列表长度为%d.\n",L.length);     // 检验操作是否成功

    // 销毁列表
    printf("\n");
    printf("操作完成, 销毁列表.\n");
    if (DestoryList(&L) == OK)
        printf("列表已销毁.\n");
    else 
        printf("列表销毁失败.\n");
    
    system("pause");
    return 0;
}