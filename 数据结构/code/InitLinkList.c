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

/* 结点结构描述 */
typedef struct LNode{   // 结点类型
    ElemType        data;
    struct LNode    *next;
} LNode, *LinkList;

/* 释放结点 */
void FreeNode(LNode *p){
    free(p);
}

/* 初始化链表 */
Status InitList_L(LinkList *L){
    // 构造一个空的链表L
    (*L) = (LinkList)malloc(sizeof(LNode));
    if (!(*L)) exit(OVERFLOW);
    (*L)->next = NULL;      // 链表头指针为NULL
    return OK;
}

/* 销毁链表 */
Status DestroyList_L(LinkList *L){
    if (L == NULL) return OK;

    LinkList p = (*L)->next;
    while (p){
        p = (*L)->next;
        free(L);
        *L = p; 
    }
    return OK;
}

/* 清空链表 */
Status ClearList_L(LinkList *L){
    LinkList p, q;
    p = (*L)->next;
    while(p){
        q = p->next;
        free(p);
        p = q;
    }
    (*L)->next = NULL;
    return OK;
}

/* 判断链表是否为空 */
Status ListEmpty_L(LinkList L){
    if (L->next == NULL) return TRUE;
    else return FALSE;
}

/* 判断值是否在链表中 */
Status GetElem_L(LinkList L, int i){
    // L为带头结点的单链表的头指针
    // 当第i个元素存在时，其值赋给e并返回OK，否则返回ERROR
    LinkList p = L->next;               // 初始化，p指向第一个结点
    int j = 1;                          // j为计数器
    while (p && j < i){                 // 顺指针向后查找，直到p指向第i个元素或p为空
        p = p->next; ++j;
    }
    if (!p || j > i) return ERROR;      // 第i个元素不存在
    return p->data;                       // 取第i个元素
}

/* 返回链表的长度 */
int ListLength_L(LinkList L){
    LinkList p;
    int Length = 0;
    p = L->next;
    while (p){
        ++Length;
        p = p->next;
    }
    return Length;
}

/* 插入操作 */
Status ListInsert_L(LinkList *L, int i, ElemType e){
    // 在带头结点的单链线性表L中第i个位置之前插入元素e
    LinkList p = *L;
    int j = 0;
    while(p && j < i - 1) {p = p->next; ++j;}           // 寻找第i-1个结点
    if (!p || j > i - 1) return ERROR;                  // i小于1或者大于表长加1
    LinkList s = (LinkList) malloc (sizeof(LNode));     // 生成新结点
    s->data = e; s->next = p->next;                     // 插入L中
    p->next = s;
    return OK;
}

/* 删除操作 */
Status ListDelete_L(LinkList *L, int i, ElemType *e){
    // 在带头结点的单链线性表L中，删除第i个元素，并由e返回其值
    LinkList p = *L;
    int j = 0;
    while (p->next && j < i - 1) {      // 寻找第i个结点，并令p指向其前驱
        p = p->next; ++j;
    }
    if (!(p->next) || j > i - 1) return ERROR;          // 删除位置不合理
    LinkList q = p->next; p->next = q->next;            // 删除并释放结点
    *e = q->data; free(q);
    return OK;
}

/* 建立单链线性表 */
void CreatList_L(LinkList *L, int n){
    // 逆位序输入n个元素的值，建立带头结点的单链线性表L
    (*L) = (LinkList) malloc (sizeof(LNode));
    (*L)->next = NULL;      // 先建立一个带头结点的单链表
    for (int i = n; i > 0; --i){
        LinkList p = (LinkList) malloc (sizeof(LNode));     // 生成新结点
        scanf("%d", &p->data);                              // 输入元素值
        p->next = (*L)->next; (*L)->next = p;               // 插入到表头
    }
}

/* 打印单链线性列表 */
Status ShowList_L(LinkList L){
    LinkList p = L;
    while (p->next){
        p = p->next;
		printf("%d ",p->data);
    }
    return OK;
}

int main()
{
    LinkList L;         // 创建单链线性表L

    // 初始化单链线性表
    if (InitList_L(&L) == OK) 
        printf("单链线性表初始化完成.\n");
    else 
        printf("单链线性表初始化失败.\n");
    
    // 输入列表的值
    int n, e;           // n为列表的长度
    printf("请输入你想要创建的单链线性表的长度:\n");
    scanf("%d",&n);
    printf("你将要得到一个长度为%d的单链线性表.\n",n);
    printf("请逆序输入你的数据元素.\n");
    CreatList_L(&L, n);

    // 打印列表
    printf("\n");
    printf("你的单链线性表为:\n");
    ShowList_L(L);

    // 单链线性表中插入值
    printf("\n");
    printf("插入操作如下:\n");
    int a, b;           // a为插入位置，b为值
    printf("请输入你想要插入的位置:\n");
    scanf("%d",&a);
    printf("请输入你想要插入的值:\n");
    scanf("%d",&b);
    
    ListInsert_L(&L, a, b);     // 插入实现

    printf("插入完成, 新的单链线性表为:\n");
    ShowList_L(L);

    // 单链线性表中删除值
    printf("\n");
    printf("删除操作如下:\n");
    int m, Retain;      // m为删除元素序号, Retain用来保留删除的值
    printf("请输入你要删除的数据元素的序号:\n");
    scanf("%d",&m);

    ListDelete_L(&L, m, &Retain);   // 删除实现

    printf("删除完成, 新的数组为:\n");
    ShowList_L(L);

    // 查找操作实现
    printf("\n");
    printf("查找操作如下:\n");
    int c, z;
    printf("请输入你想要查找的索引号:\n");
    scanf("%d",&c);
    if (c > ListLength_L(L)) printf("索引失败, 超过单链线性表长度.\n");
    else z = GetElem_L(L, c);
    printf("查找得到该索引号对应的数据元素值为%d",z);

    // 清空列表
    printf("\n");
    printf("操作完成, 清空列表.\n");
    if (ClearList_L(&L) == OK)
        printf("列表已清空.\n");
    else 
        printf("列表清空失败.\n");
    printf("此时列表长度为%d.\n",ListLength_L(L));     // 检验操作是否成功
    
    // 销毁列表
	printf("\n");
	printf("操作完成, 销毁列表.\n");
	if (DestroyList_L(&L) == OK)
		 printf("列表已销毁.\n");
    else 
        printf("列表销毁失败.\n");
    
    return 0;
}