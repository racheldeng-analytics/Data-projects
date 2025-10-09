#include<iostream>
#include<iomanip>
#include "stdlib.h"
#include<string>
using namespace std;

bool isID(string&);
typedef struct cnode
{
    char name[20];
    string ID;
    double consume;
    double integer;
    struct cnode* next;
}cnode;

void Initstack(cnode*& head)/*初始化链表*/
{
    head = new cnode();  //开辟节点空间
    head->next = NULL;
}

void Getelem(cnode* head);
void Search(cnode* head, string& ID);
void Amend(cnode* head, string& ID);
void Delete(cnode* head, string& ID);
void Showall(cnode* head);
void count(cnode* head);
double display_discount(double integer);

int main()
{
    cnode* head;
    int choice;
    string y;
    Initstack(head);
    do
    {
        cout << endl;
        cout << "       客户消费 积分管理系统    " << endl;
        cout << "  ******************************" << endl;
        cout << "  *                            *" << endl;
        cout << "  *          主菜单            *" << endl;
        cout << "  *       1  添加客户          *" << endl;
        cout << "  *       2  查找客户          *" << endl;
        cout << "  *       3  修改客户          *" << endl;
        cout << "  *       4  删除客户          *" << endl;
        cout << "  *       5  显示客户          *" << endl;
        cout << "  *       6  统计客户          *" << endl;
        cout << "  *       7  退出              *" << endl;
        cout << "  *                            *" << endl;
        cout << "  ******************************" << endl;
        cout << "请输入您的选择(1，2，3，4，5，6):";
        cin >> choice;
        if (choice == 1)
            Getelem(head);                                //添加
        else if (choice == 2)
        {
            cout << "请输入您查找客户的身份证号:";
            cin >> y;
            isID(y);
            Search(head, y);                           //查找
        }
        else if (choice == 3)
        {
            cout << "请输入您想修改客户的身份证号:";
            cin >> y;
            isID(y);
            Amend(head, y);
        }                             //修改
        else if (choice == 4)
        {
            cout << "请输入你想要删除的客户的身份证号：";
            cin >> y;
            isID(y);
            Delete(head, y);
        }                          //删除
        else if (choice == 5)
            Showall(head);                            //显示
        else if (choice == 6)
            count(head);             //统计
        else if (choice == 7)
            exit(1);
    } while (choice <= 7);
    system("pause");
    return 0;
}
void Getelem(cnode* head)
{
    //添加客户函数以头节点为参数
    cnode* p;
    double y;
    p = new cnode;
    p->next = new cnode;/*申请空的节点空间*/
    p->ID = " ";
    cout << "请输入姓名：";
    cin >> p->name;
    cout << "请输入身份证号(18位)：";
    cin >> p->ID;
    isID(p->ID);
    cout << "请输入消费金额：";
    cin >> p->consume;
    p->integer = p->consume / 100;
    cout << "积分：" << p->integer << endl;
    y = display_discount(p->integer);                      //调用函数计算折扣
    cout << "折扣:"/*<<setprecision(1)*/ << y << "折" << endl;
    p->next = head->next;
    head->next = p;
}
void Search(cnode* head, string& ID)
{
    cnode* p = new cnode;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "没有客户!" << endl;
    else
    {
        while (p->next != NULL)
        {
            p = p->next;
            if (ID == p->ID)          //判断身份证号是否相同
            {
                cout << "姓名：" << p->name << endl;
                cout << "身份证号：" << p->ID << endl;
                cout << "消费：" <</*setprecision(2)<<*/p->consume << endl;
                cout << "积分:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "折扣" <</*setprecision(1)<<*/y << "折" << endl;
                return;
            }
        }
        cout << "不存在该客户！" << endl;
    }
}

