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

void Initstack(cnode*& head)/*��ʼ������*/
{
    head = new cnode();  //���ٽڵ�ռ�
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
        cout << "       �ͻ����� ���ֹ���ϵͳ    " << endl;
        cout << "  ******************************" << endl;
        cout << "  *                            *" << endl;
        cout << "  *          ���˵�            *" << endl;
        cout << "  *       1  ��ӿͻ�          *" << endl;
        cout << "  *       2  ���ҿͻ�          *" << endl;
        cout << "  *       3  �޸Ŀͻ�          *" << endl;
        cout << "  *       4  ɾ���ͻ�          *" << endl;
        cout << "  *       5  ��ʾ�ͻ�          *" << endl;
        cout << "  *       6  ͳ�ƿͻ�          *" << endl;
        cout << "  *       7  �˳�              *" << endl;
        cout << "  *                            *" << endl;
        cout << "  ******************************" << endl;
        cout << "����������ѡ��(1��2��3��4��5��6):";
        cin >> choice;
        if (choice == 1)
            Getelem(head);                                //���
        else if (choice == 2)
        {
            cout << "�����������ҿͻ������֤��:";
            cin >> y;
            isID(y);
            Search(head, y);                           //����
        }
        else if (choice == 3)
        {
            cout << "�����������޸Ŀͻ������֤��:";
            cin >> y;
            isID(y);
            Amend(head, y);
        }                             //�޸�
        else if (choice == 4)
        {
            cout << "����������Ҫɾ���Ŀͻ������֤�ţ�";
            cin >> y;
            isID(y);
            Delete(head, y);
        }                          //ɾ��
        else if (choice == 5)
            Showall(head);                            //��ʾ
        else if (choice == 6)
            count(head);             //ͳ��
        else if (choice == 7)
            exit(1);
    } while (choice <= 7);
    system("pause");
    return 0;
}
void Getelem(cnode* head)
{
    //��ӿͻ�������ͷ�ڵ�Ϊ����
    cnode* p;
    double y;
    p = new cnode;
    p->next = new cnode;/*����յĽڵ�ռ�*/
    p->ID = " ";
    cout << "������������";
    cin >> p->name;
    cout << "���������֤��(18λ)��";
    cin >> p->ID;
    isID(p->ID);
    cout << "���������ѽ�";
    cin >> p->consume;
    p->integer = p->consume / 100;
    cout << "���֣�" << p->integer << endl;
    y = display_discount(p->integer);                      //���ú��������ۿ�
    cout << "�ۿ�:"/*<<setprecision(1)*/ << y << "��" << endl;
    p->next = head->next;
    head->next = p;
}
void Search(cnode* head, string& ID)
{
    cnode* p = new cnode;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "û�пͻ�!" << endl;
    else
    {
        while (p->next != NULL)
        {
            p = p->next;
            if (ID == p->ID)          //�ж����֤���Ƿ���ͬ
            {
                cout << "������" << p->name << endl;
                cout << "���֤�ţ�" << p->ID << endl;
                cout << "���ѣ�" <</*setprecision(2)<<*/p->consume << endl;
                cout << "����:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "�ۿ�" <</*setprecision(1)<<*/y << "��" << endl;
                return;
            }
        }
        cout << "�����ڸÿͻ���" << endl;
    }
}

void Amend(cnode* head, string& ID) {
    cnode* p;
    double y, z;
    int choose, x;
    p = head;
    if (p->next == NULL)
        cout << "û�пͻ�!" << endl;
    else
    {
        while (p->next != NULL)
        {
            p = p->next;
            if (ID == p->ID)     //�ж����֤���Ƿ���ͬ
            {
                cout << "������" << p->name << endl;
                cout << "���֤�ţ�" << p->ID << endl;
                cout << "���ѣ�"/*<<setprecision(2)*/ << p->consume << endl;
                cout << "����:" <</*setprecision(1)<<*/p->integer << endl;
                y = display_discount(p->integer);
                cout << "�ۿ�:" <</*setprecision(1)<<*/y << "��" << endl;
                cout << "��ѡ����Ҫ�޸ĵ�1��������2�����֤�š�3�����ѽ�";
                cin >> choose;
                if (choose == 1)
                {
                    cout << "�������޸ĺ�����;";
                    cin >> p->name;
                }
                if (choose == 2)
                {
                    cout << "�������޸ĺ�����֤��:";
                    cin >> p->ID;
                    isID(p->ID);
                }
                if (choose == 3)
                {
                    cout << "1.������ǰ���ѡ�2.���������ڷ���!��ѡ��:";
                    cin >> x;
                    if (x == 1)
                    {
                        cout << "�������޸ĺ������:";
                        cin >> p->consume;
                    }
                    else {
                        printf("���������ӽ��:");
                        cin >> z;
                        p->consume += z;
                    }
                }
                cout << "������" << p->name << endl;
                cout << "���֤�ţ�" << p->ID << endl;
                cout << "���ѣ�" <<p->consume << endl;
                p->integer = p->consume / 100.0;
                cout << "����:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "�ۿ�:" << y << "��" << endl;
                return;
            }
        }
        cout << "�����ڸÿͻ���" << endl;
    }
}
void Delete(cnode* head, string& ID)
{
    //ɾ���ͻ�����
    cnode* p;
    int x;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "û�пͻ�!" << endl;
    else
    {
        while (p->next != NULL)
        {
            head = p;
            p = p->next;
            if (ID == p->ID)
            {                 //�ж����֤���Ƿ���ͬ
                cout << "������" << p->name << endl;
                cout << "���֤�ţ�" << p->ID << endl;
                cout << "���ѣ�"<< p->consume << endl;
                cout << "����:" << p->integer << endl;
                y = display_discount(p->integer);
                cout << "�ۿ�:" <<y << "��" << endl;
                cout << "��ȷ��ɾ����1��ȷ����2��ȡ������ѡ��:";
                cin >> x;
                if (x == 1)
                {
                    head->next = p->next;
                    cout << ("ɾ���ɹ�!");
                }
                else
                    cout << "ɾ��ʧ��!";
                return;
            }
        }
        cout << "�����ڸÿͻ���" << endl;
    }
}
void Showall(cnode* head) //��ʾ���пͻ�����
{
    cnode* p;
    double y;
    p = head;
    if (p->next == NULL)
        cout << "û�пͻ�!" << endl;
    else
        while (p->next != NULL)
        {
            p = p->next;
            cout << "������" << p->name << endl;
            cout << "���֤�ţ�" << p->ID << endl;
            cout << "���ѣ�" <<p->consume << endl;
            cout << "���֣�" << p->integer << endl;
            y = display_discount(p->integer);
            cout << "�ۿۣ�" <<y << "��" << endl;
        }
}

void count(cnode* head)
{
    cnode* p;
    int i = 0;
    p = head;
    if (p->next == NULL)
        cout << "û�пͻ�!" << endl;
    else
        while (p->next != NULL)
        {
            p = p->next;
            i++;
        }
    cout << "���пͻ�����Ϊ" << i << "λ!" << endl;
}
double display_discount(double points)
{
    //����ͻ��ۿۺ���������һ��double�͵�����Ϊ�����������Ӧ���ۿ�
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
            cout << "�����ʽ����ȷ,���������룺" << endl;
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