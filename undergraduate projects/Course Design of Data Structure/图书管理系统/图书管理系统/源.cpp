#include <iostream>
#include <cstdio>
#include <cstring>
#include <string>  
#include <vector>                               //vector ˳������ ��������Խ .at()����
#include <algorithm>                            //ģ���  
#include <fstream>
#include <cctype>                               //�ַ������   �ַ����ԡ�ӳ��
#include <iomanip>                              //��������ͷ�ļ�
using namespace std;
struct student
{
	static int s1;
	int id;//���߱��
	string name;//��������
	int borrowsum;//���ѽ��Ķ��ٱ���,Ĭ��Ϊ0
	int number;//���ڻ��ж��ٱ���δ����Ĭ��Ϊ0
	string borrowday;//�ϴν���ʱ�䣬Ĭ��Ϊ0000.00.00
	int b[10];//��������ĵı�ţ����10��
	//char bookname[100];
	string bookname;
	string authorname;
};
struct book
{
	int idnum;//ͼ���ź�
	int BorrowCount;//ͼ�������,��ʼ��Ϊ0
	string name;//����
	string kind;//ͼ������
	double price;//ͼ��۸�
	int sum;//ͼ���ܿ�����
	int nowsum;//ͼ���ֿ����
	string author;//ͼ������
	bool ok;//�Ƿ�ɽ�,��ʼΪ����
	string borrowdate;//ͼ�����һ�ν��ʱ�䣬Ĭ��Ϊ0000-00-00��
	string returndate;//ͼ�����һ�ι黹ʱ�䣬Ĭ��Ϊ0000-00-00��
};
bool cmpByidnum(book a, book b)
{
	return a.idnum < b.idnum;
}
bool cmpByCount(book a, book b)
{
	return a.BorrowCount > b.BorrowCount;
}
bool cmpByBorrowsum(student a, student b)
{
	return a.borrowsum > b.borrowsum;
}
bool cmpByid(student a, student b)
{
	return a.id < b.id;
}
class Library
{
private:
	vector<book> data;
	vector<student> data1;
	vector<int> betoli;//ԤԼ�鵽�ݣ���������
public:
	Library();
	void AddBook(book NewBook);  //����ͼ��
	void DeleteBook(string bookname, string author);//ɾ��ͼ��
	void BorrowBook(string name, string author);//����ͼ��
	void BackBook(string name, string author, int k);//�黹ͼ��
	void ShowAllBook(); //���ϵͳ����ͼ��
	void SearchBookPosWithNum(int theauthor);//����Ų�ѯ
	void  SearchBookPosWithname(string thebook); //��������ѯ
	void  SearchBookPosWithAuthor(string theauthor);//�����߲�ѯ
	void  SearchBookPosWithKind(string kind);//�������ѯ
	int  SearchBookPosWithAB(string theauthor, string thebook);//�����ߺ�������ѯ
	void Save();  //����ͼ����ļ�
	void Save1();//����ѧ���ļ�
	void printbook(book a);//���ĳ�����������Ϣ
	void revisebook(string name, string author);//�޸�ĳ�������Ϣ
	int SerchStudent(int id);//��ѯĳ������
	void AddStudent(student a);//����һ������
	void PrintStudent(int kid);//���������Ϣ
	int GetStudent();//���ض�������
};
Library::Library()
{
	int AllBook, AllStudent;
	ifstream fin("book.txt");
	if (fin)
	{
		fin >> AllBook;
		for (int i = 0; i < AllBook; i++)
		{
			book tem;
			fin >> tem.idnum >> tem.name >> tem.author >> tem.price >> tem.kind >> tem.sum >> tem.nowsum >> tem.BorrowCount >> tem.ok >> tem.borrowdate >> tem.returndate;
			data.push_back(tem);              //������������
		}
		fin.close();
	}
	ifstream tfin("student.txt");
	if (tfin)
	{
		tfin >> AllStudent;
		for (int i = 0; i < AllStudent; i++)
		{
			student tem;
			tfin >> tem.id >> tem.name >> tem.borrowsum >> tem.number >> tem.borrowday;
			for (int j = 0; j < 10; j++)
			{
				tfin >> tem.b[j];
			}
			data1.push_back(tem);
		}
		tfin.close();
	}
}
int Library::GetStudent()
{
	int k = (int)data1.size();
	return k + 1;
}
void Library::AddBook(book NewBook)
{
	data.push_back(NewBook);
}
void Library::AddStudent(student newstudent)
{
	data1.push_back(newstudent);
}
void Library::DeleteBook(string bookname, string author)
{
	int pos = SearchBookPosWithAB(author, bookname);
	if (pos != -1)
	{
		data.erase(data.begin() + pos);
		Save();
		return;
	}
	else
		cout << "���޴��飡\n";
}
void Library::BorrowBook(string name, string author)
{
	string BorrowDate;
	string BackDate;
	char c;
	int flag = 0;
	int sid = -1;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == name && data[i].author == author)
		{
			if (data[i].nowsum)
			{
				cout << "������ߵĶ��ߺ��ǣ�";
				cin >> sid;
				if (data1[sid - 1].number > 10)
				{
					cout << "����ͬʱ����10���飡�����ٽ裡" << endl;
					break;
				}
				flag = 1;
				data[i].nowsum = data[i].nowsum - 1;
				data[i].BorrowCount = data[i].BorrowCount + 1;
				cout << "�������������" << endl;
				cin >> BorrowDate;
				data[i].borrowdate = BorrowDate;
				cout << "������Ԥ�ƹ黹����" << endl;
				cin >> BackDate;
				data[i].returndate = BackDate;
				data[i].ok = bool(data[i].nowsum);
				data1[sid - 1].number++;
				for (int j = 0; j < 10; j++)
				{
					if (data1[sid - 1].b[j] == 0)
						data1[sid - 1].b[j] = data[i].idnum;
					    data1[sid - 1].bookname = data[i].name.data();
					    data1[sid - 1].authorname = data[i].author;
					Save();
					Save1();
				}
				cout << "���ĳɹ�" << endl;
			}
			else
			{
				cout << "��Ǹ�Ȿ����Ϊ�㣬�޷�����" << endl;
			}
		}
	}
	if (!flag)
		cout << "��Ǹ��δ�ҵ���Ҫ�ҵ��顣" << endl;
}
void Library::BackBook(string name, string author, int k)//k��ʾ����;��
{
	int c = -1;
	{
		cout << "��������Ķ��ߺţ�";
		cin >> c;
		c = c - 1;
	}
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == name && data[i].author == author)
		{
			data[i].nowsum = data[i].nowsum + 1;
			data[i].ok = bool(data[i].nowsum);
			for (int j = 0; j < 10; j++)
			{
				if (data1[c].b[j] == data[i].idnum)
					data1[c].b[j] = 0;
			}
			data1[c].number--;
			break;
		}
	}
	Save();
	Save1();
	cout << "����ɹ�" << endl;
}
void Library::printbook(book a)
{

	cout << " ���:" << setw(12) << a.idnum;
	cout << " ����:" << setw(14) << a.name;
	cout << " ����:" << setw(14) << a.author << endl;
	cout << " �۸�:" << setw(14) << fixed << setprecision(2) << a.price;
	cout << " ����:" << setw(14) << a.kind;
	cout << " �ܿ����:" << setw(10) << a.sum;
	cout << " �ֿ����:" << setw(10) << a.nowsum;
	cout << " ͼ�������:" << setw(14) << a.BorrowCount << endl;
	cout << " ״̬:" << setw(14) << (a.ok == 0 ? "���ɽ�" : "�ɽ�");
	cout << " ���ڽ������:" << setw(14) << a.borrowdate;
	cout << " ���ڹ黹����:" << setw(14) << a.returndate << endl;
	cout << endl << endl;
}
void Library::PrintStudent(int kid)
{
	int id = kid - 1;
	cout << setw(8) << data1[id].id;
	cout << setw(8) << data1[id].name;
	cout << setw(18) << data1[id].number;
	if (data1[id].number)
	{
		
		cout << "                 " << endl;
		cout << "�㵱ǰ������Щ�飺\n";
		cout << setw(16) << "���" << setw(16) << "����" << setw(16) << "����" << endl;
		for (int i = 0; i < 1; i++)
		{
			
			if (data1[id].b[i] != 0)
				cout << setw(16) << data1[id].b[i]<< setw(16) << data1[id].bookname << setw(16) << data1[id].authorname<< endl;
		}
	}
	else
		cout << "�㵱ǰ��δ���κ���,��ȥ�豾�鿴���ɣ�\n";
}
void Library::ShowAllBook()
{
	system("cls");
	cout << "����ͼ��Ϊ:" << endl;
	for (int i = 0; i < (int)data.size(); i++)
	{
		printbook(data[i]);
	}
}
int Library::SerchStudent(int id)
{
	int m = -1;
	for (int i = 0; i < (int)data1.size(); i++)
	{
		if (data1[i].id == id)
		{
			return i;
		}
	}
	return m;
}
void Library::SearchBookPosWithNum(int thenum)//����Ų�ѯ
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].idnum == thenum)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "���޴˱�ţ�";
}
void Library::SearchBookPosWithname(string thebook)//��������ѯ
{
	int flag = 0;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == thebook)
		{
			printbook(data[i]);
			flag = 1;
		}
	}
	if (!flag) cout << "���޴��飡\n";
}
void Library::SearchBookPosWithAuthor(string theauthor)//�����߲�ѯ
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].author == theauthor)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "���޴����ߵ��飡";
}
void Library::SearchBookPosWithKind(string kind)//�������ѯ
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); ++i)
	{
		if (data[i].kind == kind)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "���޴����飡";
}
int Library::SearchBookPosWithAB(string theauthor, string thebook)//�����ߺ�������ѯ
{
	for (int i = 0; i < (int)data.size(); ++i)
	{
		if (data[i].author == theauthor && data[i].name == thebook)
		{
			printbook(data[i]);
			return i;
		}
	}
	cout << "���޴��飡";
	return -1;
}
void Library::Save() //�����鼮�ļ�
{
	ofstream fout("book.txt");
	if (fout)
	{
		fout << data.size() << endl;
		for (int i = 0; i < (int)data.size(); i++)
		{
			fout << data[i].idnum << " " << data[i].name << " " << data[i].author << " " << data[i].price << " " << data[i].kind /*<< " " << data[i].room */ << " " << data[i].sum << " " << data[i].nowsum << " " << data[i].BorrowCount << " " << data[i].ok/* << " " << data[i].appointment */ << " " << data[i].borrowdate << " " << data[i].returndate << " " << endl;
		}
		fout.close();
	}
}
void Library::Save1() //����ѧ���ļ�
{
	ofstream fout("student.txt");
	if (fout)
	{
		fout << data1.size() << endl;
		for (int i = 0; i < (int)data1.size(); i++)
		{
			fout << data1[i].id << " " << data1[i].name << " " << data1[i].borrowsum << " " << data1[i].number << " " << data1[i].borrowday<<endl;
			for (int j = 0; j < 10; j++)
			{
				fout << " " << data1[i].b[j]<<" "<<data1[i].bookname<<endl;
			}
			fout << endl;
		}
		fout.close();
	}
}
void Library::revisebook(string name, string author)//�޸�ͼ��
{
	Library mybook;
	string  Kind;
	int num1, num2, k = 0;
	printf("��Ҫ�޸ĵ������ǣ�\n");
	printf("1.ͼ���ֿ�����޸�\n");
	printf("2.ͼ���ܿ�����޸�\n");
	printf("3.ͼ�����������޸�\n");
	printf("4.�˳�\n");
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].author == author && data[i].name == name)
		{
			k = i;
			break;
		}
	}
	int cho;
	do
	{
		cin >> cho;
		switch (cho)
		{
		case 1:
		{
			cout << "�������µ��ֿ������\n";
			cin >> num1;
			data[k].nowsum = num1;
			Save();
			cout << "�޸ĳɹ�" << endl;
			break;
		}
		case 2:
		{
			cout << "�������µ��ܿ������\n";
			cin >> num2;
			data[k].sum = num2;
			Save();
			cout << "�޸ĳɹ�" << endl;
			break;
		}
		case 3:
		{
			cout << "������ͼ�����������ࣺ\n";
			cin >> Kind;
			data[k].kind = Kind;
			Save();
			cout << "�޸ĳɹ�" << endl;
			break;
		}
		}
	} while (cho < 3);
}