void Amend(cnode* head, string& ID) {
    cnode* p;
    double y, z;
    int choose, x;
    p = head;
    if (p->next == NULL)
        cout << "没有客户!" << endl;
    else
    {
        while (p->next != NULL)
        {
            p = p->next;
            if (ID == p->ID)     //判断身份证号是否相同
            {
                cout << "姓名：" << p->name << endl;
                cout << "身份证号：" << p->ID << endl;
                cout << "消费："/*<<setprecision(2)*/ << p->consume << endl;
                cout << "积分:" <</*setprecision(1)<<*/p->integer << endl;
                y = display_discount(p->integer);
                cout << "折扣:" <</*setprecision(1)<<*/y << "折" << endl;
                cout << "请选择你要修改的1、姓名。2、身份证号。3、消费金额。";
                cin >> choose;
                if (choose == 1)
                {
                    cout << "请输入修改后姓名;";
                    cin >> p->name;
                }
                if (choose == 2)
                {
                    cout << "请输入修改后的身份证号:";
                    cin >> p->ID;
                    isID(p->ID);
                }
                if (choose == 3)
                {
                    cout << "1.覆盖以前消费、2.续加上现在费用!请选择:";
                    cin >> x;
                    if (x == 1)
                    {
                        cout << "请输入修改后的消费:";
                        cin >> p->consume;
                    }
                    else {
                        printf("请输入续加金额:");
                        cin >> z;
                        p->consume += z;
                    }
                }
                cout << "姓名：" << p->name << endl;
                cout << "身份证号：" << p->ID << endl;
                cout << "消费：" <<p->consume << endl;
                p->integer = p->consume / 100.0;
                cout << "积分:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "折扣:" << y << "折" << endl;
                return;
            }
        }
        cout << "不存在该客户！" << endl;
    }
}
void Delete(cnode* head, string& ID)
{
    //删除客户函数
    cnode* p;
    int x;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "没有客户!" << endl;
    else
    {
        while (p->next != NULL)
        {
            head = p;
            p = p->next;
            if (ID == p->ID)
            {                 //判断身份证号是否相同
                cout << "姓名：" << p->name << endl;
                cout << "身份证号：" << p->ID << endl;
                cout << "消费："<< p->consume << endl;
                cout << "积分:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "折扣:" <<y << "折" << endl;
                cout << "你确认删除？1、确定。2、取消。请选择:";
                cin >> x;
                if (x == 1)
                {
                    head->next = p->next;
                    cout << ("删除成功!");
                }
                else
                    cout << "删除失败!";
                return;
            }
        }
        cout << "不存在该客户！" << endl;
    }
}
void Showall(cnode* head) //显示所有客户函数
{
    cnode* p;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "没有客户!" << endl;
    else
        while (p->next != NULL)
        {
            p = p->next;
            cout << "姓名：" << p->name << endl;
            cout << "身份证号：" << p->ID << endl;
            cout << "消费：" <<p->consume << endl;
            cout << "积分：" << p->integer << endl;
            y = display_discount(p->integer);
            cout << "折扣：" <<y << "折" << endl;
        }
}

void count(cnode* head)
{
    cnode* p;
    int i = 0;
    p = head;
    if (p->next == NULL)
        cout << "没有客户!" << endl;
    else
        while (p->next != NULL)
        {
            p = p->next;
            i++;
        }
    cout << "现有客户数量为" << i << "位!" << endl;
}
double display_discount(double points)
{
    //计算客户折扣函数，接受一个double型的数作为参数，输出对应的折扣
    double discount;
    if (points == 0)
        discount = 0;
    if (points > 0 && points <= 50)
        discount = 9.8;
    if (points > 50 && points <= 100)
        discount = 9.5;
    if (points > 100 && points <= 150)
        discount = 9.2;
    if (points > 150 && points <= 200)
        discount = 9;
    if (points > 200 && points <= 300)
        discount = 8;
    else if (points > 300)
        discount = 7;
    return discount;
}

int cal(string a)
{
    return (a[0] - '0') * 7 + (a[1] - '0') * 9 + (a[2] - '0') * 10 + (a[3] - '0') * 5 + (a[4] - '0') * 8 +
        (a[5] - '0') * 4 + (a[6] - '0') * 2 + (a[7] - '0') * 1 + (a[8] - '0') * 6 + (a[9] - '0') * 3 +
        (a[10] - '0') * 7 + (a[11] - '0') * 9 + (a[12] - '0') * 10 + (a[13] - '0') * 5 + (a[14] - '0') * 8 +
        (a[15] - '0') * 4 + (a[16] - '0') * 2;
}

char s(string a)
{
    int k = cal(a) % 11;
    if (k == 0)
        return '1';
    else if (k == 1)
        return '0';
    else if (k == 2)
        return 'X';
    else
        return '0' + 12 - k;
}

bool isNumber(string str);
bool isID(string& number)
{
    do
    {
        if (18 == number.length() && isNumber(number))
            if (number[17] == s(number))
                return true;
            else
                return false;
        else
            cout << "输入格式不正确,请重新输入：" << endl;
    } while (cin >> number);

}

bool isNumber(string str)
{
    for (int i = 0; i < str.length() - 1; i++)
        if (!isdigit(str[i]))
            return false;
    if ((isdigit(str[str.length() - 1])) || str[str.length() - 1] == 'X')
        return true;
    else
        return false;
}