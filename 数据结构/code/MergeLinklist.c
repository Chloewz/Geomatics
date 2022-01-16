#include <stdio.h>
#include <stdlib.h>

/* 宏定义 */
#define LIST_INIT_SIZE 100
#define LISTINCREMENT 10

/* 状态码 */
#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
#define OVERFLOW -2

typedef int Status;

typedef int ElemType;

/* 结点结构描述 */
typedef struct LNode {  // 结点类型
    ElemType data;
    struct LNode *next;
} LNode, *LinkList;

/* 初始化链表 */
Status InitList_L(LinkList *L) {
    // 构造一个空的链表L
    (*L) = (LinkList) malloc(sizeof(LNode));
    if (!(*L))
        exit(OVERFLOW);
    (*L)->next = NULL;  // 链表头指针为NULL
    return OK;
}

/* 建立单链线性表 */
void CreatList_L(LinkList *L, int n) {
    // 逆位序输入n个元素的值，建立带头结点的单链线性表L
    (*L) = (LinkList) malloc(sizeof(LNode));
    (*L)->next = NULL;  // 先建立一个带头结点的单链表
    for (int i = n; i > 0; --i) {
        LinkList p = (LinkList) malloc(sizeof(LNode));  // 生成新结点
        scanf("%d", &p->data);                         // 输入元素值
        p->next = (*L)->next;
        (*L)->next = p;  // 插入到表头
    }
}

/* 合并两个单链线性表 */
void MergeList_L(LinkList *La, LinkList *Lb, LinkList *Lc) {
    // 已知单链线性表La和Lb的元素按值非递减排列
    // 归并La和Lb得到新的单链线性表Lc, Lc的值按非递增排列
    LinkList pa = (*La)->next;
    LinkList pb = (*Lb)->next;

    while (pa && pb) {
        LinkList p = (LinkList) malloc(sizeof(LNode));  // 生成新结点
        if (pa->data <= pb->data) {
            p->data = pa->data; pa = pa->next;
        } else {
            p->data = pb->data; pb = pb->next;
        }
        p->next = (*Lc)->next; (*Lc)->next = p;
    }

    // 插入剩余段
    while (pa) {
        LinkList p = (LinkList) malloc(sizeof(LNode));  // 生成新结点
        p->data = pa->data; pa = pa->next;
        p->next = (*Lc)->next; (*Lc)->next = p;
    }
    while(pb){
        LinkList p = (LinkList) malloc(sizeof(LNode));  // 生成新结点
        p->data = pb->data; pb = pb->next;
        p->next = (*Lc)->next;(*Lc)->next = p;
    }
}

/* 打印单链线性列表 */
Status ShowList_L(LinkList L) {
    LinkList p = L;
    while (p->next) {
        p = p->next;
        printf("%d ", p->data);
    }
    free(p);
    return OK;
}

/* 判断单链线性表格式是否正确 */
Status JudgeList_L(LinkList L) {
    LinkList p = L->next;
    while (p->next) {
        if (p->data > p->next->data) {
            printf("输入错误.\n");
            return ERROR;
        } else p = p->next;
    }
    printf("No Problem!\n");
    return OK;
}

int main() {
    // 初始化三个单链线性表
    LinkList La, Lb, Lc;
    InitList_L(&La);
    InitList_L(&Lb);
    InitList_L(&Lc);

    // 输入La和Lb
    int n_a, n_b;  // n_a, n_b分别是表La与Lb的长度
    int e_a, e_b;  // e_a, e_b分别是表La与Lb中的数据元素值
    printf("请输入La的长度:\n");
    scanf("%d", &n_a);
    printf("请从逆序输入La:\n");
    CreatList_L(&La, n_a);

    printf("请输入Lb的长度:\n");
    scanf("%d", &n_b);
    printf("请逆序输入Lb:\n");
    CreatList_L(&Lb, n_b);

    // 判断La和Lb格式是否正确, 即数据元素是否按照由小到大排序
    printf("\n现在对输入单链线性表格式进行检查\n");
    JudgeList_L(La);
    JudgeList_L(Lb);
    printf("检查无误.\n");

    // 合并操作实现
    printf("\n现在对两个单链线性表合并:\n");
    MergeList_L(&La, &Lb, &Lc);
    ShowList_L(Lc);

    system("pause");
    return 0;
}