int main()
{
	cout.setf(ios::left);
	Library mybook;
	L1:cout << "************************** ��ӭʹ�û�������ѧͼ�����ϵͳ **************************" << endl << endl;
	cout << "��������߱�ŵ�¼" << endl;
	int mm = 510640;
	int bh, k = 0, z = 0, cho;

	cin >> bh;
	if (bh == mm)
	{
		cout << "��ӭʹ��" << endl;
		k = 2;
	}
	else    z = 3;

	if (k == 2) {
		do
		{
		    L3:cout << "��ӭ�������Աϵͳ" << endl;
			cin.clear();
			cin.sync();
			cout << " ***    1.ͼ��Ŀ¼    ***" << endl;
			cout << " ***    2.��ѯͼ��    ***" << endl;
			cout << " ***    3.���ͼ��    ***" << endl;
			cout << " ***    4.ɾ��ͼ��    ***" << endl;
			cout << " ***  5.�޸�ͼ����Ϣ  ***" << endl;
			cout << " ***      0.�˳�      ***" << endl;
			cout << "-------------------------------------------------------------------------------------------------------------------" << endl;
			cout << "��ѡ����,����ָ�� " << endl;
			cin >> cho;
			switch (cho)
			{
			case 1:
			{
				int cho2;
				mybook.ShowAllBook();
				cout << "--------------------------------------------------------------------------------------------------------------------" << endl;
				
				break;
			}
			case 2:
			{
				int p1;
				do
				{
					L2: cout << " ***       0.����       *** " << endl;
					cout << " ***    1.��������ѯ    *** " << endl;
					cout << " ***    2.�����߲�ѯ    *** " << endl;
					cout << " ***    3.�������ѯ    *** " << endl;
					cout << " ***    4.����Ų�ѯ    *** " << endl;
					cout << " *** ��ѡ����,����ָ�� *** " << endl;
					
					string Name, Author, Kind;
					int thenum;
					cin >> p1;
					if (p1 >= 0 && p1 <= 4)
					{
						do
						{
							switch (p1)
							{
							case 1:do
							{
								cout << "������������" << endl;
								cin >> Name;
								mybook.SearchBookPosWithname(Name); //��������ѯ
								break;
							} while (p1 != 0); break;
							case 2:
							{
								cout << "���������ߣ�" << endl;
								cin >> Author;
								mybook.SearchBookPosWithAuthor(Author);//�����߲�ѯ
								break;
							}
							case 3:
							{
								cout << "���������࣡" << endl;
								cin >> Kind;
								mybook.SearchBookPosWithKind(Kind);//�������ѯ
								break;
							}
							case 4:
							{
								cout << "�������ţ�" << endl;
								cin >> thenum;
								mybook.SearchBookPosWithNum(thenum);//����Ų�ѯ
								break;
							}
							case 0:
							{
								goto L3;
							}
							}

						} while (p1 <= 0);

						break;
					}
					else
					{
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						break;
					}
					
				} while (p1 >= 1 && p1 <= 4);
				goto L2;
				break;
			}
			case 3:         //����ͼ��
			{
				book temp;
				cin.clear();
				cin.sync();
				cout << "���:";
				cin >> temp.idnum;
				cout << "����:";
				cin >> temp.name;
				cout << "���ߣ�";
				cin >> temp.author;
				cout << "�۸�:";
				cin >> temp.price;
				cout << "����:";
				cin >> temp.kind;
				cout << "����:";
				cin >> temp.sum;
				temp.nowsum = temp.sum;
				temp.BorrowCount = 0;
				temp.ok = true;
				temp.borrowdate = "0000.00.00";
				temp.returndate = "0000.00.00";
				mybook.AddBook(temp);
				mybook.Save();
				cout << "��Ϣ����ɹ�" << endl;
				break;
			}
			case 4:         //ɾ��ͼ��
			{
				string bookname, bookauthor;
				cout << "����������������:" << endl;
				cin >> bookname >> bookauthor;
				mybook.DeleteBook(bookname, bookauthor);
				break;
			}
			case 5://�޸�ͼ����Ϣ
			{
				string name, author;
				cout << "������Ҫ�޸ĵ����������ߣ�" << endl;
				cin >> name >> author;
				mybook.revisebook(name, author);
				break;
			}
			case 0:
			{
				goto L1;
			}
			}
		} while (cho >= 1 && cho <= 5);
		{
			cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
			cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
			cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
			system("pause");
		}
	}

	if (z == 3)
	{


		if (mybook.SerchStudent(bh) == -1)
		{
			int n;
			cout << "�㲻�Ǵ�ϵͳ���ߣ��Ƿ�ע�᣿\n";
			cout << "                    1.ע��\n";
			cout << "                    2.����Ҫ\n";
			cin >> n;
			student temp;
			if (n == 1)
			{
				cout << "�������������:";
				cin >> temp.name;
				cin.clear();
				cin.sync();
				temp.id = mybook.GetStudent();
				temp.borrowsum = 0;
				temp.number = 0;
				temp.borrowday = "0000.00.00";
				for (int i = 0; i < 10; i++)
				{
					temp.b[i] = 0;
				}
				mybook.AddStudent(temp);
				mybook.Save1();
				cout << "                ע��ɹ������ס��Ķ��ߺţ�����������ϵ����Ա!\n";
				cout << "                ����:" << temp.name << endl;
				cout << "                ���ߺţ�" << temp.id << endl;
				k = temp.id;
				do
				{

					cin.clear();
					cin.sync();
					L7:cout << "***    0.����    ***" << endl;
					cout << "***  1.��ѯͼ��  ***" << endl;
					cout << "***  2.����ͼ��  ***" << endl;
					cout << "***  3.�黹ͼ��  ***" << endl;
					cout << "***4.��ѯ������Ϣ***" << endl;
					cout << "***��ѡ����,����ָ��***" << endl;
					cin >> cho;
					int thenum;
					switch (cho)
					{
					case 1:
					{   L6:cout << " ***    0.����    *** " << endl;
					cout << " *** 1.��������ѯ *** " << endl;
					cout << " *** 2.�����߲�ѯ *** " << endl;
					cout << " *** 3.�������ѯ *** " << endl;
					cout << " *** 4.����Ų�ѯ *** " << endl;
					cout << " *** ��ѡ����,����ָ�� *** " << endl;
					int p1;
					string Name, Author, Kind;
					cin >> p1;
					if (p1 >= 0 && p1 <= 4)
					{
						do
						{
							switch (p1)
							{
							case 1:do
							{
								cout << "������������" << endl;
								cin >> Name;
								mybook.SearchBookPosWithname(Name); //��������ѯ
								break;
							} while (p1 != 0); break;
							case 2:
							{
								cout << "���������ߣ�" << endl;
								cin >> Author;
								mybook.SearchBookPosWithAuthor(Author);//�����߲�ѯ
								break;
							}
							case 3:
							{
								cout << "���������࣡" << endl;
								cin >> Kind;
								mybook.SearchBookPosWithKind(Kind);//�������ѯ
								break;
							}
							case 4:
							{
								cout << "�������ţ�" << endl;
								cin >> thenum;
								mybook.SearchBookPosWithNum(thenum);//����Ų�ѯ
								break;
							}
							case 0:
							{
								goto L7;
							}
							}
						}

						while (p1 >= 1 && p1 <= 4); break;
					}
					else
					{
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						break;
					}
					goto L6;
					break;
					}
					case 2:
					{
						string bookname, bookauthor;
						cout << "������Ҫ������������ߣ�" << endl;
						cin >> bookname >> bookauthor;
						mybook.BorrowBook(bookname, bookauthor);
						mybook.Save();
						system("pause");
						break;
					}
					case 3:
					{
						string bookname, bookauthor;
						cout << "������Ҫ�������������ߣ�" << endl;
						cin >> bookname >> bookauthor;
						mybook.BackBook(bookname, bookauthor, -1);
						mybook.Save();
						system("pause");
						break;
					}
					case 4:
					{
						cout << setw(8) << "���ߺ�" << setw(8) << "����"<< setw(8) << "���ڽ��������" << endl;
						mybook.PrintStudent(k);
						system("pause");
						break;
					}
					case 0:
					{
						goto L1;
					}
					}
				} while (cho >= 1 && cho <= 4);
				{cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				system("pause");
				}

			}
			else

				return(0);
		}


		else
		{
			k = bh;
		}

		do
		{

			cin.clear();
			cin.sync();
			L5:cout << "***    0.�˳�    ***" << endl;
			cout << "***  1.��ѯͼ��  ***" << endl;
			cout << "***  2.����ͼ��  ***" << endl;
			cout << "***  3.�黹ͼ��  ***" << endl;
			cout << "***4.��ѯ������Ϣ***" << endl;
			cout << "***��ѡ����,����ָ��***" << endl;
			cin >> cho;
			switch (cho)
			{
			case 1:
			{   L4:cout << " ***    0.����    *** " << endl;
			cout << " *** 1.��������ѯ *** " << endl;
			cout << " *** 2.�����߲�ѯ *** " << endl;
			cout << " *** 3.�������ѯ *** " << endl;
			cout << " *** 4.����Ų�ѯ *** " << endl;
			cout << " *** ��ѡ����,����ָ�� *** " << endl;
			int p1;
			string Name, Author, Kind;
			int thenum;
			cin >> p1;
			if (p1 >= 0 && p1 <= 4)
			{
				do
				{
					switch (p1)
					{
					case 1:do
					{
						cout << "������������" << endl;
						cin >> Name;
						mybook.SearchBookPosWithname(Name); //��������ѯ
						break;
					} while (p1 != 0); break;
					case 2:
					{
						cout << "���������ߣ�" << endl;
						cin >> Author;
						mybook.SearchBookPosWithAuthor(Author);//�����߲�ѯ
						break;
					}
					case 3:
					{
						cout << "���������࣡" << endl;
						cin >> Kind;
						mybook.SearchBookPosWithKind(Kind);//�������ѯ
						break;
					}
					case 4:
					{
						cout << "�������ţ�" << endl;
						cin >> thenum;
						mybook.SearchBookPosWithNum(thenum);//����Ų�ѯ
						break;
					}
					case 0:
					{
						goto L5; 
					}
					
					}
				} while (p1 < 0);
				goto L4;
				break;
			}
			else
			{
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				break;
			}
			goto L4;
			break;
			}
			case 2:
			{
				string bookname, bookauthor;
				cout << "������Ҫ������������ߣ�" << endl;
				cin >> bookname >> bookauthor;
				mybook.BorrowBook(bookname, bookauthor);
				mybook.Save();
				system("pause");
				break;
			}
			case 3:
			{
				string bookname, bookauthor;
				cout << "������Ҫ�������������ߣ�" << endl;
				cin >> bookname >> bookauthor;
				mybook.BackBook(bookname, bookauthor, -1);
				mybook.Save();
				system("pause");
				break;
			}
			case 4:
			{
				cout << setw(8) << "���ߺ�" << setw(8) << "����" << setw(8) << "���ڽ��������" << endl;
				mybook.PrintStudent(k);
				system("pause");
				break;
			}
			default:
				goto L1;
			}
		} while (cho >= 1 && cho <= 4);
		{cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
		cout << "!!!!!!!!!!��������ȷָ��!!!!!!!!!!" << endl;
		cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
		system("pause");
		}

	}
}
